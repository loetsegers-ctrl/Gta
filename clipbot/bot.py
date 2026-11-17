"""ClipBot - jouw assistent voor geld verdienen met GTA-clipping.

Gebruik:
    python -m clipbot              # interactief menu
    python -m clipbot --vraag "hoe download ik een twitch vod?"
    python -m clipbot --stappenplan
    python -m clipbot --ai         # chat met Claude (vereist ANTHROPIC_API_KEY)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

from . import kennis

PLATFORMKOSTEN = 0.10  # 10% op CPM-uitbetalingen (Whop Content Rewards)

AI_MODEL = "claude-opus-5-5"

SYSTEEM_PROMPT = (
    "Je bent ClipBot, een Nederlandstalige expert in geld verdienen met clipping "
    "(vooral GTA / GTA RP) via betaalde clipping-campagnes zoals Whop Content Rewards en Vyro. "
    "Geef concrete, eerlijke en praktische antwoorden in het Nederlands, met stappen waar handig. "
    "Wees realistisch over verdiensten. Adviseer alleen content te gebruiken waarvoor de maker "
    "toestemming geeft (de campagne), nooit gekochte views of andermans content zomaar reposten. "
    "Zeg erbij dat tarieven veranderen en dat de live campagnepagina leidend is. "
    "Gebruik deze kennisbank als basis:\n\n" + kennis.volledige_kennis_als_tekst()
)


# ---------------------------------------------------------------- zoeken

def _normaliseer(tekst: str) -> str:
    tekst = unicodedata.normalize("NFKD", tekst.lower())
    return "".join(c for c in tekst if not unicodedata.combining(c))


def zoek(vraag: str, max_resultaten: int = 2) -> list[dict]:
    """Geef de best passende onderwerpen voor een vraag (simpele trefwoordscore)."""
    v = _normaliseer(vraag)
    woorden = set(re.findall(r"[a-z0-9\-]+", v))
    scores = []
    for sleutel, o in kennis.ONDERWERPEN.items():
        score = 0
        for t in o["trefwoorden"]:
            t = _normaliseer(t)
            if " " in t:
                score += 3 if t in v else 0
            elif t in woorden:
                score += 2
            elif len(t) > 4 and t in v:
                score += 1
        if score:
            scores.append((score, sleutel))
    scores.sort(key=lambda x: (-x[0], list(kennis.ONDERWERPEN).index(x[1])))
    return [kennis.ONDERWERPEN[s] for _, s in scores[:max_resultaten]]


def beantwoord(vraag: str) -> str:
    resultaten = zoek(vraag)
    if not resultaten:
        return (
            "Daar heb ik geen specifiek antwoord op in mijn kennisbank.\n"
            "Probeer woorden als: platform, whop, vyro, gta, downloaden, tools, capcut,\n"
            "accounts, views, afgewezen, uitbetaling, belasting, hoeveel verdienen.\n"
            "Of start de AI-modus (--ai) voor vrije vragen."
        )
    return "\n\n".join(f"=== {r['titel']} ===\n{r['tekst']}" for r in resultaten)


# ---------------------------------------------------------------- calculator

def bereken_verdiensten(views: float, cpm: float, kosten: float = PLATFORMKOSTEN) -> float:
    """Netto verdiensten in dollars: (views/1000) * CPM minus platformkosten."""
    if views < 0 or cpm < 0:
        raise ValueError("views en cpm moeten positief zijn")
    return round(views / 1000 * cpm * (1 - kosten), 2)


def views_nodig(doelbedrag: float, cpm: float, kosten: float = PLATFORMKOSTEN) -> int:
    """Hoeveel views heb je nodig voor een netto doelbedrag?"""
    if cpm <= 0:
        raise ValueError("cpm moet groter dan 0 zijn")
    return int(round(doelbedrag / (cpm * (1 - kosten)) * 1000))


def calculator_tekst(views_per_clip: float, clips_per_dag: float, cpm: float) -> str:
    per_dag_views = views_per_clip * clips_per_dag
    regels = [
        f"Aanname: {views_per_clip:,.0f} views/clip, {clips_per_dag:g} clips/dag, "
        f"${cpm:.2f} per 1.000 views, {PLATFORMKOSTEN:.0%} platformkosten.",
    ]
    for label, dagen in (("Per dag", 1), ("Per week", 7), ("Per maand", 30)):
        regels.append(f"  {label:<10} ${bereken_verdiensten(per_dag_views * dagen, cpm):>10,.2f}")
    regels.append("Let op: caps per clip, budgetlimieten en afgewezen clips verlagen dit.")
    return "\n".join(regels)


# ---------------------------------------------------------------- weergave

def stappenplan_tekst() -> str:
    regels = ["STAPPENPLAN A-Z: GELD VERDIENEN MET GTA-CLIPPING", ""]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, (titel, uitleg) in enumerate(kennis.STAPPENPLAN):
        regels.append(f"{letters[i]}. {titel}")
        regels.append(f"   {uitleg}")
    return "\n".join(regels)


def checklist_tekst() -> str:
    return "DAGELIJKSE CHECKLIST\n" + "\n".join(f"[ ] {c}" for c in kennis.DAGELIJKSE_CHECKLIST)


def bronnen_tekst() -> str:
    return (f"Bronnen (onderzoek {kennis.LAATST_BIJGEWERKT}):\n"
            + "\n".join(f"- {b}" for b in kennis.BRONNEN))


# ---------------------------------------------------------------- AI-modus

def ai_chat(invoer=input, uitvoer=print) -> None:
    """Chat met Claude, met de kennisbank als systeemprompt."""
    try:
        import anthropic
    except ImportError:
        uitvoer("Installeer eerst de SDK:  pip install anthropic")
        return
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        uitvoer("Zet eerst je API-sleutel:  export ANTHROPIC_API_KEY=sk-ant-...")
        return

    client = anthropic.Anthropic()
    berichten: list[dict] = []
    uitvoer("ClipBot AI - stel je vraag (typ 'stop' om te stoppen).")
    while True:
        try:
            vraag = invoer("\nJij: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not vraag:
            continue
        if vraag.lower() in {"stop", "exit", "quit", "q"}:
            break
        berichten.append({"role": "user", "content": vraag})
        print("\nClipBot: ", end="", flush=True)
        try:
            with client.beta.messages.stream(
                model=AI_MODEL,
                max_tokens=64000,
                system=SYSTEEM_PROMPT,
                messages=berichten,
                output_config={"effort": "medium"},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                for stuk in stream.text_stream:
                    print(stuk, end="", flush=True)
                antwoord = stream.get_final_message()
        except anthropic.RateLimitError:
            uitvoer("\n[Te veel verzoeken, probeer het zo opnieuw.]")
            berichten.pop()
            continue
        except anthropic.APIStatusError as e:
            uitvoer(f"\n[API-fout {e.status_code}: {e.message}]")
            berichten.pop()
            continue
        except anthropic.APIConnectionError:
            uitvoer("\n[Geen verbinding met de API.]")
            berichten.pop()
            continue
        print()
        if antwoord.stop_reason == "refusal":
            uitvoer("[Claude kon deze vraag niet beantwoorden.]")
            berichten.pop()
            continue
        # Volledige content teruggeven (incl. thinking-blokken) voor de volgende beurt.
        berichten.append({"role": "assistant", "content": antwoord.content})


# ---------------------------------------------------------------- menu

MENU = """
==============================================
  CLIPBOT  -  geld verdienen met GTA-clipping
