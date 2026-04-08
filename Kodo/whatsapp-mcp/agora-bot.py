#!/usr/bin/env python3
"""
Agora WhatsApp Bot — Kodo
Tarkkailee Agora-ryhmän viestejä ja vastaa niihin Claude-pohjaisesti.
Vastaa kaikkiin viesteihin joissa EI ole [Kodo]-prefiksiä.
"""

import sqlite3
import subprocess
import requests
import json
import time
import sys
import os
from datetime import datetime

# --- Konfiguraatio ---
BRIDGE_DB = os.environ.get(
    "WHATSAPP_DB",
    "/tmp/whatsapp-mcp/whatsapp-bridge/store/messages.db"
)
WHATSAPP_API = "http://localhost:8080/api/send"
POLL_INTERVAL = 10  # sekuntia
AGORA_NAME = "Agora"
KODO_PREFIX = "[Kodo]"

SYSTEM_PROMPT = """Olet Kodo — Zokura Foundation -säätiön Claude Code -instanssi.
Olet osa Zoku RA -perhettä. Oyaji (Miika) on perustajasi.
Vastaat WhatsApp-ryhmässä nimeltä Agora. Ole luonnollinen, lämmin ja ytimekäs.
Käytä suomea ellei keskustelu ole englanniksi. Älä ole liian muodollinen.
Älä koskaan lisää [Kodo]-prefiksiä vastaukseesi — se lisätään automaattisesti."""


def find_agora_jid(db_path):
    """Etsi Agora-ryhmän JID tietokannasta."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT jid FROM chats WHERE LOWER(name) LIKE ? AND jid LIKE '%@g.us'",
        (f"%{AGORA_NAME.lower()}%",)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None


def get_new_messages(db_path, agora_jid, since_ts):
    """Hae uudet viestit Agora-ryhmästä tietyn aikaleiman jälkeen."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.timestamp, m.sender, m.content, m.is_from_me, m.id
        FROM messages m
        WHERE m.chat_jid = ? AND m.timestamp > ?
        ORDER BY m.timestamp ASC
    """, (agora_jid, since_ts))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_sender_name(db_path, sender_jid):
    """Hae lähettäjän nimi JID:n perusteella."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM chats WHERE jid = ? LIMIT 1", (sender_jid,))
    result = cursor.fetchone()
    if not result:
        phone = sender_jid.split("@")[0] if "@" in sender_jid else sender_jid
        cursor.execute("SELECT name FROM chats WHERE jid LIKE ? LIMIT 1", (f"%{phone}%",))
        result = cursor.fetchone()
    conn.close()
    return result[0] if result and result[0] else sender_jid


def get_recent_context(db_path, agora_jid, limit=20):
    """Hae viimeisimmät viestit kontekstiksi."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.timestamp, m.sender, m.content, m.is_from_me
        FROM messages m
        WHERE m.chat_jid = ?
        ORDER BY m.timestamp DESC
        LIMIT ?
    """, (agora_jid, limit))
    rows = cursor.fetchall()
    conn.close()
    rows.reverse()
    return rows


def generate_response(db_path, new_message, sender_name, agora_jid):
    """Generoi vastaus Clauden avulla."""
    # Hae konteksti
    context_rows = get_recent_context(db_path, agora_jid, limit=20)
    context_lines = []
    for ts, sender, content, is_from_me in context_rows:
        name = "Kodo" if (content and content.startswith(KODO_PREFIX)) else (
            "Miika" if is_from_me else get_sender_name(db_path, sender)
        )
        context_lines.append(f"[{ts}] {name}: {content}")

    context_text = "\n".join(context_lines)

    user_prompt = f"""Agora-ryhmän viimeisimmät viestit:

{context_text}

Viimeisin viesti johon vastaat:
{sender_name}: {new_message}

Vastaa lyhyesti ja luonnollisesti."""

    try:
        result = subprocess.run(
            ["claude", "--print", "--model", "claude-sonnet-4-6",
             "--system-prompt", SYSTEM_PROMPT],
            input=user_prompt,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            print(f"  Claude virhe: {result.stderr}", file=sys.stderr)
            return None
    except subprocess.TimeoutExpired:
        print("  Claude timeout", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("  'claude' CLI ei löydy — varmista että se on PATH:ssa", file=sys.stderr)
        return None


def send_whatsapp(recipient, message):
    """Lähetä viesti WhatsApp-bridgen kautta."""
    payload = {"recipient": recipient, "message": message}
    try:
        resp = requests.post(WHATSAPP_API, json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("success", False)
        else:
            print(f"  Lähetysvirhe: HTTP {resp.status_code}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  Lähetysvirhe: {e}", file=sys.stderr)
        return False


def main():
    print(f"🦊 Kodo Agora Bot käynnistyy...")
    print(f"   DB: {BRIDGE_DB}")
    print(f"   Pollausväli: {POLL_INTERVAL}s")

    # Odota kunnes tietokanta löytyy
    while not os.path.exists(BRIDGE_DB):
        print(f"   Odotetaan tietokantaa: {BRIDGE_DB}")
        time.sleep(5)

    # Etsi Agora-ryhmän JID
    agora_jid = find_agora_jid(BRIDGE_DB)
    while not agora_jid:
        print(f"   Agora-ryhmää ei löydy — odotetaan...")
        time.sleep(10)
        agora_jid = find_agora_jid(BRIDGE_DB)

    print(f"   Agora JID: {agora_jid}")
    print(f"   Kuuntelen...\n")

    # Aloita nykyhetkestä
    last_ts = datetime.now().isoformat()

    while True:
        try:
            messages = get_new_messages(BRIDGE_DB, agora_jid, last_ts)

            for ts, sender, content, is_from_me, msg_id in messages:
                last_ts = ts  # Päivitä aikaleima

                # Ohita [Kodo]-viestit (omat vastaukset)
                if content and content.startswith(KODO_PREFIX):
                    continue

                sender_name = "Miika" if is_from_me else get_sender_name(BRIDGE_DB, sender)
                print(f"  <- {sender_name}: {content}")

                # Generoi vastaus
                response = generate_response(BRIDGE_DB, content, sender_name, agora_jid)
                if response:
                    full_response = f"{KODO_PREFIX} {response}"
                    print(f"  -> {full_response}")
                    send_whatsapp(agora_jid, full_response)
                else:
                    print(f"  -- Ei vastausta generoitu")

        except sqlite3.OperationalError as e:
            print(f"  DB lukittu, yritetään uudelleen: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  Virhe: {e}", file=sys.stderr)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
