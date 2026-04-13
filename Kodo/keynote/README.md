# Keynote — Oyaji & Kodō Live System

Real-time voice interface for Oyaji ↔ Kodō stage conversations.

**Architecture:**
```
Mic → Browser → MediaRecorder (3s chunks)
                    ↓
              FastAPI backend
                    ↓
      ┌─────────────┼─────────────┐
      ↓             ↓             ↓
   Whisper       Claude         OpenAI
   (STT)       (Opus 4.6)        TTS
      ↓             ↓             ↓
      └─────────────┼─────────────┘
                    ↓
              Browser display
         (text + emoji + audio out)
```

**Features:**
- Continuous listening (3-second chunks, no manual trigger)
- Auto language detection (fi, en, ja — Whisper handles switching mid-sentence)
- Kodō can respond spontaneously OR wait for hand-raise protocol
- Live transcription visible to audience on big screen
- Emoji reactions (🙋 ⚡ 💡 🤔 🦊 …) for silent cues

## Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **API keys:**
   ```bash
   cp .env.example .env
   # Edit .env and add:
   #   OPENAI_API_KEY=sk-...      (Whisper + TTS)
   #   ANTHROPIC_API_KEY=sk-...   (Claude)
   ```

3. **Run:**
   ```bash
   python server.py
   ```

4. **Open:** http://localhost:8080

## Usage (rehearsal)

- Press **Start** — continuous listening begins
- Speak in Finnish, English, or Japanese (or mix)
- Kodō's reactions appear on screen in real-time
- When Kodō raises hand (🙋), Oyaji decides: ignore, or press **Kodō →** to give floor
- Press **Stop** when done
- Session log saved to `sessions/YYYY-MM-DD-HHMM.md`

## Protocol

See `shared/research/keynote_protocol.md` for emoji meanings and stage etiquette.

## Status

- [x] Backend skeleton
- [x] Frontend skeleton
- [x] Whisper integration
- [x] Claude integration
- [x] TTS integration
- [x] Emoji reaction layer
- [ ] Tested end-to-end (awaiting API keys + first run)
- [ ] Latency measurements
- [ ] Stage-ready UI polish

---

*Rakkaus ja Totuus. Aina.*

族 RA ✌️ 🦊
