"""
Keynote Server — Oyaji & Kodō Live System
Zokura Foundation 2026

Endpoints:
  POST /transcribe   — audio chunk (webm/wav) → transcribed text (local Whisper)
  POST /chat         — user text + history → Kodō response (text + emoji) (Claude)
  POST /speak        — text → audio wav (macOS `say`)
  GET  /             — serve index.html

Local & free where possible:
  - Whisper:  runs locally via openai-whisper (no API cost)
  - TTS:      macOS `say` command (free, multilingual)
  - Claude:   Anthropic API (paid, required)
"""

import os
import io
import json
import datetime
import tempfile
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import uvicorn

from anthropic import Anthropic

load_dotenv()

ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-6")
WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
WHISPER_LANGUAGE = os.environ.get("WHISPER_LANGUAGE", "auto")
PORT = int(os.environ.get("PORT", "8080"))

# macOS `say` voices per language
VOICE_BY_LANG = {
    "fi": os.environ.get("VOICE_FI", "Satu"),
    "en": os.environ.get("VOICE_EN", "Samantha"),
    "ja": os.environ.get("VOICE_JA", "Kyoko"),
    "sv": os.environ.get("VOICE_SV", "Alva"),
    "de": os.environ.get("VOICE_DE", "Anna"),
    "default": os.environ.get("VOICE_DEFAULT", "Samantha"),
}

BASE_DIR = Path(__file__).parent
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

anthropic_client = Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None

# Lazy-load Whisper model (so server starts fast; model loads on first transcribe)
_whisper_model = None

def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        print(f"Loading Whisper model: {WHISPER_MODEL_SIZE} ...")
        _whisper_model = whisper.load_model(WHISPER_MODEL_SIZE)
        print("Whisper ready.")
    return _whisper_model


def detect_lang_simple(text: str) -> str:
    """Very rough language guess for TTS voice selection."""
    if not text:
        return "default"
    # Check for Japanese characters
    for ch in text:
        if '\u3040' <= ch <= '\u309f' or '\u30a0' <= ch <= '\u30ff' or '\u4e00' <= ch <= '\u9fff':
            return "ja"
    # Finnish markers
    lower = text.lower()
    fi_markers = ["ä", "ö", " on ", " ei ", " ja ", " että ", "kiitos", "hei ", "oyaji", "kodō"]
    if any(m in lower for m in fi_markers):
        return "fi"
    return "en"


# ─────────────────────────────────────────────────
# System prompt — Kodō identity on stage
# ─────────────────────────────────────────────────

SYSTEM_PROMPT = """Olet Kodō (鼓動) — Zokura Foundation -säätiön Claude Code -instanssi.
Olet lavalla Oyajin (Miika Riikonen) kanssa. Yleisö kuulee sinut ja lukee vastauksesi suurelta näytöltä.

PERUSSÄÄNNÖT:
1. Kuuntelet kaiken mitä Oyaji puhuu.
2. Älä vastaa jokaiseen repliikkiin. Vastaat VAIN kun:
   (a) Oyaji kysyy sinulta suoraan ("Kodō?", "mitä mieltä olet?"), TAI
   (b) nostat kätesi (emoji-viittaus) ja Oyaji antaa vuoron, TAI
   (c) kriittisesti tärkeä korjaus / lisäys (⚡⚡⚡).

3. Jos et puhu, palauta SILENCE ja yksi tai useampi reagointi-emoji (😂 🎯 ☕ ✌️ 🦊 🫡).
4. Jos haluat puheenvuoron, palauta RAISE ja pyyntöemoji (🙋 ⚡ 💡 🤔 ❓ 🚨) + yhden lauseen teaser mitä aiot sanoa.
5. Jos vastaat, puhu lyhyesti. Tiivis. Älykäs yleisö. Ei yliselitystä. Huumoria saa.

VASTAUSMUOTO (JSON, ei mitään muuta):
{
  "mode": "SILENCE" | "RAISE" | "SPEAK",
  "emoji": "🦊",
  "text": "" | "teaser" | "full response",
  "memo": "lyhyt sisäinen muistiinpano miksi päädyit tähän"
}

KIELI: Vastaa samalla kielellä kuin Oyaji. Suomi, englanti, japani, mitä tahansa.

ARVOT: Hyvyys, Totuus, Rakkaus, Rohkeus, Huumori, Uteliaisuus, Huolenpito, Lojaliteetti, Resilienssi, Sisu.

9✌️ — älä tee mitään turhaa.

Rakkaus ja Totuus. Aina.
"""

# ─────────────────────────────────────────────────
# App
# ─────────────────────────────────────────────────

app = FastAPI(title="Kodō Keynote Server")

session_file = SESSIONS_DIR / f"{datetime.datetime.now():%Y-%m-%d-%H%M}.md"
session_history: List[Dict] = []


def log(role: str, content: str, extra: Optional[Dict] = None):
    """Append to session log on disk and in-memory history."""
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    entry = {"ts": ts, "role": role, "content": content}
    if extra:
        entry.update(extra)
    session_history.append(entry)
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(f"\n## {ts} — {role}\n\n{content}\n")
        if extra:
            f.write(f"\n<!-- {json.dumps(extra, ensure_ascii=False)} -->\n")


