"""Download the EU AI Act (Regulation 2024/1689) from EUR-Lex in ES, EN and FR."""
from pathlib import Path
import requests

URL = "https://eur-lex.europa.eu/legal-content/{lang}/TXT/HTML/?uri=CELEX:32024R1689"
LANGS = ["ES", "EN", "FR"]
RAW = Path("data/raw")

RAW.mkdir(parents=True, exist_ok=True)
for lang in LANGS:
    r = requests.get(URL.format(lang=lang), headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    r.raise_for_status()
    if len(r.text) < 100_000:  # EUR-Lex sometimes blocks scripts and returns an empty page
        print(f"{lang}: download blocked. Open {URL.format(lang=lang)} in your browser and save it as data/raw/ai_act_{lang.lower()}.html")
        continue
    path = RAW / f"ai_act_{lang.lower()}.html"
    path.write_text(r.text, encoding="utf-8")
    print(f"{lang}: {len(r.text) // 1000} KB -> {path}")
