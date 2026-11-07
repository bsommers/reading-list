# Reading List (`reading-list`)

Core Python tooling, research agent, semantic chunker, conceptual taxonomy classifier, word-cloud indexer, and OntoLogic-ready knowledge graph builder.

- **This Repository (`reading-list`):** Houses the indexing, topic research, classification, and static-site generation engine with a minimal 2-document seed corpus to demonstrate the pipeline.
- **Published Database & GitHub Pages (`reading-db`):** The populated reading database, generated JSON-LD knowledge graph, and interactive GitHub Pages dashboard live in the sister repository: **[`bsommers/reading-db`](https://github.com/bsommers/reading-db)** (**[Live GitHub Pages Dashboard](https://bsommers.github.io/reading-db/)**).

## Repository Layout

| Path | Holds | Git |
|---|---|---|
| `src/reading_list/` | Importable Python package (`models`, `taxonomy`, `chunker`, `graph`, `enrich`, `research`, `site`, `cli`) | tracked |
| `tests/` | Unit/smoke tests (`test_smoke.py`) and minimal demo corpus (`fixtures/seed_corpus.json`) | tracked |
| `docs/` | Architecture (`architecture.md`), OntoLogic roadmap, and ADRs (`docs/adr/`) | tracked |
| `input/` | Local working corpus manifest (`corpus.json`) | ignored except `README.md` |
| `output/` | Local reproducible knowledge graph, chunks, word cloud, taxonomy, and `index.html` | ignored except `README.md` |
| `README.md` | Project overview, layout table, quickstart, and status | tracked |

## Tracked Reading List Corpus (`tests/fixtures/seed_corpus.json`)

1. **Technical Article:** [*On-Chip Monitors Detect Bit-Flip Attacks in AI Accelerators (UF, UT Dallas, RPI)*](https://semiengineering.com/on-chip-monitors-detect-bit-flip-attacks-in-ai-accelerators-uf-ut-dallas-rpi/) (`semieng-2026-bare-ai-monitors` — Semiconductor Engineering Staff — University of Florida; University of Texas at Dallas; Rensselaer Polytechnic Institute)
2. **Academic Paper:** [*BARE-AI: Bit-Flip Attack Resilience in AI Hardware through Built-in Performance Monitors*](https://arxiv.org/abs/2610.08739v2) (`arxiv-2610.08739v2` — Habibur Rahaman, Swastik Bhattacharya, Sanjay Das, Kanad Basu, Swarup Bhunia — University of Florida; University of Texas at Dallas; Rensselaer Polytechnic Institute)
3. **Research Note:** *Rowhammer Faults in ViT NPUs* (`note-rowhammer-vit`)

## Quickstart: `python3 -m reading_list.cli <command> [switches] [subcommand(s)]`

All commands accept `-d` / `--db` / `--db-dir <path>` to target and rebuild any specified reading database (such as `../reading-db`):

```bash
# 1. Run the verification test suite
PYTHONPATH=src python3 -m unittest discover -s tests -v

# 2. Research a topic and add to ../reading-db (adds primary papers + synthesis note & rebuilds site)
python3 -m reading_list.cli research -d ../reading-db \
  -t "SAT and SMT solvers applications in software development, graph analysis, and ontologies" add

# 3. Add a new document directly to the specified reading-db repository and rebuild all artifacts
python3 -m reading_list.cli add -d ../reading-db \
  --title "Your Paper or Article Title" \
  --type academic_paper \
  --url "https://arxiv.org/abs/..." \
  --text "Paste abstract or notes here..." \
  --priority high

# 4. List or update status in the specified database
python3 -m reading_list.cli list -d ../reading-db --status to-read
python3 -m reading_list.cli status arxiv-1610.00502 -d ../reading-db --set read --priority high

# 5. Publish enriched corpus, knowledge graph JSONs, and interactive GitHub Pages site to ../reading-db
python3 -m reading_list.cli publish-db -d ../reading-db

# 6. Classify any snippet or abstract on the fly (without saving)
python3 -m reading_list.cli classify \
  --title "Rowhammer Fault Injection in NPU Accelerators" \
  --text "Memory-level bit-flip perturbations in DRAM degrade Vision Transformer accuracy on 28nm AI accelerators."
```

## Status

Tooling (`research`, `add`, `list`, `status`, `update`, `publish-db`, `classify`), semantic chunker, conceptual taxonomy classifier, and GitHub Pages generator operational (`v0.1.0`).
