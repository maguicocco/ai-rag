# AI Act RAG — Cross-lingual Question Answering

A multilingual (Spanish / English / French) question-answering system over the **EU Artificial Intelligence Act** (Regulation 2024/1689) that cites the exact article behind each answer, plus a study of **how much retrieval degrades when the question and the documents are in different languages** — and which techniques fix it.

Because the EU publishes the law with identical content in every official language, the text stays fixed while only the language changes: any difference in results comes from the language, not the content.

## Research question

> If a user asks in Spanish but the documents are in French (or vice versa), how much worse is retrieval, and what closes the gap?

## Roadmap

- [ ] **1. Data** — download the AI Act in ES/EN/FR and split it by article
- [ ] **2. Evaluation set** — ~100 manually written and verified questions in 3 languages, each linked to its source article(s)
- [ ] **3. Retrieval baseline** — multilingual embeddings + recall@k / MRR for every query × document language pair
- [ ] **4. Experiments** — embedding models, query translation, hybrid search (BM25 + dense), reranking
- [ ] **5. Generation** — LLM answers in the user's language with article citations; faithfulness evaluation
- [ ] **6. Demo** — Gradio app on Hugging Face Spaces

## Results

*Coming soon.*

## Project structure

```
src/
  download.py         # downloads the AI Act from EUR-Lex (ES, EN, FR)
  parse_articles.py   # splits each version into one JSON record per article
data/
  raw/                # EUR-Lex pages, any file name (not versioned)
  processed/          # articles_<lang>.jsonl
  eval/questions.jsonl
tests/
```

## Quick start

```bash
pip install -r requirements.txt
python src/download.py
python src/parse_articles.py
python -m pytest
```

## Data format

`data/processed/articles_<lang>.jsonl` — one article per line:

```json
{"id": 5, "chapter": "II", "title": "Artículo 5", "subtitle": "Prácticas de IA prohibidas", "text": "1. Quedan prohibidas..."}
```

`data/eval/questions.jsonl` — one question per line, same question in the three languages, with the article(s) that answer it:

```json
{"id": 1, "es": "...", "en": "...", "fr": "...", "articles": [5]}
```

## Source

Regulation (EU) 2024/1689 (Artificial Intelligence Act), [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj).
