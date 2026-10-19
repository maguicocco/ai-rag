"""Split each language version of the AI Act into one record per article."""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

RAW, OUT = Path("data/raw"), Path("data/processed")


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    for div in soup.find_all("div", id=re.compile(r"^art_\d+$")):
        title = div.find("p", class_="oj-ti-art")
        subtitle = div.find("p", class_="oj-sti-art")
        chapter = div.find_parent("div", id=re.compile(r"^cpt_[IVXL]+$"))
        article = {
            "id": int(div["id"][4:]),
            "chapter": chapter["id"][4:] if chapter else None,
            "title": clean(title.get_text()) if title else "",
            "subtitle": clean(subtitle.get_text()) if subtitle else "",
        }
        for p in (title, subtitle):
            if p:
                p.decompose()  # remove so they don't repeat in the body
        article["text"] = clean(div.get_text(" "))
        articles.append(article)
    return articles


def language(html):
    # EUR-Lex pages say their language in a meta tag, so file names don't matter
    m = re.search(r"z_usr_lan['\"] content=['\"](\w+)", html)
    return m.group(1).lower() if m else None


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    ids = {}
    for path in sorted(RAW.iterdir()):
        html = path.read_text(encoding="utf-8", errors="ignore")
        lang, articles = language(html), parse(html)
        if not lang or not articles:
            print(f"Skipping {path.name}: not an AI Act page")
            continue
        with open(OUT / f"articles_{lang}.jsonl", "w", encoding="utf-8") as f:
            for a in articles:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")
        ids[lang] = {a["id"] for a in articles}
        print(f"{lang}: {len(articles)} articles ({path.name})")

    if not ids:
        print("No articles found. Put the EUR-Lex pages of the AI Act into data/raw/")
    elif len({frozenset(s) for s in ids.values()}) > 1:
        print("WARNING: languages don't have the same articles")
    elif len(next(iter(ids.values()))) != 113:
        print("WARNING: expected 113 articles")
    else:
        print(f"OK: 113 articles aligned across {len(ids)} languages")
