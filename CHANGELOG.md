# Changelog

All notable changes to `reading-list` are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-11-07

### Added
- **Curriculum Importer (`kitsumiko` & `import-curriculum` CLI):** Added `src/reading_list/kitsumiko.py` and `python3 -m reading_list.cli import-curriculum --source <dir> -d <db>` to parse, deduplicate, and import curated AI/ML paper curricula (`kitsumiko/papers`) into OntoLogic-ready knowledge-graph databases while preserving full Apache-2.0 attribution (`LICENSE`, `NOTICE.md`, `learning/`, `learning-path.md`, `by-date.md`, and `identifiers.kitsumiko_*` back-references).
- **Rendered Markdown Artifact Pages (`taxonomy.html`, `chunks.html`, `summary.html`):** Added human-readable Markdown (`taxonomy.md`, `chunks.md`) and interactive rendered HTML viewers (`taxonomy.html`, `chunks.html`, `summary.html`) for the header's **Taxonomy**, **Chunks**, and **Summary MD** buttons, complete with client-side search filtering and direct **Raw File** + **Download** actions for both Markdown and JSON (`taxonomy_tree.json`, `chunks.json`, `summary.md`).
- **Neon-Blue `⚡ TRON` Theme (`[data-theme="tron"]`):** Added a 3-way theme selector (`Dark` | `⚡ TRON` | `Light`) persisted in `localStorage` across the main explorer and all rendered Markdown viewer pages, featuring a deep-grid background (`#020813`), glowing cyan borders (`#00f0ff`), neon status badges, and cyan force-directed graph styling.
- **Interactive KPI Row & Linked Document Drawer (`#kpi-linked-drawer`):** Upgraded the 6 top-level KPI cards (`Scoped Documents`, `Semantic Chunks`, `Active Concepts`, `Taxonomy Nodes`, `Total Graph Nodes`, `Total Graph Edges`) with inline clickable document badges that jump directly to `#corpus-heading` and highlight the document, plus an expandable linked-items drawer (`View all N →`) for deep navigation across documents, chunks, concepts, taxonomy paths, and knowledge-graph edges.

### Changed
- **Expanded Conceptual Taxonomy (`src/reading_list/taxonomy.py`):** Added 9 new technology-area rules and 8 new concept definitions covering neuro-symbolic architectures, lattice deduction, logic programming, datalog, GPU-accelerated combinatorial optimization (`CuOpt`), LLM cybersecurity benchmarks (`SEC-bench`), and multi-agent formal hardware verification (`VeriMAS`, `Vericoding`).

## [0.1.0] - 2026-11-07

### Added
- **Initial Release:** Core Python package (`models`, `taxonomy`, `chunker`, `graph`, `enrich`, `research`, `site`, `cli`) for semantic chunking, hierarchical taxonomy classification, TF-IDF word-cloud indexing, OntoLogic-compatible JSON-LD knowledge graph generation, and interactive GitHub Pages static site generation.
- **CLI Commands:** Added `build`, `update`, `publish-db`, `research`, `add`, `list`, `status`, and `classify` commands with `-d` / `--db` / `--db-dir` support for external database repositories.
