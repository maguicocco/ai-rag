import sys
sys.path.insert(0, "src")
from parse_articles import parse

HTML = """
<div id="cpt_II">
  <div id="art_5">
    <p class="oj-ti-art">Artículo 5</p>
    <div class="eli-title"><p class="oj-sti-art">Prácticas de IA prohibidas</p></div>
    <p class="oj-normal">1. Quedan prohibidas las siguientes prácticas de IA:</p>
    <table><tr><td><p class="oj-normal">a)</p></td><td><p class="oj-normal">la introducción en el mercado...</p></td></tr></table>
  </div>
</div>
"""


def test_parse():
    [a] = parse(HTML)
    assert a["id"] == 5
    assert a["chapter"] == "II"
    assert a["title"] == "Artículo 5"
    assert a["subtitle"] == "Prácticas de IA prohibidas"
    assert a["text"].startswith("1. Quedan prohibidas")
    assert "Artículo 5" not in a["text"]
