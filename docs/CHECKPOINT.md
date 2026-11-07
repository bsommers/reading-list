# Checkpoint — Synoptic Domain Navigator & Knowledge Graph Pipeline — 2026-11-07

**Status:** COMPLETE

## Done (with evidence)
- **Tooling repository ([`reading-list`](file:///Users/bill/src/reading-list)):**
  - `HEAD` at `e083c82` (`origin/main` in sync: `https://github.com/bsommers/reading-list`).
  - Unit & smoke test suite (`PYTHONPATH=src python3 -m unittest discover -s tests -v`) → **6 passed in 0.102s**.
  - Minimal 2-document seed fixture in [`tests/fixtures/seed_corpus.json`](file:///Users/bill/src/reading-list/tests/fixtures/seed_corpus.json) (BARE-AI primary paper `arxiv-2610.08739v2` + Semiconductor Engineering secondary coverage `semieng-2026-bare-ai-monitors`).
  - CLI commands in [`src/reading_list/cli.py`](file:///Users/bill/src/reading-list/src/reading_list/cli.py): `build`, `update`, `classify`, `add`, `list`, `status`, `publish-db`, and `research`.
- **Published knowledge base & GitHub Pages repository ([`../reading-db`](file:///Users/bill/src/reading-db)):**
  - Populated with **16 documents** in [`../reading-db/corpus.json`](file:///Users/bill/src/reading-db/corpus.json), including:
    1. BARE-AI 28nm hardware monitors (`arxiv-2610.08739v2` + secondary coverage)
    2. Fil-C Rowhammer resilience (`arxiv-2610.33748` + secondary coverage)
    3. *"Formal verification languages in chip and semiconductor design"* (`arxiv-2208.03699` UCLID5, `arxiv-2503.19174` AssertionForge, `arxiv-2604.23100` ProofLoop, `arxiv-2609.26751` EquivSVA, and `research-formal-verification-languages-in-chip-and-se`)
    4. *"SAT and SMT solvers applications in software development, graph analysis, and ontologies"* (`arxiv-1402.4677` MonoSAT, `arxiv-2201.04663` cvc5, `arxiv-1610.00502` Symbolic Execution Survey, `arxiv-1507.01763` SAT/SMT for Description Logics & Ontologies, and `research-sat-and-smt-solvers-applications-in-software`).
- **Synoptic Domain & Slice Navigator ([`src/reading_list/site.py`](file:///Users/bill/src/reading-list/src/reading_list/site.py)):**
  - Multi-dimension top-level slice tabs (`#slice-dimension-tabs`): *By Domain Hierarchy*, *By Technology Area*, *By Reading Stage*, *By Document Type*.
  - Interactive breadcrumb drill-down bar (`#breadcrumb-bar`) with L1/L2/L3 subcategory scoping.
  - Scoped interactive SVG Knowledge Graph (`#kg-svg`) with node dragging, canvas pan/zoom, legend toggles, 1-hop neighborhood highlighting, and full-page (`#fullscreen-graph-btn` / `Esc`) toggle.
  - Scoped Word Cloud (`#word-cloud`) and OntoLogic Sub-Hierarchy (`#taxonomy-list`) recomputed dynamically for the active slice.
  - Synoptic compact **Table View** (`#view-table-btn`, default, paginated 8/page) + **Card View** (`#view-cards-btn`) toggle.

## Failed / blocked (with root cause)
- None currently blocked.

## Bugs fixed this session (so they aren't reintroduced)
- [`src/reading_list/site.py`](file:///Users/bill/src/reading-list/src/reading_list/site.py): Avoided `Element.closest()` on SVG elements in Safari/WebKit by walking parent nodes explicitly, and fixed pointer capture so clicking nodes vs. dragging nodes distinguishes click-to-filter (`<5px` travel) from drag-to-reposition.
- [`tests/test_smoke.py`](file:///Users/bill/src/reading-list/tests/test_smoke.py): Aligned element ID assertions (`#domain-cards-grid`, `#fullscreen-graph-btn`) and synthesized note ID (`research-formal-verification-languages-in-chip-and-se`) with the generator output.

## State that may have changed
- Both `/Users/bill/src/reading-list` and `/Users/bill/src/reading-db` have clean working trees synced with `origin/main` as of `2026-11-07`.

## Next steps (exact commands, in order)
1. Verify baseline test suite on resume:
   ```bash
   PYTHONPATH=src python3 -m unittest discover -s tests -v
   ```
2. Research a new topic and publish directly to `../reading-db`:
   ```bash
   PYTHONPATH=src python3 -m reading_list.cli research --topic "<topic>" --db-dir ../reading-db
   ```
3. Or rebuild and publish `../reading-db` after manual edits to `../reading-db/corpus.json`:
   ```bash
   PYTHONPATH=src python3 -m reading_list.cli publish-db --db-dir ../reading-db
   ```

## Open questions
- None. Ready for new research topics, additional corpus ingestion, or OntoLogic schema integration.
