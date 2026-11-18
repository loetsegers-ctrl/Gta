"""Maak een kant-en-klare verticale clip (9:16) uit een bronvideo.

Voorbeelden:
    python -m clipbot.maak_clip bron.mp4 --start 1:23:05 --eind 1:23:40 \\
        --streamer Lysium --hook "Hij had dit NOOIT moeten doen..."
    python -m clipbot.maak_clip "https://www.twitch.tv/videos/123" --start 10:00 --eind 10:30 --streamer Lysium

Uitvoer: <naam>.mp4 (1080x1920, H.264/AAC) en <naam>.txt (caption + checklist).
Gebruik alleen bronmateriaal waarvoor de campagne/streamer toestemming geeft.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path

from . import kennis
from .bot import _normaliseer, re

BREEDTE, HOOGTE = 1080, 1920
LETTERTYPE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MIN_SEC, MAX_SEC = 5, 90


def tijd_naar_sec(t: str) -> float:
    """'1:23:05' / '23:05' / '65.5' -> seconden."""
    delen = [float(x) for x in t.strip().split(":")]
    if not 1 <= len(delen) <= 3 or any(d < 0 for d in delen):
        raise ValueError(f"ongeldige tijd: {t!r}")
    sec = 0.0
    for d in delen:
        sec = sec * 60 + d
    return sec


def _zonder_emoji(tekst: str) -> str:
    # Het lettertype heeft geen emoji; die zouden als blokjes verschijnen.
    return " ".join("".join(c for c in tekst if ord(c) < 0x2600).split())


def ffmpeg_filter(hook_bestand: str | None, credit_bestand: str | None) -> str:
    """Filtergraph: vervaagde achtergrond + scherpe video in het midden + teksten."""
    f = (
        f"[0:v]scale={BREEDTE}:{HOOGTE}:force_original_aspect_ratio=increase,"
        f"crop={BREEDTE}:{HOOGTE},boxblur=20:2,eq=brightness=-0.08[bg];"
        f"[0:v]scale={BREEDTE}:-2[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1"
    )
    if hook_bestand:
        f += (f",drawtext=fontfile={LETTERTYPE}:textfile={hook_bestand}:fontsize=64:"
              f"fontcolor=black:box=1:boxcolor=white@0.95:boxborderw=24:line_spacing=12:"
              f"x=(w-text_w)/2:y=230")
    if credit_bestand:
        f += (f",drawtext=fontfile={LETTERTYPE}:textfile={credit_bestand}:fontsize=46:"
              f"fontcolor=white:borderw=4:bordercolor=black@0.8:x=(w-text_w)/2:y=h-330")
    return f + "[v]"


def download_fragment(url: str, start: float, eind: float, map_: Path) -> Path:
    if not shutil.which("yt-dlp"):
        raise SystemExit("yt-dlp ontbreekt. Installeer met:  pip install yt-dlp")
    sjabloon = str(map_ / "bron.%(ext)s")
    cmd = ["yt-dlp", "--no-playlist", "-f", "bv*[height<=1080]+ba/b[height<=1080]/b",
           "--download-sections", f"*{start}-{eind}", "--force-keyframes-at-cuts",
           "--merge-output-format", "mp4", "-o", sjabloon, url]
    subprocess.run(cmd, check=True)
    gevonden = sorted(map_.glob("bron.*"))
    if not gevonden:
        raise SystemExit("Download mislukt: geen bestand ontvangen.")
    return gevonden[0]


def luidheid_per_seconde(pad: Path) -> list[float]:
    """Momentane luidheid (LUFS) per seconde via ffmpeg's ebur128-filter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(pad), "-vn",
                        "-af", "ebur128=framelog=verbose", "-f", "null", "-"],
                       capture_output=True, text=True)
    per_sec: dict[int, list[float]] = {}
    for m in re.finditer(r"t:\s*([\d.]+)\s+TARGET.*?M:\s*(-?[\d.]+|-inf)", r.stderr):
        waarde = -70.0 if m.group(2) == "-inf" else max(float(m.group(2)), -70.0)
        per_sec.setdefault(int(float(m.group(1))), []).append(waarde)
    if not per_sec:
        return []
    return [max(per_sec.get(i, [-70.0])) for i in range(max(per_sec) + 1)]


def vind_hoogtepunten(luidheid: list[float], duur: int = 30, aantal: int = 3) -> list[tuple[int, float]]:
    """Beste vensters (startseconde, score): veel harde pieken = enthousiasme.

    Score = gemiddelde luidheid + 2x het aandeel seconden dat >6 dB boven het
    gemiddelde van de hele video zit (schreeuwen/juichen), zonder overlap.
    """
    if not luidheid:
        return []
    duur = max(1, min(duur, len(luidheid)))
    basis = sum(luidheid) / len(luidheid)
    kandidaten = []
    for start in range(0, len(luidheid) - duur + 1):
        venster = luidheid[start:start + duur]
        pieken = sum(1 for v in venster if v > basis + 6) / duur
        kandidaten.append((sum(venster) / duur + 20 * pieken, start))
    kandidaten.sort(reverse=True)
    gekozen: list[tuple[int, float]] = []
    for score, start in kandidaten:
        if all(abs(start - g) >= duur for g, _ in gekozen):
            gekozen.append((start, round(score, 1)))
        if len(gekozen) == aantal:
            break
    return gekozen


