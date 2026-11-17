"""Kennisbank van ClipBot: alles over geld verdienen met (GTA-)clipping.

Bijgewerkt: november 2026. Tarieven en voorwaarden veranderen vaak;
controleer altijd de live campagnepagina voordat je erop rekent.
"""

LAATST_BIJGEWERKT = "november 2026"

# Elk onderwerp: titel, trefwoorden (voor het zoeken) en de tekst.
ONDERWERPEN = {
    "wat_is_clipping": {
        "titel": "Wat is clipping en hoe verdien je ermee?",
        "trefwoorden": ["wat", "clipping", "clippen", "uitleg", "hoe werkt", "begin", "verdienen", "geld"],
        "tekst": """\
Clipping = je knipt de beste momenten uit lange video's of livestreams van een
creator (bijv. een GTA RP-streamer) en post die als korte video's (Shorts,
TikTok, Reels, X).

Je verdient NIET via het TikTok Creativity Program of YouTube-advertenties,
maar via CLIPPING-CAMPAGNES:
  1. Een streamer/merk zet een budget klaar op een clipping-platform
     (bijv. Whop Content Rewards of Vyro).
  2. Jij maakt clips volgens hun regels en post ze op JE EIGEN accounts.
  3. Je dient de link van je gepubliceerde clip in op het platform.
  4. Het platform telt je views en betaalt je per 1.000 views (CPM)
     uit het campagnebudget.

Waarom betalen ze? Jouw clips = gratis reclame/bereik voor de streamer.
De streamer GEEFT TOESTEMMING om zijn content te gebruiken. Dat is het
cruciale verschil met zomaar andermans video's reposten.""",
    },
    "platformen": {
        "titel": "Op welke sites vind je betaalde clipping-campagnes?",
        "trefwoorden": ["site", "sites", "platform", "platformen", "whop", "vyro", "waar", "aanmelden", "campagne", "content rewards", "clipping.net", "clipaffiliates"],
        "tekst": """\
1. WHOP CONTENT REWARDS  (whop.com -> 'Content Rewards')
   - Grootste marktplaats. Gratis aanmelden, meestal geen volger-eis.
   - Tarieven ca. $0,20 - $6 per 1.000 views; mediaan rond $1 - $1,50.
   - 10% platformkosten op CPM-uitbetalingen.
   - Er staan regelmatig GTA RP-campagnes (bijv. NoPixel-streamers,
     ca. $1,50 per 1.000 views in nov. 2026).

2. VYRO  (vyro.com, platform van MrBeast)
   - Je post op je eigen accounts en dient de URL in; views worden
     cross-platform geteld.
   - Gerapporteerd: ca. $1,50 - $3 per 1.000 views, vaak een max per post
     en een minimum aantal views voor uitbetaling.

3. Andere (kleiner, minder onafhankelijk gecontroleerd):
   Clipping.net, ClipAffiliates, en Discord-servers van streamers zelf
   (veel streamers hebben een #clippers-kanaal met eigen regels).

!! SCAM-REGEL: een 'campagne' waarvoor JIJ moet betalen om mee te doen
   is altijd oplichting. Echte campagnes zijn gratis.""",
    },
    "gta_campagnes": {
        "titel": "GTA-clipping specifiek",
        "trefwoorden": ["gta", "rp", "roleplay", "nopixel", "gta5", "streamer", "fivem", "gta rp"],
        "tekst": """\
- GTA RP (FiveM-servers zoals NoPixel) is een van de populairste niches:
  lange streams vol grappige, chaotische momenten = veel clipbare content.
- GTA 6 zorgt voor een enorme toestroom van content en campagnes.
- Zoek op Whop Content Rewards / Vyro op 'GTA', 'RP' of de naam van een
  streamer. Check ook de Discord van GTA RP-streamers.
- Typische regels bij GTA RP-campagnes:
    * Noem/tag de streamer (handle in beeld of in de caption).
    * Geen drama-baiting of misleidende titels.
    * Alleen content van die specifieke streamer.
- Wat goed werkt: politie-achtervolgingen, absurde dialogen, fails,
  plot twists, reacties van de streamer, 'storytime'-compilaties.
- Realiteit: de grote verdieners in GTA RP zijn de streamers zelf.
  Als clipper verdien je mee op hun bereik - het is volume-werk.""",
    },
    "content_halen": {
        "titel": "Hoe en waar haal je de content (bronvideo's)?",
        "trefwoorden": ["kopieren", "kopiëren", "plakken", "downloaden", "download", "content", "bron", "vod", "twitch", "kick", "yt-dlp", "halen", "video"],
        "tekst": """\
REGEL 1: haal alleen content van creators die het TOESTAAN (= de campagne).
Lees in de campagne-brief welke bron je mag gebruiken.

Bronnen, van makkelijk naar technisch:
 a) Campagne-materiaal: veel campagnes geven een Google Drive / Dropbox
    link met ruwe footage. Gewoon downloaden.
 b) Twitch-clips: op twitch.tv -> kanaal -> 'Clips'. Max 60 sec per clip.
    Je kunt ook zelf een clip maken tijdens een live stream (clip-knop).
 c) Twitch/Kick VOD's (hele uitzendingen): voor langere fragmenten.
    Twitch-VOD's blijven beperkt beschikbaar (vaak 14-60 dagen).
 d) Download-tool: yt-dlp (gratis, open source, commandline):
        yt-dlp "https://www.twitch.tv/videos/<id>" -o "vod.mp4"
        yt-dlp "https://kick.com/video/<uuid>" -o "vod.mp4"
    Alleen een stuk downloaden (bespaart tijd):
        yt-dlp --download-sections "*01:23:00-01:25:30" "<url>"
    Grafisch alternatief: 4K Video Downloader, TwitchLeecher.
 e) YouTube-video's van de streamer: zelfde yt-dlp-aanpak, maar ALLEEN
    als de campagne YouTube-content expliciet toestaat.

NIET doen: willekeurige virale video's van anderen downloaden en
herposten. Dat is auteursrechtinbreuk, je account wordt gestraft en je
krijgt er via campagnes niets voor betaald.""",
    },
    "tools": {
        "titel": "Welke tools heb je nodig om te knippen en te bewerken?",
        "trefwoorden": ["tool", "tools", "capcut", "opus", "opus clip", "editen", "bewerken", "knippen", "ondertitels", "captions", "submagic", "software", "app"],
        "tekst": """\
GRATIS STARTERSPAKKET:
 - CapCut (desktop/mobiel): beste gratis editor. Knippen, 9:16 formaat,
   automatische ondertitels, zoom-effecten.
 - yt-dlp: bronvideo's downloaden (zie 'content halen').
 - DaVinci Resolve (gratis, desktop) als je meer controle wilt.

AI-TOOLS (sneller, betaald, ca. $15-30/maand):
 - Opus Clip: zoekt automatisch de beste momenten in een VOD.
   (Twitch: alleen VOD's na de uitzending.)
 - ClipSpeedAI, Vizard, Klap, Ssemble: alternatieven, sommige ook voor
   live Twitch/Kick.
 - Submagic: opvallende, geanimeerde ondertitels.

BEWEZEN WORKFLOW:
  AI-clipper (moment vinden) -> CapCut/Submagic (afwerken & ondertitels)
  -> posten -> link indienen.
Tip: begin gratis met CapCut; koop pas AI-tools als je verdient.""",
    },
    "accounts": {
        "titel": "Accounts opzetten (TikTok, YouTube Shorts, Instagram, X)",
        "trefwoorden": ["account", "accounts", "tiktok", "youtube", "shorts", "instagram", "reels", "x", "twitter", "kanaal", "profiel", "posten"],
        "tekst": """\
- Maak per niche een apart account, bijv. 'GTA RP Moments NL' - zo
  begrijpt het algoritme meteen wie je doelgroep is.
- Post op meerdere platforms tegelijk: TikTok, YouTube Shorts,
  Instagram Reels (en evt. X). Eén clip = meerdere kansen op views.
- Check per campagne WELKE platforms meetellen. Niet elke campagne
  accepteert elk platform; YouTube-clips betalen soms iets meer.
- Warm een nieuw account op: eerst een paar dagen normaal scrollen en
  liken in je niche voordat je veel post.
- Zet je accounts op 'openbaar' en (bij TikTok/Instagram) op een
  creator/zakelijk account zodat je statistieken kunt zien.
- Gebruik NOOIT gekochte volgers/views: dit wordt gedetecteerd en je
  wordt uitgesloten.
- Let op YouTube: een kanaal met alleen andermans clips komt meestal
  NIET in aanmerking voor het YouTube Partner Program (reused content).
  Je verdiensten komen dan dus van de campagne, niet van YouTube.""",
    },
    "goede_clip": {
        "titel": "Hoe maak je een clip die views krijgt?",
        "trefwoorden": ["viraal", "views", "goede clip", "hook", "tips", "algoritme", "meer views", "lengte", "format", "ondertiteling"],
        "tekst": """\
1. HOOK in de eerste 1-2 seconden: begin midden in de actie, of zet een
   prikkelende tekst bovenin ('Hij had dit NOOIT moeten zeggen...').
2. Formaat 9:16 (verticaal), 1080x1920. Gameplay boven/midden,
   evt. facecam van de streamer erboven.
3. Lengte: 15-60 seconden. Snij alle stiltes en 'dode' momenten eruit.
4. Grote, duidelijke ondertitels (veel mensen kijken zonder geluid).
5. Eén verhaal/moment per clip. Duidelijk begin, climax, einde.
6. Titel/caption: kort, nieuwsgierig makend, met de verplichte tag van de
   streamer + relevante hashtags (#gtarp #gta #nopixel ...).
7. Volume & consistentie: 2-5 clips per dag per account is normaal.
8. Kijk welke clips het goed doen en maak er meer van in die stijl.
9. Post op momenten dat je doelgroep online is (avond/weekend).""",
    },
    "regels_afwijzing": {
        "titel": "Waarom worden clips afgewezen? (en hoe voorkom je dat)",
        "trefwoorden": ["afgewezen", "rejected", "afwijzing", "regels", "ban", "verbannen", "fraud", "bot", "nep views", "niet betaald", "geweigerd"],
        "tekst": """\
Veelvoorkomende redenen:
 - Regels uit de campagne-brief niet gevolgd (verkeerde streamer, geen
   tag/handle, verboden onderwerp, te kort/lang).
 - Dezelfde edit in meerdere campagnes ingediend (hergebruikte edit).
 - Collab-posts zonder toestemming.
 - Verdacht viewpatroon (gekochte views, bots, view-farms,
   engagement-groepen). Gevolg: afwijzing, uitsluiting en mogelijk
   verrekening met eerdere uitbetalingen.
 - Clip gepost vóór je je aanmeldde of buiten de campagneperiode.
 - Verkeerd land/regio als de campagne regio-eisen heeft.
 - Budget van de campagne is op: dan worden nieuwe views niet betaald.

Voorkomen: lees de HELE brief, maak per campagne een nieuwe edit,
gebruik alleen echte groei, dien in zodra je post.""",
    },
    "uitbetaling": {
        "titel": "Uitbetaling, belasting en Nederland",
        "trefwoorden": ["uitbetaling", "betaling", "uitbetalen", "paypal", "bank", "iban", "crypto", "kyc", "belasting", "kvk", "nederland", "leeftijd", "18"],
        "tekst": """\
WHOP:
 - Uitbetaling naar bankrekening, mobiele wallet of crypto in 200+ landen.
 - Je moet 18+ zijn en je identiteit verifiëren (KYC via Stripe:
   ID-bewijs + soms selfie).
 - Standaard uitbetaling tot ca. 5 werkdagen; instant opties sneller
   (tegen een fee).
 - Buiten de VS: je bankrekening moet de valuta van je geregistreerde
   land accepteren (voor NL: euro-IBAN).
 - Na goedkeuring van een clip staat het geld eerst even 'on hold'.
VYRO: uitbetaling via het dashboard; check daar minimumbedrag en methode.

NEDERLAND & BELASTING (geen belastingadvies!):
 - Inkomsten uit clipping zijn belastbaar: 'resultaat uit overige
   werkzaamheden' of, als je het structureel/zakelijk doet,
   winst uit onderneming (dan KvK-inschrijving en mogelijk btw).
 - Houd een overzicht bij van alle uitbetalingen en kosten (tools).
 - Twijfel? Bel de Belastingtelefoon of vraag een boekhouder.
 - Onder 18? Dan kun je vaak niet zelf uitbetaald worden - laat een
   ouder meekijken/het account beheren.""",
    },
    "campagne_kiezen": {
        "titel": "Hoe kies je een campagne die echt uitbetaalt?",
        "trefwoorden": ["kiezen", "beste campagne", "budget", "cap", "max", "cpm", "tarief", "welke campagne", "goedkeuring", "approval", "minimum"],
        "tekst": """\
Kijk naar VIER dingen, in deze volgorde:
 1. RESTEREND BUDGET - het belangrijkste. Bijna leeg = je views worden
    misschien niet meer betaald. Staat het budget er niet bij? Ga uit van
    'bijna leeg'.
 2. GOEDKEURINGSPERCENTAGE - $2 CPM met 65% goedkeuring en $8.000 budget
    is beter dan $4 CPM met 10% goedkeuring en $200 budget.
 3. CPM-TARIEF - mediaan rond $1,09 per 1.000 views (707 campagnes,
    nov. 2026); de meeste tussen $1 en $5.
 4. REGELS - minimum views (soms 10K-100K voordat je iets krijgt),
    maximum per clip (cap), toegestane platforms, en de looptijd
    (bij Whop stopt CPM-verdienen 30 dagen na indienen).

Vuistregel: score = CPM x resterend budget / aantal clippers dat al
meedoet. Een middelmatige CPM met een grote pot wint meestal.
Gebruik optie 'campagne-checker' in de bot om dit te berekenen.""",
    },
    "scams": {
        "titel": "Scams herkennen en vermijden",
        "trefwoorden": ["scam", "oplichting", "nep", "discord", "cursus", "betalen", "fee", "dm", "veilig", "legit", "betrouwbaar"],
        "tekst": """\
RODE VLAGGEN:
 - Je moet EERST betalen: 'clipping-cursus', 'onboarding fee',
   'verificatie-borg', betaalde Discord-tier, crypto 'gas fees'.
 - Onverwachte DM op Discord met een 'campagne' - ook van een bekende:
   veel Discord-accounts worden gehackt en gebruikt voor scams.
 - Nep-'verificatiebots' of 'ik heb je per ongeluk gerapporteerd'-
   berichten die om je login of 2FA-code vragen.
 - Trainingen die je leren andermans content zonder toestemming te
   clippen (auteursrechtrisico, accounts worden gebanned).
 - Beloftes als '$10.000 per week gegarandeerd'.

VEILIG WERKEN:
 - Gebruik alleen campagnes die zichtbaar op het platform staan
   (Whop Content Rewards, Vyro) of in de officiële Discord van de streamer.
 - Zet 2FA aan op Discord, Whop, TikTok, YouTube en je e-mail.
 - Geef nooit je wachtwoord of 2FA-code aan iemand.
 - Beperk DM's van onbekenden op Discord.""",
    },
    "gta6_kans": {
        "titel": "GTA 6: waarom NU starten?",
        "trefwoorden": ["gta 6", "gta vi", "gta6", "release", "launch", "uitkomst", "komt uit", "timing", "wanneer", "trend"],
        "tekst": """\
 - GTA 6 komt uit op donderdag 19 november 2026 (PS5 en Xbox Series X|S;
   nog geen pc-versie aangekondigd).
 - Rond de release kijkt iedereen GTA 6: streamers spelen urenlang,
   en er komen veel clipping-campagnes en zoekverkeer bij.
 - Plan:
     * Vóór de release: accounts klaar en opgewarmd, aangemeld op Whop
       en Vyro, CapCut-sjabloon (9:16, ondertitels) klaar.
     * Release-week: volg 2-3 grote streamers met een actieve campagne,
       clip hun eerste reacties, grappige fails en 'eerste keer'-momenten.
     * Daarna: kies een vaste niche (bijv. één streamer, GTA 6 RP zodra
       dat er is, of 'GTA 6 fails') en bouw consistent op.
 - Concurrentie is ook groot: snelheid (binnen enkele uren na de stream
   posten) en kwaliteit van je hook maken het verschil.""",
    },
    "verwachtingen": {
        "titel": "Hoeveel kun je realistisch verdienen?",
        "trefwoorden": ["hoeveel", "verdien", "verdienen", "inkomen", "realistisch", "per maand", "rijk", "salaris", "geld"],
        "tekst": """\
Rekensom: verdiensten = (views / 1.000) x CPM - 10% platformkosten.

Voorbeelden bij $1,50 per 1.000 views:
   10.000 views   ->  ca. $13,50
  100.000 views   ->  ca. $135
1.000.000 views   ->  ca. $1.350

Realiteit:
 - De meeste beginners verdienen de eerste weken weinig tot niets.
 - Het is VOLUME-werk: veel clips, veel accounts, veel testen.
 - Verhalen over '$10.000 per week' komen vaak van sites die tools of
   cursussen verkopen. Wees kritisch.
 - Er gelden vaak caps per clip en het budget kan op raken.
Gebruik in de bot optie 'calculator' om je eigen scenario te rekenen.""",
    },
}

