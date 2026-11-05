# Output Directory (`output/`)

Generated artifacts produced from `input/` (or `tests/fixtures/seed_corpus.json`). All files in this directory except `README.md` are git-ignored and deterministically reproducible.

## Generated Artifacts

- `output/knowledge_graph.json` — Nodes (`document`, `chunk`, `concept`, `taxonomy_category`, `technology_area`, `author`, `institution`), typed edges (`HAS_CHUNK`, `MENTIONS_CONCEPT`, `IN_CATEGORY`, `IN_TECH_AREA`, `REPORTS_ON`, `AUTHORED_BY`, `AFFILIATED_WITH`, `SUBCATEGORY_OF`, `RELATED_CONCEPT`), and OntoLogic-ready JSON-LD `@context` mappings.
- `output/chunks.json` — Semantically chunked segments for every document with token counts, key terms, matched concepts, and assigned conceptual hierarchy paths.
- `output/word_cloud.json` — Term frequency weights (per-document and global corpus) normalized for word-cloud visualization and concept indexing.
- `output/taxonomy_tree.json` — Hierarchical conceptual taxonomy and technology area index with attached documents and chunks.
- `output/summary.md` — Human-readable Markdown index with Mermaid knowledge graph and taxonomy diagrams.

## Regenerating Outputs

Run the pipeline from the repository root:

```bash
PYTHONPATH=src python3 -m reading_list.cli build \
  --input tests/fixtures/seed_corpus.json \
  --output-dir output
```
