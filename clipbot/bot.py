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


# ---------------------------------------------------------------- campagne-checker

def campagne_score(cpm: float, budget: float, clippers: int, goedkeuring: float = 50.0) -> float:
    """Vergelijkingsscore: CPM x resterend budget x goedkeuring% / aantal clippers."""
    if min(cpm, budget, goedkeuring) < 0 or clippers < 0:
        raise ValueError("waarden moeten positief zijn")
    return round(cpm * budget * (goedkeuring / 100) / max(clippers, 1), 2)


def campagne_advies(cpm: float, budget: float, clippers: int, goedkeuring: float = 50.0,
                    cap: float | None = None, verwachte_views: float = 10_000) -> str:
    score = campagne_score(cpm, budget, clippers, goedkeuring)
    regels = [f"Score: {score:,.2f}  (hoger = beter; vergelijk campagnes onderling)"]
    if budget < 500:
        regels.append("- Let op: klein resterend budget; je views worden mogelijk niet meer betaald.")
    if goedkeuring < 30:
        regels.append("- Lage goedkeuring: lees de regels extra goed of kies een andere campagne.")
    if cpm < 0.75:
        regels.append("- Laag tarief (mediaan is ca. $1,09 per 1.000 views).")
    per_clip = bereken_verdiensten(verwachte_views, cpm)
    if cap is not None and per_clip > cap:
        regels.append(f"- Cap bereikt: bij {verwachte_views:,.0f} views krijg je max ${cap:,.2f} per clip.")
        per_clip = cap
    regels.append(f"Verwacht per clip bij {verwachte_views:,.0f} views: ca. ${per_clip:,.2f}")
    if len(regels) == 2:
        regels.insert(1, "- Ziet er gezond uit.")
    return "\n".join(regels)


# ---------------------------------------------------------------- hooks

def hooks_en_caption(streamer: str, platform: str = "Twitch", aantal: int = 5) -> str:
    streamer = streamer.strip() or "deze streamer"
    tag = re.sub(r"[^a-z0-9]", "", _normaliseer(streamer)) or "streamer"
    hooks = [h.format(streamer=streamer) for h in kennis.HOOK_SJABLONEN[:aantal]]
    caption = kennis.CAPTION_SJABLOON.format(hook=hooks[0], streamer=streamer.replace(" ", ""),
                                             platform=platform, streamer_tag=tag)
    return ("HOOK-IDEEËN (tekst bovenin je clip):\n"
            + "\n".join(f"  {i}. {h}" for i, h in enumerate(hooks, 1))
            + "\n\nVOORBEELD-CAPTION:\n" + caption
            + "\n\nCheck altijd welke tag/hashtags de campagne verplicht stelt.")


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


def markdown_export() -> str:
    """Het complete stappenplan + alle kennis als Markdown-document."""
    d = ["# Geld verdienen met GTA-clipping: stappenplan A-Z", "",
         f"_Gegenereerd door ClipBot uit de kennisbank (onderzoek {kennis.LAATST_BIJGEWERKT}). "
         "Tarieven en voorwaarden veranderen; de live campagnepagina is leidend._", "",
         "## Stappenplan", ""]
    for i, (titel, uitleg) in enumerate(kennis.STAPPENPLAN):
        d.append(f"**{chr(65 + i)}. {titel}**  ")
        d.append(f"{uitleg}")
        d.append("")
    d += ["## Dagelijkse checklist", ""] + [f"- [ ] {c}" for c in kennis.DAGELIJKSE_CHECKLIST] + [""]
    for o in kennis.ONDERWERPEN.values():
        d += [f"## {o['titel']}", "", "```text", o["tekst"], "```", ""]
    d += ["## Hook-ideeën", ""] + [f"- {h.format(streamer='<streamer>')}" for h in kennis.HOOK_SJABLONEN] + [""]
    d += ["## Bronnen", ""] + [f"- <{b}>" for b in kennis.BRONNEN] + [""]
    return "\n".join(d)


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
 5. GTA 6: waarom NU starten?
 6. Hoe haal/download ik de content?
 7. Tools om te knippen en bewerken
 8. Accounts opzetten
 9. Hoe maak ik een clip die viraal gaat?