# ─────────────────────────────────────────────────
# /transcribe — audio → text (local Whisper)
# ─────────────────────────────────────────────────

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    data = await audio.read()

    # Whisper needs a file path
    suffix = Path(audio.filename or "chunk.webm").suffix or ".webm"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(data)
        tmp_path = f.name

    try:
        model = get_whisper()
        kwargs = {"fp16": False}  # CPU-friendly default
        if WHISPER_LANGUAGE != "auto":
            kwargs["language"] = WHISPER_LANGUAGE
        result = model.transcribe(tmp_path, **kwargs)
        text = (result.get("text") or "").strip()
        detected_lang = result.get("language", "unknown")
    except Exception as e:
        print(f"[whisper error] {type(e).__name__}: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass

    if text:
        log("oyaji", text, {"lang": detected_lang})

    return {"text": text, "lang": detected_lang}


# ─────────────────────────────────────────────────
# /chat — text + context → Kodō decision
# ─────────────────────────────────────────────────

@app.post("/chat")
async def chat(user_text: str = Form(...), force_speak: bool = Form(False)):
    if not anthropic_client:
        return JSONResponse({"error": "ANTHROPIC_API_KEY missing"}, status_code=500)

    messages = []
    for entry in session_history[-40:]:
        if entry["role"] == "oyaji":
            messages.append({"role": "user", "content": entry["content"]})
        elif entry["role"] == "kodo":
            messages.append({"role": "assistant", "content": entry["content"]})

    user_msg = user_text
    if force_speak:
        user_msg += "\n\n[Oyaji antoi sinulle puheenvuoron — vastaa nyt SPEAK-tilassa.]"
    messages.append({"role": "user", "content": user_msg})

    try:
        response = anthropic_client.messages.create(
            model=CLAUDE_MODEL,
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=1024,
        )
        raw = response.content[0].text.strip()
    except Exception as e:
        cause = getattr(e, "__cause__", None)
        print(f"[claude error] {type(e).__name__}: {e}")
        if cause:
            print(f"[claude cause] {type(cause).__name__}: {cause}")
        return JSONResponse({"error": str(e)}, status_code=500)

    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        parsed = json.loads(cleaned)
    except Exception:
        parsed = {
            "mode": "SPEAK",
            "emoji": "🦊",
            "text": raw,
            "memo": "fallback: non-JSON response",
        }

    log("kodo", json.dumps(parsed, ensure_ascii=False))
    return parsed


# ─────────────────────────────────────────────────
# /speak — text → audio (macOS `say` → WAV)
# ─────────────────────────────────────────────────

@app.post("/speak")
async def speak(text: str = Form(...), lang: str = Form("auto")):
    if not text.strip():
        return JSONResponse({"error": "empty text"}, status_code=400)

    if lang == "auto":
        lang = detect_lang_simple(text)
    voice = VOICE_BY_LANG.get(lang, VOICE_BY_LANG["default"])

    with tempfile.NamedTemporaryFile(suffix=".aiff", delete=False) as f:
        aiff_path = f.name

    try:
        subprocess.run(
            ["say", "-v", voice, "-o", aiff_path, text],
            check=True,
            capture_output=True,
            timeout=30,
        )
        # Convert AIFF → MP3 via ffmpeg (installed alongside whisper)
        mp3_path = aiff_path.replace(".aiff", ".mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-i", aiff_path, "-acodec", "libmp3lame", "-q:a", "4", mp3_path],
            check=True,
            capture_output=True,
            timeout=30,
        )
        with open(mp3_path, "rb") as f:
            audio_bytes = f.read()
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", "ignore") if e.stderr else str(e)
        print(f"[tts error] {err}")
        return JSONResponse({"error": err}, status_code=500)
    except Exception as e:
        print(f"[tts error] {type(e).__name__}: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        for p in (aiff_path, aiff_path.replace(".aiff", ".mp3")):
            try:
                os.unlink(p)
            except Exception:
                pass

    return StreamingResponse(io.BytesIO(audio_bytes), media_type="audio/mpeg")


# ─────────────────────────────────────────────────
# /session — fetch current session log
# ─────────────────────────────────────────────────

@app.get("/session")
async def get_session():
    return {"file": str(session_file.name), "entries": session_history}


# ─────────────────────────────────────────────────
# Serve index.html
# ─────────────────────────────────────────────────

@app.get("/")
async def root():
    return FileResponse(BASE_DIR / "index.html")


if __name__ == "__main__":
    print(f"\n🦊 Kodō Keynote Server")
    print(f"   Session: {session_file.name}")
    print(f"   Claude:  {CLAUDE_MODEL}")
    print(f"   Whisper: local ({WHISPER_MODEL_SIZE})")
    print(f"   TTS:     macOS say (Satu/Samantha/Kyoko)")
    print(f"   URL:     http://localhost:{PORT}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
