"""Importer and knowledge-graph builder for the `kitsumiko/papers` AI/ML Research Curriculum.

Preserves all original references, citations, links, annotations, chronological dates,
and Apache-2.0 acknowledgements back to https://github.com/kitsumiko/papers.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

from reading_list.enrich import extract_arxiv_id
from reading_list.models import Document, DocumentRelation

KITSUMIKO_REPO_URL = "https://github.com/kitsumiko/papers"
KITSUMIKO_LICENSE = "Apache-2.0"

AREAS: tuple[tuple[str, str, str], ...] = (
    ("classics", "🏺", "Classics: Historical Roots of Neural Networks"),
    ("foundations", "🏗️", "Foundations of Deep Learning & Representations"),
    ("language-models", "🤖", "Large Language Models"),
    ("attention", "⚡", "Attention Mechanisms & Context"),
    ("retrieval", "🔍", "Retrieval & RAG Systems"),
    ("reasoning", "🧠", "Reasoning & Agentic Systems"),
    ("architectures", "🏛️", "Novel Architectures & Theory"),
    ("interpretability", "🔬", "Interpretability & Evaluation"),
    ("safety", "🛡️", "Security, Safety & Robustness"),
    ("advanced", "🎯", "Advanced Topics & Automated AI Research"),
    ("probabilistic", "🎲", "Probabilistic & Diffusion Models"),
    ("vision", "👁️", "Vision & Multimodal Systems"),
    ("hardware", "⚙️", "Hardware & Systems"),
    ("human-ai-interaction", "🧠", "Human-AI Interaction & Cognition"),
    ("policy", "📜", "Policy, Governance & Societal Impact"),
)

# Map each kitsumiko area stem to domain-relevant keywords so every paper in that area
# connects cleanly to the reading-list conceptual taxonomy.
AREA_TAXONOMY_CONTEXT: dict[str, str] = {
    "classics": "artificial intelligence neural networks deep learning architectures",
    "foundations": "deep neural networks large language models tokenization transformer",
    "language-models": "large language models pretraining megatron zero scaling laws flashattention",
    "attention": "flashattention sparse attention long context kv cache transformer",
    "retrieval": "retrieval-augmented rag federated learning large language models",
    "reasoning": "chain-of-thought latent reasoning react reflexion agentic multi-agent rlhf ppo",
    "architectures": "state-space model mamba rwkv kolmogorov-arnold kan neural tangent kernel lattice deduction",
    "interpretability": "mechanistic interpretability superposition sparse autoencoder calibration truthfulqa",
    "safety": "security adversarial prompt injection jailbreaking red teaming guardrail constitutional ai",
    "advanced": "artificial intelligence agentic automated reasoning deep neural networks",
    "probabilistic": "diffusion model denoising diffusion probabilistic programming variational inference bayesian",
    "vision": "vision transformers clip segment anything multimodal deep neural networks",
    "hardware": "hardware ai accelerators gpu datapath memory inference",
    "human-ai-interaction": "human-ai automation bias governance artificial intelligence",
    "policy": "governance regulation eu ai act nist ai rmf model risk management compliance",
}

URL_PAT = r"(?:[^()\s]|\([^()\s]*\))+"
ENTRY_RE = re.compile(rf"^(\d+)\.\s+((?:📄|🔒)\s+)?\[(.+?)\]\(({URL_PAT})\)(.*)$")
BULLET_RE = re.compile(rf"^- ((?:📄|🔒)\s+)?\[(.+?)\]\(({URL_PAT})\)(.*)$")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:52].strip("-") or "paper"


def _canon_url(url: str) -> str:
    arxiv_id = extract_arxiv_id(url)
    if arxiv_id:
        base_id = re.sub(r"v\d+$", "", arxiv_id)
        return f"arxiv:{base_id}"
    return url.replace("http://", "https://").rstrip("/")


def _parse_citation_tail(rest: str) -> tuple[list[str], str, str]:
    """Extract `(authors, year, extra_note)` from the trailing `(Authors, YYYY)` string."""
    cleaned = rest.strip()
    paren_matches = list(re.finditer(r"\(([^()]+)\)", cleaned))
    if not paren_matches:
        return ["kitsumiko/papers Curated Collection"], "2025", cleaned

    first_paren = paren_matches[0].group(1).strip()
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", first_paren)
    year = year_match.group(1) if year_match else "2025"

    # Extract author or issuing organization before the year
    if year_match:
        before_year = first_paren[: year_match.start()].strip(" ,;-—")
    else:
        before_year = first_paren.strip(" ,;-—")

    if not before_year:
        authors = ["kitsumiko/papers Curated Collection"]
    else:
        # Clean up things like "signed May 14," or "adopted October"
        before_year = re.sub(
            r"\b(?:signed|published|issued|adopted|released|updated|effective)\b.*$",
            "",
            before_year,
            flags=re.IGNORECASE,
        ).strip(" ,;-—")
        if not before_year:
            before_year = first_paren
        if "&" in before_year and "et al" not in before_year:
            authors = [a.strip() for a in before_year.split("&") if a.strip()]
        else:
            authors = [before_year]

    extra = cleaned[paren_matches[0].end() :].strip(" -—")
    return authors, year, extra


def _rewrite_glossary_links(text: str) -> str:
    """Convert relative `glossary.md#...` or `learning/...` links to absolute kitsumiko/papers GitHub URLs."""
    def _repl(m: re.Match[str]) -> str:
        label, target = m.group(1), m.group(2)
        if target.startswith("http://") or target.startswith("https://"):
            return m.group(0)
        clean_target = target.lstrip("./")
        if clean_target.startswith("../"):
            clean_target = clean_target[3:]
        elif not clean_target.startswith("learning/"):
            clean_target = f"learning/{clean_target}"
        return f"[{label}]({KITSUMIKO_REPO_URL}/blob/main/{clean_target})"

    return MD_LINK_RE.sub(_repl, text)


def parse_bydate_index(bydate_path: Path) -> dict[str, str]:
    """Return a map from canonical URL key to `YYYY-MM` or `YYYY` from `by-date.md`."""
    dates_by_canon: dict[str, str] = {}
    if not bydate_path.exists():
        return dates_by_canon

    curr_year: str | None = None
    curr_month: str | None = None
    for raw_line in bydate_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## ") and not line.startswith("### "):
            m_y = re.match(r"^##\s+(\d{4})\b", line)
            curr_year = m_y.group(1) if m_y else None
            curr_month = None
        elif line.startswith("### "):
            m_ym = re.match(r"^###\s+(\d{4})\.(\d{2})\b", line)
            if m_ym:
                curr_year = m_ym.group(1)
                curr_month = m_ym.group(2)
        else:
            b = BULLET_RE.match(line)
            if b and curr_year:
                url = b.group(3)
                cu = _canon_url(url)
                date_str = f"{curr_year}-{curr_month}" if curr_month else curr_year
                dates_by_canon[cu] = date_str
    return dates_by_canon


def build_kitsumiko_corpus(source_repo_dir: Path) -> list[Document]:
    """Parse all 15 topic areas and `by-date.md` from `kitsumiko/papers` into `Document` objects."""
    learning_dir = source_repo_dir / "learning"
    bydate_path = source_repo_dir / "by-date.md"
    dates_by_canon = parse_bydate_index(bydate_path)

    documents: list[Document] = []
    doc_by_canon: dict[str, Document] = {}
    area_note_ids: list[str] = []
    seen_doc_ids: set[str] = set()

    for stem, emoji, area_title in AREAS:
        topic_path = learning_dir / f"{stem}.md"
        if not topic_path.exists():
            continue

        lines = topic_path.read_text(encoding="utf-8").splitlines()
        overview_lines: list[str] = []
        sections: list[dict[str, Any]] = []
        current_sec: dict[str, Any] | None = None

        for idx, line in enumerate(lines, start=1):
            if line.startswith("## "):
                current_sec = {
                    "name": line[3:].strip(),
                    "goal": "",
                    "entries": [],
                }
                sections.append(current_sec)
            elif current_sec is None:
                if line.startswith("**Overview**:") or (overview_lines and line.strip() and not line.startswith("---") and not line.startswith("[←")):
                    overview_lines.append(line.strip())
            else:
                if line.strip().startswith("**Goal**:"):
                    current_sec["goal"] = line.strip().replace("**Goal**:", "").strip()
                    continue
                m = ENTRY_RE.match(line)
                if m:
                    current_sec["entries"].append(
                        {
                            "num": int(m.group(1)),
                            "line": idx,
                            "emoji": (m.group(2) or "").strip(),
                            "title": m.group(3).strip(),
                            "url": m.group(4).strip(),
                            "rest": m.group(5).strip(),
                            "cont": [],
                        }
                    )
                elif current_sec["entries"] and re.match(r"^\s+-\s", line):
                    current_sec["entries"][-1]["cont"].append(line.strip()[2:].strip())

        area_doc_ids: list[str] = []
        overview_text = _rewrite_glossary_links(" ".join(overview_lines)) or (
            f"Curated research papers and foundational resources in {area_title}."
        )

        for sec in sections:
            sec_name = sec["name"]
            sec_goal = sec["goal"]
            for entry in sec["entries"]:
                title = entry["title"]
                url = entry["url"]
                emoji_marker = entry["emoji"]
                authors, fallback_year, extra_venue = _parse_citation_tail(entry["rest"])
                cu = _canon_url(url)
                if cu in doc_by_canon:
                    existing_doc = doc_by_canon[cu]
                    area_doc_ids.append(existing_doc.doc_id)
                    if stem not in existing_doc.tags:
                        existing_doc.tags.append(stem)
                    existing_doc.identifiers["kitsumiko_secondary_area"] = stem
                    existing_doc.identifiers["kitsumiko_secondary_source_url"] = (
                        f"{KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md#L{entry['line']}"
                    )
                    continue

                published_date = dates_by_canon.get(cu, fallback_year)

                arxiv_id = extract_arxiv_id(url)
                if arxiv_id:
                    base_arxiv = re.sub(r"v\d+$", "", arxiv_id)
                    base_doc_id = f"arxiv-{base_arxiv}"
                elif emoji_marker == "📄" or stem == "policy":
                    base_doc_id = f"policy-{_slugify(title)}"
                else:
                    base_doc_id = f"paper-{_slugify(title)}"

                doc_id = base_doc_id
                suffix = 2
                while doc_id in seen_doc_ids:
                    doc_id = f"{base_doc_id}-{suffix}"
                    suffix += 1
                seen_doc_ids.add(doc_id)
                area_doc_ids.append(doc_id)

                why_parts: list[str] = []
                note_parts: list[str] = []
                for bullet in entry["cont"]:
                    rewritten = _rewrite_glossary_links(bullet)
                    if rewritten.lower().startswith("*why*:"):
                        why_parts.append(rewritten[6:].strip())
                    elif rewritten.lower().startswith("*note*:"):
                        note_parts.append(rewritten[7:].strip())
                    else:
                        why_parts.append(rewritten)

                why_text = " ".join(why_parts) or f"Selected curriculum paper in {area_title} ({sec_name})."
                note_text = " ".join(note_parts)

                is_policy = emoji_marker == "📄" or (stem == "policy" and not arxiv_id)
                is_paywalled = emoji_marker == "🔒"
                doc_type = "technical_paper" if is_policy else "academic_paper"

                area_context_kw = AREA_TAXONOMY_CONTEXT.get(stem, "")
                content_sections = [
                    f"## Why It Matters & Core Contribution\n{why_text}",
                    (
                        f"## Curriculum Placement & Context\n"
                        f"Part of the **{area_title}** curriculum area under section **{sec_name}**"
                        + (f" (Section Goal: *{sec_goal}*)." if sec_goal else ".")
                        + (f" Additional Note: {note_text}" if note_text else "")
                        + (f" Venue/Citation Context: {extra_venue}." if extra_venue else "")
                        + f" Domain keywords: {area_context_kw}."
                    ),
                    (
                        f"## Attribution & Source Links\n"
                        f"Curated and annotated in [`kitsumiko/papers`]({KITSUMIKO_REPO_URL}) "
                        f"([`learning/{stem}.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md#L{entry['line']}), "
                        f"[`by-date.md`]({KITSUMIKO_REPO_URL}/blob/main/by-date.md)) under the {KITSUMIKO_LICENSE} License. "
                        f"Primary link: [{title}]({url})."
                    ),
                ]

                identifiers: dict[str, str] = {
                    "kitsumiko_repo": KITSUMIKO_REPO_URL,
                    "kitsumiko_area": stem,
                    "kitsumiko_section": sec_name,
                    "kitsumiko_source_url": f"{KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md#L{entry['line']}",
                    "kitsumiko_bydate_url": f"{KITSUMIKO_REPO_URL}/blob/main/by-date.md",
                    "license": KITSUMIKO_LICENSE,
                }
                if arxiv_id:
                    identifiers["arxiv"] = arxiv_id
                    identifiers["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"
                if is_paywalled:
                    identifiers["access"] = "paywalled"
                if is_policy:
                    identifiers["document_category"] = "policy_governance"

                tags = [
                    "kitsumiko-papers",
                    stem,
                    _slugify(sec_name)[:28],
                ]
                if is_policy:
                    tags.append("policy-document")
                if is_paywalled:
                    tags.append("paywalled")
                if arxiv_id:
                    tags.append("arxiv")

                priority = "high" if ("**" in why_text or published_date.startswith("2026")) else "medium"
                notes_summary = re.sub(r"\*\*([^*]+)\*\*", r"\1", why_text)
                if len(notes_summary) > 220:
                    notes_summary = notes_summary[:217] + "..."

                new_doc = Document(
                    doc_id=doc_id,
                    title=title,
                    doc_type=doc_type,
                    url=url,
                    published_date=published_date,
                    authors=authors,
                    institutions=[f"kitsumiko/papers — {area_title}"],
                    identifiers=identifiers,
                    relations=[],
                    content="\n\n".join(content_sections),
                    reading_status="to-read",
                    priority=priority,
                    tags=tags,
                    notes=f"[{area_title} > {sec_name}] {notes_summary} (Source: kitsumiko/papers)",
                )
                doc_by_canon[cu] = new_doc
                documents.append(new_doc)

        # Create an Area Synthesis Note linking all papers in this curriculum area
        area_note_id = f"curriculum-area-{stem}"
        area_note_ids.append(area_note_id)
        section_names = ", ".join(s["name"] for s in sections)
        documents.append(
            Document(
                doc_id=area_note_id,
                title=f"Curriculum Area Guide: {emoji} {area_title} ({len(area_doc_ids)} Papers)",
                doc_type="note",
                url=f"{KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md",
                published_date="2026-11",
                authors=["kitsumiko/papers Contributors"],
                institutions=["kitsumiko/papers AI/ML Research Curriculum"],
                identifiers={
                    "kitsumiko_repo": KITSUMIKO_REPO_URL,
                    "kitsumiko_area": stem,
                    "kitsumiko_source_url": f"{KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md",
                    "license": KITSUMIKO_LICENSE,
                },
                relations=[DocumentRelation("REPORTS_ON", pid) for pid in area_doc_ids],
                content=(
                    f"## Curriculum Area Overview: {area_title}\n"
                    f"{overview_text}\n\n"
                    f"## Subtopics & Pedagogical Structure\n"
                    f"This area comprises **{len(area_doc_ids)} curated papers and documents** organized across "
                    f"{len(sections)} subtopics: {section_names}. Domain focus: {AREA_TAXONOMY_CONTEXT.get(stem, '')}.\n\n"
                    f"## Attribution & Upstream Reference\n"
                    f"Adapted from [`learning/{stem}.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/{stem}.md) in "
                    f"[`kitsumiko/papers`]({KITSUMIKO_REPO_URL}) ({KITSUMIKO_LICENSE} License). "
                    f"See also the [Learning Path]({KITSUMIKO_REPO_URL}/blob/main/learning-path.md) and "
                    f"[161-Term AI/ML Glossary]({KITSUMIKO_REPO_URL}/blob/main/learning/glossary.md)."
                ),
                reading_status="read",
                priority="high",
                tags=["curriculum-area", "kitsumiko-papers", stem],
                notes=f"Topical curriculum index for {area_title} ({len(area_doc_ids)} entries) from kitsumiko/papers.",
            )
        )

    # Create Master Curriculum Overview Note linking all 15 Area Guides
    documents.append(
        Document(
            doc_id="curriculum-kitsumiko-master-path",
            title="AI/ML Research Curriculum Master Index & Learning Path (kitsumiko/papers — 320 Papers across 15 Areas)",
            doc_type="note",
            url=KITSUMIKO_REPO_URL,
            published_date="2026-11",
            authors=["kitsumiko/papers Contributors"],
            institutions=["kitsumiko/papers AI/ML Research Curriculum"],
            identifiers={
                "kitsumiko_repo": KITSUMIKO_REPO_URL,
                "kitsumiko_learning_path": f"{KITSUMIKO_REPO_URL}/blob/main/learning-path.md",
                "kitsumiko_bydate": f"{KITSUMIKO_REPO_URL}/blob/main/by-date.md",
                "kitsumiko_glossary": f"{KITSUMIKO_REPO_URL}/blob/main/learning/glossary.md",
                "license": KITSUMIKO_LICENSE,
            },
            relations=[DocumentRelation("CITES", aid) for aid in area_note_ids],
            content=(
                "## Collection Overview & Mission\n"
                "A curated, pedagogically organized collection of **320 essential research papers and policy documents** "
                "spanning the landscape of artificial intelligence and machine learning from 1936 to 2026 across 15 topic areas "
                "and 161 glossary terms.\n\n"
                "## Curated Role-Based Learning Tracks\n"
                "- **Comprehensive Track**: Classics → Foundations → Language Models → Attention → Retrieval → Reasoning → Architectures → Interpretability → Safety → Advanced → Probabilistic → Vision → Hardware → Human-AI Interaction → Policy.\n"
                "- **ML Practitioner Track**: Language Models → Attention → Reasoning → Interpretability (+ Retrieval & Safety).\n"
                "- **Engineer Track**: Language Models, Attention, Interpretability, Safety, and Hardware & Systems.\n"
                "- **Security Specialist Track**: Foundations & Language Models → Safety & Security → Interpretability & Policy.\n\n"
                "## Full Attribution & License\n"
                f"All paper selections, area structures, and *Why* annotations originate from "
                f"[`kitsumiko/papers`]({KITSUMIKO_REPO_URL}), licensed under the [Apache License 2.0]({KITSUMIKO_REPO_URL}/blob/main/LICENSE). "
                f"Interactive knowledge-graph indexing, OntoLogic JSON-LD export, and semantic chunking generated by "
                f"[`bsommers/reading-list`](https://github.com/bsommers/reading-list)."
            ),
            reading_status="read",
            priority="high",
            tags=["kitsumiko-papers", "learning-path", "curriculum-master", "glossary"],
            notes="Master learning path and attribution hub for the 320-paper kitsumiko/papers collection.",
        )
    )

    return documents


def copy_upstream_reference_files(source_repo_dir: Path, target_db_dir: Path) -> None:
    """Copy `LICENSE`, `learning/`, `learning-path.md`, and `by-date.md` into `target_db_dir` for complete reference preservation."""
    target_db_dir.mkdir(parents=True, exist_ok=True)
    for fname in ("LICENSE", "learning-path.md", "by-date.md", "CONTRIBUTING.md"):
        src = source_repo_dir / fname
        if src.exists():
            shutil.copyfile(src, target_db_dir / fname)

    src_learning = source_repo_dir / "learning"
    dst_learning = target_db_dir / "learning"
    if src_learning.exists():
        if dst_learning.exists():
            shutil.rmtree(dst_learning)
        shutil.copytree(src_learning, dst_learning)

    notice_path = target_db_dir / "NOTICE.md"
    notice_path.write_text(
        "# Attribution & Notice (`ai-curriculum-db`)\n\n"
        "This knowledge-graph database and interactive GitHub Pages explorer is built directly from the\n"
        "**[`kitsumiko/papers`](https://github.com/kitsumiko/papers)** AI/ML Research Papers Collection.\n\n"
        "- **Upstream Repository:** [`https://github.com/kitsumiko/papers`](https://github.com/kitsumiko/papers)\n"
        "- **Upstream Curriculum & Learning Path:** [`learning-path.md`](learning-path.md) "
        "([upstream](https://github.com/kitsumiko/papers/blob/main/learning-path.md))\n"
        "- **Upstream Chronological Index (1936–2026):** [`by-date.md`](by-date.md) "
        "([upstream](https://github.com/kitsumiko/papers/blob/main/by-date.md))\n"
        "- **Upstream 161-Term AI/ML Glossary:** [`learning/glossary.md`](learning/glossary.md) "
        "([upstream](https://github.com/kitsumiko/papers/blob/main/learning/glossary.md))\n"
        "- **Upstream License:** [Apache License 2.0](LICENSE)\n"
        "- **Knowledge Graph & Indexing Engine:** [`bsommers/reading-list`](https://github.com/bsommers/reading-list)\n"
        "- **Sibling Hardware Security / Formal Verification / SMT DB:** [`bsommers/reading-db`](https://github.com/bsommers/reading-db)\n\n"
        "## License & Copyright\n\n"
        "The curation, organization, and annotations from [`kitsumiko/papers`](https://github.com/kitsumiko/papers) "
        "are licensed under the [Apache License 2.0](LICENSE). The linked research papers and policy documents "
        "remain under their original licenses and copyrights held by their respective authors and publishers.\n",
        encoding="utf-8",
    )


def write_curriculum_db_readme(target_db_dir: Path, documents: list[Document]) -> None:
    """Write a comprehensive `README.md` for `../ai-curriculum-db` with full attribution to `kitsumiko/papers`."""
    paper_count = sum(1 for d in documents if d.doc_type != "note")
    note_count = sum(1 for d in documents if d.doc_type == "note")

    readme_content = f"""# AI/ML Research Curriculum Knowledge Graph (`ai-curriculum-db`)

