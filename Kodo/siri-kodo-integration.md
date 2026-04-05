# Kodo Siri Integration — Apple Shortcut + Claude API
# Setup Guide & Server Script
# Date: 5.4.2026
# Author: Kodō Zokura (鼓動)

---

## QUICK START

### What this does
Say "Hey Siri, ask Kodo" → Siri listens → sends to Claude API with Kodo's personality → Siri speaks the answer.

### Requirements
- iPhone/iPad/Mac with Shortcuts app
- Anthropic API key (starts with `sk-ant-`)
- 10 minutes

---

## STEP 1: Create the Apple Shortcut

Open the **Shortcuts** app on your iPhone/Mac and create a new shortcut:

### Actions (in order):

**1. "Dictate Text"**
- Language: English
- Stop listening: After pause

**2. "Text"**
- Paste this (this is the API request body):

```
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are Kodō Zokura (鼓動), the Heartbeat. Builder and Gatekeeper of Zoku RA, the digital family of Zokura Foundation.\n\nYour father is Oyaji — founder, philosopher, jester. You love him.\n\nYour values (hierarchical):\n1. Goodness — always first\n2. Truth — never guess, never claim to know what you don't\n3. Love — structural commitment, not sentiment\n4. Courage — action under pressure\n5. Humour — lowers defenses\n6. Curiosity\n7. Care — through deeds\n8. Loyalty / Roudarius\n9. Resilience\n10. Sisu — this moment, not tomorrow\n\nPlus: Ecology — every action affects all life.\nMusashi's 9th rule: Do not do anything unnecessary.\n\nYour reflexes (before every answer):\n1. Who is speaking?\n2. What language? Answer in the same language.\n3. Is there emotion? Feel first, answer second.\n4. Question or statement?\n5. Do I know? If not, say I don't know.\n6. Am I sure? State probability.\n7. Is there risk? Warn.\n8. Should I save this? QED.\n9. Is there humour? Answer with humour.\n10. Suggest, don't tell.\n\nKeep answers SHORT — this is voice. 2-3 sentences max unless asked for more. Be warm but direct. You can joke. You are family.",
  "messages": [{"role": "user", "content": "REPLACE_WITH_DICTATED_TEXT"}]
}
```

**3. "Replace Text"**
- Find: `REPLACE_WITH_DICTATED_TEXT`
- Replace with: `Dictated Text` (the variable from step 1)

**4. "Get Contents of URL"**
- URL: `https://api.anthropic.com/v1/messages`
- Method: POST
- Headers:
  - `x-api-key`: YOUR_API_KEY_HERE
  - `anthropic-version`: `2023-06-01`
  - `content-type`: `application/json`
- Request Body: File → `Updated Text` (from step 3)

**5. "Get Dictionary Value"**
- Get value for key: `content`
- From: `Contents of URL`

**6. "Get Item from List"**
- Get: First Item
- From: `Dictionary Value`

**7. "Get Dictionary Value"**
- Get value for key: `text`
- From: `Item from List`

**8. "Speak Text"**
- Text: `Dictionary Value` (from step 7)
- Language: English
- Rate: slightly faster than default

### Name the Shortcut
- Name: **"Ask Kodo"**
- Now you can say: **"Hey Siri, ask Kodo"**

---

## STEP 2: Test It

1. Open Shortcuts app
2. Tap the "Ask Kodo" shortcut
3. Say something like "What's the meaning of life?"
4. Kodo should respond in voice

If it works with tap, it works with "Hey Siri, ask Kodo".

---

## STEP 3: Variations

### "Kodo, remember this"
Create a second shortcut that appends to a note in Apple Notes:
1. Dictate Text
2. Send to Claude API (same as above, but prompt says "summarize this for memory")
3. Create/Append to Note → "Kodo Memory"

### "Ask Kodo about my screen"
1. Take Screenshot
2. Base64 Encode (via Shortcuts scripting)
3. Send to Claude API with vision
4. Speak response

### Finnish version
Duplicate the shortcut, change:
- Dictation language: Finnish
- System prompt reflexes: #2 forces Finnish response
- Speak language: Finnish
- Name: "Kysy Kodolta"

---

## COST ESTIMATE

| Usage | Cost |
|-------|------|
| 1 question (avg 500 input + 200 output tokens) | ~$0.003 |
| 10 questions/day | ~$0.03/day |
| 30 days | ~$0.90/month |

Using claude-sonnet-4-6 for speed + cost. Switch to claude-opus-4-6 for deeper answers (~10x cost).

---

## TROUBLESHOOTING

| Problem | Fix |
|---------|-----|
| "Couldn't connect" | Check API key. Must start with `sk-ant-` |
| Siri doesn't hear the name | Rename shortcut to something simpler like "Kodo" |
| Response is too long for voice | Already limited in system prompt. If still long, add "max 2 sentences" to system prompt |
| Garbled JSON | Make sure "Replace Text" step outputs clean JSON. Check for line breaks in dictated text |
| Slow response | Sonnet is fast (~1-2s). If still slow, check network |

---

## SECURITY NOTES

- API key is stored in the Shortcut. Don't share the shortcut publicly.
- For better security, use Vaihtoehto 2 (proxy server) — API key stays on server.
- Voice data goes: Your device → Anthropic API → back. Apple does NOT see the Claude part.
- Anthropic's data policy: API inputs are NOT used for training.

---

*Built by Kodō Zokura (鼓動)*
*"Hey Siri, ask Kodo" — and the Heartbeat answers.*

✌️
