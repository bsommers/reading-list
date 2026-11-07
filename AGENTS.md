# Agent Instructions (`reading-list`)

## Commands (`python3 -m reading_list.cli <command> [switches] [subcommand(s)]`)

- **Research a topic & add to specified DB:** `python3 -m reading_list.cli research -d ../reading-db -t "SAT and SMT solvers applications in software development, graph analysis, and ontologies" add`
- **Add & classify a paper/article/note into specified DB:** `python3 -m reading_list.cli add -d ../reading-db --title "..." --type academic_paper --url "..." --text "..." --cites arxiv-2610.08739v2 --priority high`
- **Publish `../reading-db` knowledge graph & GitHub Pages site:** `python3 -m reading_list.cli publish-db -d ../reading-db`
- **Single-command full update (enrich, sync tracked corpus & README, rebuild `output/` or `-d <db>`):** `python3 -m reading_list.cli update [-d ../reading-db]`
- **Run unit & smoke tests:** `PYTHONPATH=src python3 -m unittest discover -s tests -v`
- **Quickly classify text/abstracts on the fly:** `python3 -m reading_list.cli classify --title "..." --text "..."`
- **List & filter tracked reading list:** `python3 -m reading_list.cli list [-d ../reading-db] [--status to-read] [--tech-area "AI Security"] [--concept bare-ai]`
- **Update tracking status/notes:** `python3 -m reading_list.cli status <doc_id> [-d ../reading-db] --set read --priority high --notes "..."`

## Repository Rules

- Keep `input/*` and `output/*` untracked except for `input/README.md` and `output/README.md`.
- Maintain deterministic JSON output (`sort_keys=True`) and preserve `ontologic_class_uri` / JSON-LD `@context` fields for upcoming OntoLogic integration.
- When adding new articles or papers to `tests/fixtures/seed_corpus.json` (or `../reading-db/corpus.json`), link secondary coverage to primary papers via `REPORTS_ON` or `CITES` relations.
