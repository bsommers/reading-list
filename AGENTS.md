# Agent Instructions (`reading-list`)

## Commands

- **Run unit & smoke tests:** `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- **Quickly classify text/abstracts on the fly:** `PYTHONPATH=src python3 -m reading_list.cli classify --title "..." --text "..."`
- **Add & classify a new article/paper/note:** `PYTHONPATH=src python3 -m reading_list.cli add --title "..." --type academic_paper --url "..." --text "..." --cites arxiv-2610.08739v2 --priority high`
- **List & filter tracked reading list:** `PYTHONPATH=src python3 -m reading_list.cli list [--status to-read] [--tech-area "AI Security"] [--concept bare-ai]`
- **Update tracking status/notes:** `PYTHONPATH=src python3 -m reading_list.cli status <doc_id> --set read --priority high --notes "..."`
- **Seed `input/corpus.json`:** `PYTHONPATH=src python3 -m reading_list.cli seed-input`
- **Build all knowledge-graph & taxonomy outputs:** `PYTHONPATH=src python3 -m reading_list.cli build --input input/corpus.json --output-dir output`

## Repository Rules

- Keep `input/*` and `output/*` untracked except for `input/README.md` and `output/README.md`.
- Maintain deterministic JSON output (`sort_keys=True`) and preserve `ontologic_class_uri` / JSON-LD `@context` fields for upcoming OntoLogic integration.
- When adding new articles or papers to `tests/fixtures/seed_corpus.json` (or `input/corpus.json`), link secondary coverage to primary papers via `REPORTS_ON` or `CITES` relations.
