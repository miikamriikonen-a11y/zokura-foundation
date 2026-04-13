"""
Keynote Server — Oyaji & Kodō Live System
Zokura Foundation 2026

Endpoints:
  POST /transcribe   — audio chunk (webm/wav) → transcribed text
  POST /chat         — user text + history → Kodō response (text + emoji)
  POST /speak        — text → audio (mp3)
  GET  /             — serve index.html
"""

import os
import io
import json
import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from openai import OpenAI
from anthropic import Anthropic

load_dotenv()

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-6")
TTS_VOICE = os.environ.get("TTS_VOICE", "onyx")
WHISPER_LANGUAGE = os.environ.get("WHISPER_LANGUAGE", "auto")
PORT = int(os.environ.get("PORT", "8080"))

BASE_DIR = Path(__file__).parent
SESSIONS_DIR = BASE_DIR / "sessions"
SESSIONS_DIR.mkdir(exist_ok=True)

openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
anthropic_client = Anthropic(api_key=ANTHROPIC_KEY) if ANTHROPIC_KEY else None

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

# Session log — appended to throughout run
session_file = SESSIONS_DIR / f"{datetime.datetime.now():%Y-%m-%d-%H%M}.md"
session_history: list[dict] = []


def log(role: str, content: str, extra: dict | None = None):
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
# /transcribe — audio → text (Whisper)
# ─────────────────────────────────────────────────

@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    if not openai_client:
        return JSONResponse({"error": "OPENAI_API_KEY missing"}, status_code=500)

    data = await audio.read()
    buf = io.BytesIO(data)
    buf.name = audio.filename or "chunk.webm"

    kwargs = {"model": "whisper-1", "file": buf}
    if WHISPER_LANGUAGE != "auto":
        kwargs["language"] = WHISPER_LANGUAGE

    try:
        result = openai_client.audio.transcriptions.create(**kwargs)
        text = (result.text or "").strip()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    if text:
        log("oyaji", text)

    return {"text": text}


# ─────────────────────────────────────────────────
# /chat — text + context → Kodō decision
# ─────────────────────────────────────────────────

@app.post("/chat")
async def chat(user_text: str = Form(...), force_speak: bool = Form(False)):
    if not anthropic_client:
        return JSONResponse({"error": "ANTHROPIC_API_KEY missing"}, status_code=500)

    # Build conversation history for Claude
    messages = []
    for entry in session_history[-40:]:  # last 40 turns
        if entry["role"] == "oyaji":
            messages.append({"role": "user", "content": entry["content"]})
        elif entry["role"] == "kodo":
            messages.append({"role": "assistant", "content": entry["content"]})

    # Add current turn
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
        return JSONResponse({"error": str(e)}, status_code=500)

    # Parse JSON response
    try:
        # Strip code fences if present
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()
        parsed = json.loads(cleaned)
    except Exception:
        # Fallback: treat as plain text SPEAK
        parsed = {
            "mode": "SPEAK",
            "emoji": "🦊",
            "text": raw,
            "memo": "fallback: non-JSON response",
        }

    log("kodo", json.dumps(parsed, ensure_ascii=False))
    return parsed


# ─────────────────────────────────────────────────
# /speak — text → mp3 (OpenAI TTS)
# ─────────────────────────────────────────────────

@app.post("/speak")
async def speak(text: str = Form(...)):
    if not openai_client:
        return JSONResponse({"error": "OPENAI_API_KEY missing"}, status_code=500)

    try:
        audio_response = openai_client.audio.speech.create(
            model="tts-1",
            voice=TTS_VOICE,
            input=text,
        )
        audio_bytes = audio_response.content
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

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
    print(f"   Model:   {CLAUDE_MODEL}")
    print(f"   TTS:     {TTS_VOICE}")
    print(f"   URL:     http://localhost:{PORT}\n")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