10. Hoe kies ik een goede campagne?
11. Waarom worden clips afgewezen?
12. Scams herkennen
13. Uitbetaling, belasting & Nederland
14. Hoeveel kan ik verdienen?
15. Verdien-calculator
16. Campagne-checker
17. Hook- & caption-generator
18. Dagelijkse checklist
19. Stel een vraag (offline)
20. AI-chat met Claude
21. Bronnen
 0. Stoppen
"""

MENU_ONDERWERPEN = {
    "2": "wat_is_clipping", "3": "platformen", "4": "gta_campagnes", "5": "gta6_kans",
    "6": "content_halen", "7": "tools", "8": "accounts", "9": "goede_clip",
    "10": "campagne_kiezen", "11": "regels_afwijzing", "12": "scams",
    "13": "uitbetaling", "14": "verwachtingen",
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
        elif keuze == "15":
            v = _lees_getal(invoer, "Gemiddeld aantal views per clip", 5000)
            c = _lees_getal(invoer, "Clips per dag", 3)
            cpm = _lees_getal(invoer, "Tarief in $ per 1.000 views", 1.5)
            uitvoer(calculator_tekst(v, c, cpm))
            doel = _lees_getal(invoer, "Netto doelbedrag per maand in $", 500)
            uitvoer(f"Daarvoor heb je ca. {views_nodig(doel, cpm):,} views per maand nodig.")
        elif keuze == "16":
            cpm = _lees_getal(invoer, "Tarief in $ per 1.000 views", 1.5)
            budget = _lees_getal(invoer, "Resterend budget in $", 5000)
            clippers = int(_lees_getal(invoer, "Aantal clippers dat al meedoet", 100))
            goed = _lees_getal(invoer, "Goedkeuringspercentage (schatting)", 50)
            cap = _lees_getal(invoer, "Max uitbetaling per clip in $ (0 = geen)", 0)
            uitvoer(campagne_advies(cpm, budget, clippers, goed, cap or None))
        elif keuze == "17":
            naam = invoer("Naam van de streamer: ")
            plat = invoer("Platform van de streamer [Twitch]: ").strip() or "Twitch"
            uitvoer(hooks_en_caption(naam, plat))
        elif keuze == "18":
            uitvoer(checklist_tekst())
        elif keuze == "19":
            uitvoer(beantwoord(invoer("Je vraag: ")))
        elif keuze == "20":
            ai_chat(invoer, uitvoer)
        elif keuze == "21":
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
    p.add_argument("--hooks", metavar="STREAMER", help="hook- en caption-ideeën voor een streamer")
    p.add_argument("--campagne", nargs=4, type=float, metavar=("CPM", "BUDGET", "CLIPPERS", "GOEDKEURING"),
                   help="beoordeel een campagne")
    p.add_argument("--export", metavar="BESTAND", help="schrijf stappenplan + kennis naar een Markdown-bestand")
    a = p.parse_args(argv)
    if a.vraag:
        print(beantwoord(a.vraag))
    elif a.stappenplan:
        print(stappenplan_tekst())
    elif a.checklist:
        print(checklist_tekst())
    elif a.calc:
        print(calculator_tekst(*a.calc))
    elif a.export:
        with open(a.export, "w", encoding="utf-8") as f:
            f.write(markdown_export())
        print(f"Geschreven: {a.export}")
    elif a.hooks:
        print(hooks_en_caption(a.hooks))
    elif a.campagne:
        cpm, budget, clippers, goed = a.campagne
        print(campagne_advies(cpm, budget, int(clippers), goed))
    elif a.ai:
        ai_chat()
    else:
        menu()
    return 0


if __name__ == "__main__":
    sys.exit(main())
