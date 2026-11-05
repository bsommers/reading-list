# Input Directory (`input/`)

Read-only source documents, metadata manifests, and downloaded academic/technical papers for the reading list. All files in this directory except `README.md` are git-ignored.

## Seed Sources

1. **Technical Article (Semiconductor Engineering)**
   - **Title:** On-Chip Monitors Detect Bit-Flip Attacks in AI Accelerators (UF, UT Dallas, RPI)
   - **URL:** `https://semiengineering.com/on-chip-monitors-detect-bit-flip-attacks-in-ai-accelerators-uf-ut-dallas-rpi/`
   - **Document ID:** `semieng-2026-bare-ai-monitors`
   - **Type:** `technical_article`
   - **Reports On:** `arxiv-2610.08739v2`

2. **Academic Paper (arXiv Preprint)**
   - **Title:** BARE-AI: Bit-Flip Attack Resilience in AI Hardware through Built-in Performance Monitors
   - **URL:** `https://arxiv.org/abs/2610.08739v2`
   - **PDF URL:** `https://arxiv.org/pdf/2610.08739v2`
   - **Pinned Version:** `arXiv:2610.08739v2` (published `2026-10-06`, updated `2026-10-07`, primary category `cs.CR`)
   - **Authors:** Habibur Rahaman, Swastik Bhattacharya, Sanjay Das, Kanad Basu, Swarup Bhunia
   - **Institutions:** University of Florida (UF), University of Texas at Dallas (UT Dallas), Rensselaer Polytechnic Institute (RPI)
   - **Document ID:** `arxiv-2610.08739v2`
   - **Type:** `academic_paper`

## Populating `input/`

To materialize the seed corpus into `input/corpus.json` (or add new JSON/Markdown documents):

```bash
PYTHONPATH=src python3 -m reading_list.cli seed-input --output input/corpus.json
```

Tracked test fixtures mirroring the initial seed corpus live in `tests/fixtures/seed_corpus.json`.