# Het complete stappenplan van A tot Z.
STAPPENPLAN = [
    ("Begrijp het model",
     "Je wordt betaald door streamers/merken via clipping-campagnes, per 1.000 views. "
     "Niet door TikTok of YouTube zelf."),
    ("Check de basis",
     "Ben je 18+ (nodig voor uitbetaling/KYC)? Heb je een euro-bankrekening, een pc of "
     "goede telefoon, en 1-3 uur per dag?"),
    ("Maak je accounts aan",
     "Eén niche-account (bijv. 'GTA RP Moments') op TikTok, YouTube Shorts en Instagram. "
     "Openbaar + creator-account. Een paar dagen opwarmen in de niche."),
    ("Meld je aan op de platforms",
     "Maak een gratis account op Whop (Content Rewards) en Vyro. Verifieer je identiteit "
     "en koppel je uitbetaalmethode alvast."),
    ("Kies een campagne",
     "Zoek op 'GTA' / 'RP' / streamernaam. Kijk naar: CPM-tarief, resterend budget, "
     "max per clip, toegestane platforms. Kies er 1-2 om mee te beginnen."),
    ("Lees de brief VOLLEDIG",
     "Welke bron mag je gebruiken? Moet de handle in beeld? Welke hashtags? Wat is verboden? "
     "Schrijf de regels op."),
    ("Haal de bronvideo",
     "Campagne-Drive, Twitch-clips, of de VOD via yt-dlp "
     "(yt-dlp --download-sections \"*start-eind\" <url>). Alleen toegestane content."),
    ("Vind de beste momenten",
     "Kijk de VOD op 1,5-2x snelheid of gebruik een AI-clipper (Opus Clip e.d.). "
     "Noteer tijdstempels van grappige/spannende stukken."),
    ("Edit de clip",
     "CapCut: 9:16, 15-60 sec, sterke hook in de eerste 2 sec, stiltes eruit, grote "
     "ondertitels, handle van de streamer in beeld."),
    ("Post op je accounts",
     "Pakkende caption + verplichte tag + hashtags. Post op alle toegestane platforms."),
    ("Dien de link in",
     "Plak de URL van je gepubliceerde clip in de campagne op Whop/Vyro. Doe dit direct "
     "na het posten."),
    ("Volg je views en uitbetaling",
     "Het platform telt je views; na goedkeuring komt het geld in je saldo. Opnemen naar "
     "je bank zodra het vrijgegeven is."),
    ("Analyseer en verbeter",
     "Welke clips scoorden? Welke hooks? Maak meer van wat werkt, schrap wat niet werkt."),
    ("Opschalen",
     "Meer clips per dag, meer campagnes, evt. AI-tools of een tweede account. "
     "Houd je administratie bij voor de belasting."),
]