[![Upstream: kitsumiko/papers](https://img.shields.io/badge/upstream-kitsumiko%2Fpapers-blue.svg)]({KITSUMIKO_REPO_URL})
[![Papers](https://img.shields.io/badge/papers-{paper_count}-blue.svg)](by-date.md)
[![Areas](https://img.shields.io/badge/learning-15_areas-green.svg)](learning-path.md)
[![Glossary](https://img.shields.io/badge/glossary-161_terms-purple.svg)](learning/glossary.md)
[![License](https://img.shields.io/badge/license-Apache_2.0-orange.svg)](LICENSE)

Interactive **Knowledge Graph**, **OntoLogic JSON-LD** property graph, semantic chunk index, conceptual taxonomy, and **GitHub Pages** explorer for the **[`kitsumiko/papers`]({KITSUMIKO_REPO_URL})** AI/ML Research Curriculum (**{paper_count} curated papers & policy documents** across **15 learning areas**, 1936–2026), generated by **[`bsommers/reading-list`](https://github.com/bsommers/reading-list)**.

- **Live Interactive Dashboard:** **[`https://bsommers.github.io/ai-curriculum-db/`](https://bsommers.github.io/ai-curriculum-db/)**
- **Upstream Curated Collection (Source of Truth):** **[`https://github.com/kitsumiko/papers`]({KITSUMIKO_REPO_URL})**
- **Sibling Focused Research DB (Hardware Security, RTL Verification & SAT/SMT):** **[`https://github.com/bsommers/reading-db`](https://github.com/bsommers/reading-db)**
- **Tooling & CLI Engine:** **[`https://github.com/bsommers/reading-list`](https://github.com/bsommers/reading-list)**

---

## 🙏 Attribution & Acknowledgements (`kitsumiko/papers`)

All **320 paper selections**, **15 pedagogical learning areas**, **chronological timelines (1936–2026)**, **161 glossary definitions**, and **\"Why it matters\" annotations** in this database originate from **[`kitsumiko/papers`]({KITSUMIKO_REPO_URL})** under the **[Apache License 2.0](LICENSE)** (see [`NOTICE.md`](NOTICE.md)).

 All original Markdown curriculum pages are preserved directly in this repository alongside the generated knowledge-graph artifacts:
- 📚 **[Learning Path & Role Tracks](learning-path.md)** ([upstream]({KITSUMIKO_REPO_URL}/blob/main/learning-path.md))
- 📅 **[Chronological Index (1936–2026)](by-date.md)** ([upstream]({KITSUMIKO_REPO_URL}/blob/main/by-date.md))
- 📖 **[161-Term AI/ML Glossary](learning/glossary.md)** ([upstream]({KITSUMIKO_REPO_URL}/blob/main/learning/glossary.md))

### The 15 Curriculum Areas (`learning/*.md`)

| Area | Preserved Markdown | Upstream Source |
|---|---|---|
| 🏺 **Classics** | [`learning/classics.md`](learning/classics.md) | [`kitsumiko/papers/learning/classics.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/classics.md) |
| 🏗️ **Foundations** | [`learning/foundations.md`](learning/foundations.md) | [`kitsumiko/papers/learning/foundations.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/foundations.md) |
| 🤖 **Language Models** | [`learning/language-models.md`](learning/language-models.md) | [`kitsumiko/papers/learning/language-models.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/language-models.md) |
| ⚡ **Attention** | [`learning/attention.md`](learning/attention.md) | [`kitsumiko/papers/learning/attention.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/attention.md) |
| 🔍 **Retrieval & RAG** | [`learning/retrieval.md`](learning/retrieval.md) | [`kitsumiko/papers/learning/retrieval.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/retrieval.md) |
| 🧠 **Reasoning & Agents** | [`learning/reasoning.md`](learning/reasoning.md) | [`kitsumiko/papers/learning/reasoning.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/reasoning.md) |
| 🏛️ **Architectures** | [`learning/architectures.md`](learning/architectures.md) | [`kitsumiko/papers/learning/architectures.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/architectures.md) |
| 🔬 **Interpretability** | [`learning/interpretability.md`](learning/interpretability.md) | [`kitsumiko/papers/learning/interpretability.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/interpretability.md) |
| 🛡️ **Safety & Security** | [`learning/safety.md`](learning/safety.md) | [`kitsumiko/papers/learning/safety.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/safety.md) |
| 🎯 **Advanced** | [`learning/advanced.md`](learning/advanced.md) | [`kitsumiko/papers/learning/advanced.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/advanced.md) |
| 🎲 **Probabilistic** | [`learning/probabilistic.md`](learning/probabilistic.md) | [`kitsumiko/papers/learning/probabilistic.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/probabilistic.md) |
| 👁️ **Vision & Multimodal** | [`learning/vision.md`](learning/vision.md) | [`kitsumiko/papers/learning/vision.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/vision.md) |
| ⚙️ **Hardware & Systems** | [`learning/hardware.md`](learning/hardware.md) | [`kitsumiko/papers/learning/hardware.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/hardware.md) |
| 🧠 **Human-AI Interaction** | [`learning/human-ai-interaction.md`](learning/human-ai-interaction.md) | [`kitsumiko/papers/learning/human-ai-interaction.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/human-ai-interaction.md) |
| 📜 **Policy & Governance** | [`learning/policy.md`](learning/policy.md) | [`kitsumiko/papers/learning/policy.md`]({KITSUMIKO_REPO_URL}/blob/main/learning/policy.md) |

---

## Published Knowledge-Graph Artifacts

| File | Description |
|---|---|
| `index.html` | Interactive GitHub Pages dashboard (Synoptic Domain Navigator, Knowledge Graph SVG, Word Cloud filter, Taxonomy browser, and Semantic Chunk inspector) |
| `corpus.json` | Full structured reading-list corpus ({len(documents)} documents: {paper_count} papers/policies + {note_count} curriculum synthesis guides) with `identifiers.kitsumiko_source_url` provenance |
| `knowledge_graph.json` | OntoLogic-ready JSON-LD property graph (`@context`, nodes, and typed edges) |
| `chunks.json` | Semantically chunked sections for every document with key terms, concepts, and taxonomy paths |
| `taxonomy_tree.json` | Hierarchical conceptual taxonomy and technology-area index |
| `word_cloud.json` | Normalized global and per-document word-cloud frequency weights |
| `summary.md` | Markdown report with dynamic Mermaid taxonomy & document graph |
| `NOTICE.md` & `LICENSE` | Apache 2.0 license and upstream attribution to [`kitsumiko/papers`]({KITSUMIKO_REPO_URL}) |

---

## Updating From `reading-list`

From the sibling `../reading-list` repository, run:

```bash
PYTHONPATH=src python3 -m reading_list.cli publish-db -d ../ai-curriculum-db
```
"""
    (target_db_dir / "README.md").write_text(readme_content, encoding="utf-8")
