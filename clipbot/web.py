"""Bouwt web/clipbot.html uit de kennisbank (python -m clipbot.web)."""

from __future__ import annotations

import json
from pathlib import Path

from . import kennis
from .bot import PLATFORMKOSTEN

SJABLOON = Path(__file__).with_name("web_sjabloon.html")
UITVOER = Path(__file__).resolve().parent.parent / "web" / "clipbot.html"


def bouw(pad: Path = UITVOER) -> Path:
    data = {
        "bijgewerkt": kennis.LAATST_BIJGEWERKT,
        "onderwerpen": kennis.ONDERWERPEN,
        "stappenplan": kennis.STAPPENPLAN,
        "checklist": kennis.DAGELIJKSE_CHECKLIST,
        "bronnen": kennis.BRONNEN,
        "kosten": PLATFORMKOSTEN,
        "hooks": kennis.HOOK_SJABLONEN,
    }
    # '</' escapen zodat tekst nooit de script-tag kan sluiten.
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = SJABLOON.read_text(encoding="utf-8").replace("/*__DATA__*/null", blob)
    pad.parent.mkdir(parents=True, exist_ok=True)
    pad.write_text(html, encoding="utf-8")
    return pad


if __name__ == "__main__":
    print(f"Geschreven: {bouw()}")