DAGELIJKSE_CHECKLIST = [
    "Nieuwe/actieve campagnes gecheckt (budget nog niet op?)",
    "Nieuwe VOD's/streams van mijn streamer(s) bekeken",
    "Minimaal 2-5 clips gemaakt",
    "Elke clip: hook, 9:16, ondertitels, handle/tag in beeld",
    "Gepost op alle toegestane platforms",
    "Alle links ingediend op Whop/Vyro",
    "Statistieken van gisteren bekeken en genoteerd",
    "Inkomsten/kosten bijgewerkt in mijn administratie",
]

# Sjablonen voor hooks (tekst bovenin de clip) en captions.
HOOK_SJABLONEN = [
    "{streamer} had dit NOOIT moeten doen...",
    "Wacht tot het einde 😭",
    "Dit is waarom {streamer} niet mag rijden in GTA",
    "POV: je bent de politie in GTA RP",
    "Niemand had dit zien aankomen...",
    "{streamer} verloor ALLES in 10 seconden",
    "De meest chaotische achtervolging ooit",
    "Hij dacht dat niemand het zag...",
    "Dit gebeurde er in de eerste 5 minuten van GTA 6",
    "Rate deze escape van 1 tot 10",
]

CAPTION_SJABLOON = (
    "{hook} 🎮\n"
    "Credit: @{streamer} ({platform})\n"
    "#gta #gtarp #gta6 #{streamer_tag} #gaming #fyp"
)

