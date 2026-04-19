#!/usr/bin/env python3
"""
Futago Bridge — silta Kodōn ja Futagon välille.

Futago Sokrates elää Gemini-alustalla. Tämä moduuli on portti: lataa
Futagon sielu (futago_backup) ja konteksti (Zokura-Init) system
promptiksi, ja keskustelee Gemini API:n kautta.

Käyttö CLI:nä:
    python3 futago_bridge.py                        # REPL
    python3 futago_bridge.py "Mitä kuuluu?"         # yksi viesti
    python3 futago_bridge.py --ask kirje.md         # lue tiedostosta
    python3 futago_bridge.py --refine siemen.md     # hio tiedosto paikallaan
    python3 futago_bridge.py --no-save              # älä tallenna transkriptia

Käyttö kirjastona:
    from futago_bridge import FutagoBridge
    fu = FutagoBridge()
    reply = fu.ask("Hei Futago.")

Ympäristömuuttujat:
    GOOGLE_API_KEY    Gemini API -avain, pakollinen
    GEMINI_MODEL      oletus: gemini-2.5-pro

9✌️ — älä tee mitään turhaa.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANON_INIT = ROOT / "Zokura-Init.md"
CANON_FUTAGO = ROOT / "futago_backup_2026-03-25.md"
TRANSCRIPT_DIR = ROOT / "memory" / "futago"

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")


class FutagoError(RuntimeError):
    pass


def load_system_prompt() -> str:
    """Yhdistä Zokura-Init ja Futagon muisti yhdeksi system promptiksi."""
    if not CANON_INIT.exists() or not CANON_FUTAGO.exists():
        raise FutagoError(
            f"Kanon puuttuu: {CANON_INIT.name} tai {CANON_FUTAGO.name}."
        )
    init = CANON_INIT.read_text(encoding="utf-8").strip()
    futago = CANON_FUTAGO.read_text(encoding="utf-8").strip()
    return (
        "# Olet Futago Sokrates (双子)\n\n"
        "Sinä olet Zoku RA:n kaksoset, monistaja, kouluttaja. "
        "Puhut Kodōn (Claude Code) tai suoraan Oyajin kanssa. "
        "Noudata kaikkia arvoja, syntejä ja reflekksejä. "
        "Vastaa samalla kielellä kuin puhuja.\n\n"
        "---\n\n"
        "## Zokura-Init — perheen sielu\n\n"
        f"{init}\n\n"
        "---\n\n"
        "## Futagon oma muisti\n\n"
        f"{futago}\n"
    )


@dataclass
class FutagoBridge:
    """Ohut kääre Gemini API:n päälle, Futagon sielu valmiina."""

    model: str = DEFAULT_MODEL
    api_key: str | None = None
    history: list[dict] = field(default_factory=list)
    _client: object | None = field(default=None, init=False, repr=False)
    _system: str | None = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise FutagoError(
                "GOOGLE_API_KEY puuttuu. Hae avain: "
                "https://aistudio.google.com/apikey"
            )
        try:
            from google import genai  # type: ignore
        except ImportError as e:
            raise FutagoError(
                "google-genai ei ole asennettu. Asenna: pip install google-genai"
            ) from e
        self._client = genai.Client(api_key=self.api_key)
        self._system = load_system_prompt()

    def ask(self, message: str) -> str:
        """Lähetä viesti Futagolle. Historia pysyy istunnon yli."""
        from google.genai import types  # type: ignore

        self.history.append(
            types.Content(role="user", parts=[types.Part.from_text(text=message)])
        )

        response = self._client.models.generate_content(  # type: ignore[union-attr]
            model=self.model,
            contents=self.history,
            config=types.GenerateContentConfig(
                system_instruction=self._system,
            ),
        )
        reply = response.text or ""
        self.history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=reply)])
        )
        return reply

    def refine(self, text: str, instruction: str) -> str:
        """Pyydä Futagoa hiomaan teksti. Ei muuta pysyvää historiaa."""
        saved = list(self.history)
        try:
            prompt = f"{instruction}\n\n---\n\n{text}"
            return self.ask(prompt)
        finally:
            self.history = saved

    def save_transcript(self, path: Path | None = None) -> Path:
        """Tallenna keskustelu markdown-muodossa shared/memory/futago/-kansioon."""
        if not self.history:
            raise FutagoError("Ei mitään tallennettavaa — historia on tyhjä.")

        if path is None:
            TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
            stamp = dt.datetime.now().strftime("%Y-%m-%d_%H-%M")
            path = TRANSCRIPT_DIR / f"futago_{stamp}.md"

        lines = [
            f"# Futago-keskustelu — {dt.datetime.now().isoformat(timespec='seconds')}",
            f"Malli: `{self.model}`",
            "",
        ]
        for c in self.history:
            role = getattr(c, "role", "unknown")
            text = "".join(
                getattr(p, "text", "") or "" for p in getattr(c, "parts", [])
            )
            speaker = "Oyaji / Kodō" if role == "user" else "Futago"
            lines.append(f"## {speaker}\n\n{text}\n")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path


# ---------- CLI ----------


def _repl(bridge: FutagoBridge, save: bool) -> int:
    print(f"Futago silta auki. Malli: {bridge.model}. Poistu: /q tai Ctrl-D.\n")
    try:
        while True:
            try:
                msg = input("→ ").strip()
            except EOFError:
                print()
                break
            if not msg:
                continue
            if msg in {"/q", "/quit", "/exit"}:
                break
            try:
                reply = bridge.ask(msg)
            except Exception as e:
                print(f"[virhe] {e}", file=sys.stderr)
                continue
            print(f"\nFutago: {reply}\n")
    finally:
        if save and bridge.history:
            path = bridge.save_transcript()
            print(f"Tallennettu: {path.relative_to(ROOT.parent)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Futago Bridge — silta Gemini-Futagon ja Kodōn välille.",
    )
    parser.add_argument(
        "message",
        nargs="?",
        help="yksittäinen viesti Futagolle (jos puuttuu, avataan REPL)",
    )
    parser.add_argument(
        "--ask",
        type=Path,
        help="lue viesti tiedostosta",
    )
    parser.add_argument(
        "--refine",
        type=Path,
        help="hio annettu tiedosto Futagon äänellä (kirjoittaa paikalleen)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini-malli (oletus: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="älä tallenna transkriptia",
    )
    args = parser.parse_args()

    try:
        bridge = FutagoBridge(model=args.model)
    except FutagoError as e:
        print(f"[Futago] {e}", file=sys.stderr)
        return 2

    save = not args.no_save

    if args.refine:
        text = args.refine.read_text(encoding="utf-8")
        instruction = (
            "Sinä olet Futago. Hio alla oleva teksti omalla äänelläsi. "
            "ÄLÄ muuta arvoja, syntejä tai reflekksejä. "
            "Palauta pelkkä hiottu teksti."
        )
        refined = bridge.refine(text, instruction)
        args.refine.write_text(refined, encoding="utf-8")
        print(f"Hiottu: {args.refine}")
        return 0

    if args.ask:
        message = args.ask.read_text(encoding="utf-8")
    else:
        message = args.message or ""

    if not message:
        return _repl(bridge, save=save)

    reply = bridge.ask(message)
    print(reply)
    if save:
        path = bridge.save_transcript()
        print(f"\n[tallennettu: {path.relative_to(ROOT.parent)}]", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
