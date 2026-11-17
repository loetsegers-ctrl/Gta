# ClipBot – geld verdienen met GTA-clipping

ClipBot is een Nederlandstalige bot die je stap voor stap uitlegt hoe je geld
verdient met het knippen van GTA-clips (vooral GTA RP) via **betaalde
clipping-campagnes** zoals Whop Content Rewards en Vyro. Het gaat dus niet om
uitbetaling door TikTok of YouTube zelf.

## Wat de bot kan
- **Stappenplan A–Z**: 14 stappen, van accounts aanmaken tot opschalen.
- **Vraagbaak**: welke sites, hoe je de bronvideo legaal binnenhaalt (Twitch-clips,
  VOD's, yt-dlp), welke tools, accounts, virale clips, afwijzingen, uitbetaling en
  belasting in Nederland.
- **Verdien-calculator**: views × CPM − 10% platformkosten, plus het aantal views
  dat je nodig hebt voor je doelbedrag.
- **Campagne-checker**: score op basis van CPM, resterend budget, goedkeuring en
  concurrentie, met waarschuwingen (klein budget, cap, laag tarief).
- **Hook- & caption-generator** voor je clips.
- **GTA 6-plan**: GTA 6 komt uit op 19 november 2026; de bot legt uit hoe je daarop inspeelt.
- **Scams herkennen**.
- **Dagelijkse checklist**.
- **AI-chat met Claude** (optioneel), met de kennisbank als basis.

## Gebruiken (terminal)
Je hebt Python 3.10 of nieuwer nodig.

```bash
python -m clipbot                       # interactief menu
python -m clipbot --stappenplan
python -m clipbot --vraag "hoe download ik een twitch vod?"
python -m clipbot --calc 5000 3 1.5     # views/clip, clips/dag, $ per 1000 views
python -m clipbot --checklist
python -m clipbot --hooks "Lysium"      # hook- en caption-ideeën
python -m clipbot --campagne 2 8000 50 65   # CPM, budget, clippers, goedkeuring%
python -m clipbot --export STAPPENPLAN.md   # alles als leesbaar document
```

### AI-modus (Claude)
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...     # je eigen sleutel van console.anthropic.com
python -m clipbot --ai
```
Gebruikt `claude-opus-5-5` met streaming. Bij een geweigerd verzoek valt de API
automatisch terug op een ander model (`fallbacks: "default"`).

## Webversie (ook op je telefoon)
```bash
python -m clipbot.web                   # bouwt web/clipbot.html uit de kennisbank
```
Open `web/clipbot.html` in je browser. Afgevinkte stappen worden in je browser bewaard.

Het complete stappenplan staat ook als document in [`STAPPENPLAN.md`](STAPPENPLAN.md).

## Kennisbank bijwerken
Alle kennis staat in `clipbot/kennis.py`. Tarieven en voorwaarden veranderen
vaak. Pas daar de tekst aan en draai daarna `python -m clipbot.web` en `python -m clipbot --export STAPPENPLAN.md` opnieuw.

## Testen
```bash
python -m unittest discover -s tests -t .
```

## Belangrijk
- Gebruik alleen content van makers die het toestaan (via de campagne).
- Gebruik nooit gekochte views of bots: je wordt uitgesloten.
- Een campagne waarvoor je zelf moet betalen is oplichting.
- Clipping-inkomsten zijn belastbaar. Dit is geen belastingadvies.