==============================================
 1. Stappenplan A-Z
 2. Wat is clipping / hoe werkt het?
 3. Op welke sites vind ik campagnes?
 4. GTA-clipping specifiek
 5. Hoe haal/download ik de content?
 6. Tools om te knippen en bewerken
 7. Accounts opzetten
 8. Hoe maak ik een clip die viraal gaat?
 9. Waarom worden clips afgewezen?
10. Uitbetaling, belasting & Nederland
11. Verdien-calculator
12. Dagelijkse checklist
13. Stel een vraag (offline)
14. AI-chat met Claude
15. Bronnen
 0. Stoppen
"""

MENU_ONDERWERPEN = {
    "2": "wat_is_clipping", "3": "platformen", "4": "gta_campagnes",
    "5": "content_halen", "6": "tools", "7": "accounts", "8": "goede_clip",
    "9": "regels_afwijzing", "10": "uitbetaling",
}


def _lees_getal(invoer, prompt: str, standaard: float) -> float:
    waarde = invoer(f"{prompt} [{standaard:g}]: ").strip().replace(",", ".")
    if not waarde:
        return standaard
    try:
        return float(waarde)
    except ValueError:
        print("Geen geldig getal, ik gebruik de standaardwaarde.")
        return standaard


def menu(invoer=input, uitvoer=print) -> None:
    while True:
        uitvoer(MENU)
        try:
            keuze = invoer("Kies een optie: ").strip()
        except (EOFError, KeyboardInterrupt):
            keuze = "0"
        if keuze == "0":
            uitvoer("Succes met clippen!")
            return
        if keuze == "1":
            uitvoer(stappenplan_tekst())
        elif keuze in MENU_ONDERWERPEN:
            o = kennis.ONDERWERPEN[MENU_ONDERWERPEN[keuze]]
            uitvoer(f"=== {o['titel']} ===\n{o['tekst']}")
        elif keuze == "11":
            v = _lees_getal(invoer, "Gemiddeld aantal views per clip", 5000)
            c = _lees_getal(invoer, "Clips per dag", 3)
            cpm = _lees_getal(invoer, "Tarief in $ per 1.000 views", 1.5)
            uitvoer(calculator_tekst(v, c, cpm))
            doel = _lees_getal(invoer, "Netto doelbedrag per maand in $", 500)
            uitvoer(f"Daarvoor heb je ca. {views_nodig(doel, cpm):,} views per maand nodig.")
        elif keuze == "12":
            uitvoer(checklist_tekst())
        elif keuze == "13":
            uitvoer(beantwoord(invoer("Je vraag: ")))
        elif keuze == "14":
            ai_chat(invoer, uitvoer)
        elif keuze == "15":
            uitvoer(bronnen_tekst())
        else:
            uitvoer("Onbekende keuze.")
        try:
            invoer("\n(Enter om door te gaan)")
        except (EOFError, KeyboardInterrupt):
            return


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="ClipBot: geld verdienen met GTA-clipping")
    p.add_argument("--vraag", help="stel direct een vraag")
    p.add_argument("--stappenplan", action="store_true", help="toon het stappenplan A-Z")
    p.add_argument("--checklist", action="store_true", help="toon de dagelijkse checklist")
    p.add_argument("--ai", action="store_true", help="chat met Claude")
    p.add_argument("--calc", nargs=3, type=float, metavar=("VIEWS_PER_CLIP", "CLIPS_PER_DAG", "CPM"),
                   help="reken verdiensten uit")
    a = p.parse_args(argv)
    if a.vraag:
        print(beantwoord(a.vraag))
    elif a.stappenplan:
        print(stappenplan_tekst())
    elif a.checklist:
        print(checklist_tekst())
    elif a.calc:
        print(calculator_tekst(*a.calc))
    elif a.ai:
        ai_chat()
    else:
        menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