def _fmt(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def heeft_audio(pad: Path) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "stream=index", "-of", "csv=p=0", str(pad)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def caption_tekst(hook: str, streamer: str, platform: str) -> str:
    tag = re.sub(r"[^a-z0-9]", "", _normaliseer(streamer)) or "streamer"
    caption = kennis.CAPTION_SJABLOON.format(hook=hook, streamer=streamer.replace(" ", ""),
                                             platform=platform, streamer_tag=tag)
    return (caption + "\n\n--- VOOR JE POST ---\n"
            "[ ] Verplichte tag/hashtags van de campagne erbij gezet?\n"
            "[ ] Gepost op alle toegestane platforms?\n"
            "[ ] Link direct ingediend op Whop/Vyro?\n")


def maak_clip(bron: str, start: str, eind: str, uit: Path, streamer: str,
              hook: str | None = None, platform: str = "Twitch",
              tekst_in_beeld: bool = True) -> tuple[Path, Path]:
    s, e = tijd_naar_sec(start), tijd_naar_sec(eind)
    duur = e - s
    if duur <= 0:
        raise SystemExit("De eindtijd moet na de starttijd liggen.")
    if not MIN_SEC <= duur <= MAX_SEC:
        print(f"Let op: clip is {duur:.0f} sec; 15-60 sec werkt meestal het best.", file=sys.stderr)
    hook = hook or kennis.HOOK_SJABLONEN[0].format(streamer=streamer)
    uit = uit.with_suffix(".mp4")
    uit.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_p = Path(tmp)
        if bron.startswith(("http://", "https://")):
            invoer, zoek_start = download_fragment(bron, s, e, tmp_p), 0.0
        else:
            invoer, zoek_start = Path(bron), s
            if not invoer.exists():
                raise SystemExit(f"Bestand niet gevonden: {invoer}")
        hook_f = credit_f = None
        if tekst_in_beeld:
            hook_f = tmp_p / "hook.txt"
            hook_f.write_text("\n".join(textwrap.wrap(_zonder_emoji(hook), 24)) or " ", encoding="utf-8")
            credit_f = tmp_p / "credit.txt"
            credit_f.write_text(f"@{streamer.replace(' ', '')} op {platform}", encoding="utf-8")

        cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{zoek_start}", "-t", f"{duur}", "-i", str(invoer),
               "-filter_complex", ffmpeg_filter(hook_f and str(hook_f), credit_f and str(credit_f)), "-map", "[v]"]
        if heeft_audio(invoer):
            cmd += ["-map", "0:a:0", "-c:a", "aac", "-b:a", "160k"]
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                "-r", "30", "-movflags", "+faststart", str(uit)]
        subprocess.run(cmd, check=True)

    txt = uit.with_suffix(".txt")
    txt.write_text(caption_tekst(hook, streamer, platform), encoding="utf-8")
    return uit, txt


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Maak een verticale clip met hook en credit")
    p.add_argument("bron", help="pad naar videobestand of URL (Twitch/Kick/YouTube)")
    p.add_argument("--start", help="starttijd, bijv. 1:23:05 (weglaten = automatisch hoogtepunt)")
    p.add_argument("--eind", help="eindtijd, bijv. 1:23:40")
    p.add_argument("--duur", type=int, default=30, help="lengte bij automatisch zoeken (sec)")
    p.add_argument("--streamer", required=True, help="naam/handle van de streamer")
    p.add_argument("--hook", help="tekst bovenin de clip")
    p.add_argument("--geen-tekst", action="store_true", help="geen tekst in beeld (caption blijft)")
    p.add_argument("--platform", default="Twitch", help="platform van de streamer")
    p.add_argument("--uit", default="clips/clip.mp4", help="uitvoerbestand")
    a = p.parse_args(argv)
    if not a.start:
        if a.bron.startswith(("http://", "https://")):
            raise SystemExit("Automatisch zoeken werkt op een gedownload bestand; geef anders --start/--eind.")
        top = vind_hoogtepunten(luidheid_per_seconde(Path(a.bron)), a.duur)
        if not top:
            raise SystemExit("Geen geluid gevonden om een hoogtepunt te bepalen; geef --start/--eind.")
        print("Meest enthousiaste momenten:")
        for i, (st, sc) in enumerate(top, 1):
            print(f"  {i}. {_fmt(st)} - {_fmt(st + a.duur)}  (score {sc})")
        a.start, a.eind = _fmt(top[0][0]), _fmt(top[0][0] + a.duur)
        print(f"Ik knip #1: {a.start} - {a.eind}")
    elif not a.eind:
        raise SystemExit("Geef ook --eind op.")
    video, txt = maak_clip(a.bron, a.start, a.eind, Path(a.uit), a.streamer, a.hook, a.platform,
                           tekst_in_beeld=not a.geen_tekst)
    print(f"Klaar: {video}\nCaption: {txt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