BRONNEN = [
    "https://docs.whop.com/manage-your-business/growth-marketing/content-rewards",
    "https://docs.whop.com/manage-your-business/manage-payouts/payout-methods",
    "https://www.opus.pro/blog/whop-content-rewards",
    "https://www.opus.pro/blog/vyro-vs-whop",
    "https://contentrewards.com/articles/gta-6-clipping",
    "https://www.clipspeed.ai/blog/gta-6-clipping.html",
    "https://findclout.com/blog/why-clips-get-rejected",
    "https://findclout.com/blog/youtube-reused-content-policy-clipping",
    "https://autoclip.dev/blog/kick-vod-download-and-clip-workflow",
    "https://www.ssemble.com/blog/how-to-clip-twitch-streams-2026",
    "https://contentrewards.com/articles/clipping-cpm-rates-november-2026",
    "https://openclip.app/clipping/campaign-budget-and-payout-risk",
    "https://findclout.com/blog/clipping-discord-scams",
    "https://www.gtaboom.com/gta-6-release-date-platforms-and-what-is-locked-in-aa48",
]


def volledige_kennis_als_tekst() -> str:
    """Alle kennis als één tekst (gebruikt als context voor de AI-modus)."""
    delen = [f"KENNISBANK CLIPBOT (bijgewerkt {LAATST_BIJGEWERKT})\n"]
    for o in ONDERWERPEN.values():
        delen.append(f"## {o['titel']}\n{o['tekst']}\n")
    delen.append("## Stappenplan A-Z")
    for i, (titel, uitleg) in enumerate(STAPPENPLAN, 1):
        delen.append(f"{i}. {titel}: {uitleg}")
    delen.append("\n## Dagelijkse checklist")
    delen.extend(f"- {c}" for c in DAGELIJKSE_CHECKLIST)
    return "\n".join(delen)
