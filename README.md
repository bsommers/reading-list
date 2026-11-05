# Reading List (`reading-list`)

A curated reading-list repository and knowledge-graph indexer for technical articles, technical papers, and academic papers. Documents are tracked with reading status/priority, semantically chunked, indexed for domain concepts and word-cloud term frequencies, categorized into a hierarchical conceptual taxonomy and technology areas, and linked in a JSON-LD knowledge graph designed for future integration with **OntoLogic** and **openGSD**.

## Repository Layout

| Path | Holds | Git |
|---|---|---|
| `src/reading_list/` | Importable Python package (`models`, `taxonomy`, `chunker`, `graph`, `cli`) | tracked |
| `tests/` | Unit/smoke tests (`test_smoke.py`) and tracked seed corpus (`fixtures/seed_corpus.json`) | tracked |
| `docs/` | Architecture (`architecture.md`), OntoLogic roadmap, and ADRs (`docs/adr/`) | tracked |
| `input/` | Read-only source documents and corpus manifests (`corpus.json`) | ignored except `README.md` |
| `output/` | Reproducible knowledge graph, semantic chunks, word clouds, and taxonomy artifacts | ignored except `README.md` |
| `README.md` | Project overview, layout table, quickstart, and status | tracked |

## Initial Seed Corpus

1. **Technical Article:** [*On-Chip Monitors Detect Bit-Flip Attacks in AI Accelerators (UF, UT Dallas, RPI)*](https://semiengineering.com/on-chip-monitors-detect-bit-flip-attacks-in-ai-accelerators-uf-ut-dallas-rpi/) (`semieng-2026-bare-ai-monitors`)
2. **Academic Paper:** [*BARE-AI: Bit-Flip Attack Resilience in AI Hardware through Built-in Performance Monitors*](https://arxiv.org/abs/2610.08739v2) (`arxiv-2610.08739v2` — Habibur Rahaman, Swastik Bhattacharya, Sanjay Das, Kanad Basu, Swarup Bhunia; UF, UT Dallas, RPI)

## Quickstart: Tracking & Classifying Content

```bash
# 1. Run the verification test suite
PYTHONPATH=src python3 -m unittest discover -s tests -v

# 2. Classify any snippet or abstract on the fly (without saving)
PYTHONPATH=src python3 -m reading_list.cli classify \
  --title "Rowhammer Fault Injection in NPU Accelerators" \
  --text "Memory-level bit-flip perturbations in DRAM degrade Vision Transformer accuracy on 28nm AI accelerators."

# 3. List and filter tracked documents by status, priority, taxonomy, or concept
PYTHONPATH=src python3 -m reading_list.cli list
PYTHONPATH=src python3 -m reading_list.cli list --concept bare-ai

# 4. Add & classify a new paper/article/note into input/corpus.json and rebuild output/
PYTHONPATH=src python3 -m reading_list.cli add \
  --title "Your Paper or Article Title" \
  --type academic_paper \
  --url "https://arxiv.org/abs/..." \
  --text "Paste abstract or notes here..." \
  --cites arxiv-2610.08739v2 \
  --priority high

# 5. Update reading status, priority, or notes on any tracked document
PYTHONPATH=src python3 -m reading_list.cli status arxiv-2610.08739v2 \
  --set reading \
  --priority high \
  --notes "Key baseline for runtime APC + PULSE monitoring at 28nm"
```

## Status

Scaffold + quick document tracking (`add`, `list`, `status`), instant content classification (`classify`), semantic chunking, word-cloud generation, and OntoLogic-ready knowledge graph builder operational (`v0.1.0`).
