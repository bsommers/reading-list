"""Command-line entry point for quick document tracking, content classification, research, and knowledge-graph builds.

Supports ergonomic invocation in the form:
    python3 -m reading_list.cli <command> [switches] [subcommand(s)]

Examples:
    python3 -m reading_list.cli research -d ../reading-db --topic "SAT and SMT solvers" add
    python3 -m reading_list.cli research -d ../reading-db add "Formal verification languages"
    python3 -m reading_list.cli add -d ../reading-db --title "Paper Title" --url "https://arxiv.org/abs/2201.04663" --type academic_paper
    python3 -m reading_list.cli list -d ../reading-db --status to-read
    python3 -m reading_list.cli status -d ../reading-db arxiv-2201.04663 --set read --priority high
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Sequence

from reading_list.chunker import (
    build_word_cloud,
    chunk_document,
    classify_content,
)
from reading_list.enrich import (
    enrich_document,
    extract_arxiv_id,
    fetch_arxiv_metadata,
    structure_abstract_into_sections,
    sync_readme_corpus_section,
)
from reading_list.graph import (
    build_knowledge_graph,
    build_taxonomy_index,
    render_summary_markdown,
)
from reading_list.kitsumiko import (
    build_kitsumiko_corpus,
    copy_upstream_reference_files,
    write_curriculum_db_readme,
)
from reading_list.models import Document, DocumentRelation, SemanticChunk
from reading_list.research import research_topic
from reading_list.site import render_github_pages_html

DEFAULT_FIXTURE = Path("tests/fixtures/seed_corpus.json")
DEFAULT_CORPUS = Path("input/corpus.json")
DEFAULT_OUTPUT = Path("output")
DEFAULT_README = Path("README.md")
DEFAULT_SISTER_DB = Path("../reading-db")

PRIMARY_COMMANDS = {
    "research",
    "add",
    "update",
    "sync",
    "publish-db",
    "publish",
    "build",
    "classify",
    "list",
    "status",
    "seed-input",
    "import-curriculum",
}

CHAINABLE_SUBCOMMANDS = {
    "add",
    "research",
    "update",
    "sync",
    "publish",
    "publish-db",
    "build",
    "list",
    "push",
    "status",
}


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48].strip("-") or "doc-entry"


def ensure_corpus_file(corpus_path: Path, fixture_path: Path = DEFAULT_FIXTURE) -> Path:
    """Ensure the mutable corpus JSON exists, seeding from the fixture if needed."""
    if not corpus_path.exists():
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        if fixture_path.exists():
            shutil.copyfile(fixture_path, corpus_path)
        else:
            save_corpus(corpus_path, [])
    return corpus_path


def load_corpus(path: Path) -> list[Document]:
    """Load documents from a JSON corpus manifest."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Document.from_dict(item) for item in raw.get("documents", [])]


def save_corpus(path: Path, documents: list[Document], version: str = "0.1.0") -> None:
    """Save documents deterministically to a JSON corpus manifest."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "corpus_version": version,
        "documents": [doc.to_dict() for doc in documents],
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_build(input_path: Path, output_dir: Path) -> dict[str, Path]:
    """Chunk documents, build word clouds, taxonomy index, knowledge graph, and GitHub Pages HTML into `output_dir`."""
    documents = load_corpus(input_path)
    chunks_by_doc: dict[str, list[SemanticChunk]] = {
        doc.doc_id: chunk_document(doc) for doc in documents
    }

    word_cloud = build_word_cloud(documents, chunks_by_doc)
    kg = build_knowledge_graph(documents, chunks_by_doc)
    taxonomy_index = build_taxonomy_index(documents, chunks_by_doc)
    summary_md = render_summary_markdown(documents, chunks_by_doc, word_cloud, kg)
    site_html = render_github_pages_html(
        documents, chunks_by_doc, word_cloud, taxonomy_index, kg
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    chunks_path = output_dir / "chunks.json"
    chunks_payload = {
        doc_id: [c.to_dict() for c in chunks]
        for doc_id, chunks in chunks_by_doc.items()
    }
    chunks_path.write_text(
        json.dumps(chunks_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    wc_path = output_dir / "word_cloud.json"
    wc_path.write_text(
        json.dumps(word_cloud, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    tax_path = output_dir / "taxonomy_tree.json"
    tax_path.write_text(
        json.dumps(taxonomy_index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    kg_path = output_dir / "knowledge_graph.json"
    kg_path.write_text(
        json.dumps(kg.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary_path = output_dir / "summary.md"
    summary_path.write_text(summary_md, encoding="utf-8")

    index_html_path = output_dir / "index.html"
    index_html_path.write_text(site_html, encoding="utf-8")

    nojekyll_path = output_dir / ".nojekyll"
    nojekyll_path.write_text("", encoding="utf-8")

    return {
        "chunks": chunks_path,
        "word_cloud": wc_path,
        "taxonomy_tree": tax_path,
        "knowledge_graph": kg_path,
        "summary": summary_path,
        "index_html": index_html_path,
    }


def run_update_pipeline(
    corpus_path: Path = DEFAULT_CORPUS,
    fixture_path: Path = DEFAULT_FIXTURE,
    output_dir: Path = DEFAULT_OUTPUT,
    readme_path: Path = DEFAULT_README,
    sync_fixture: bool = True,
) -> dict[str, Any]:
    """Execute the full 3-step update: (1) enrich & classify, (2) sync tracked corpus & README, (3) rebuild outputs."""
    ensure_corpus_file(corpus_path, fixture_path)
    docs = load_corpus(corpus_path)

    enriched_docs: list[Document] = []
    enriched_ids: list[str] = []
    for doc in docs:
        updated_doc, changed = enrich_document(doc)
        enriched_docs.append(updated_doc)
        if changed:
            enriched_ids.append(updated_doc.doc_id)

    save_corpus(corpus_path, enriched_docs)
    if sync_fixture and fixture_path != corpus_path:
        save_corpus(fixture_path, enriched_docs)
    if readme_path and readme_path.exists():
        sync_readme_corpus_section(readme_path, enriched_docs)

    artifacts = run_build(corpus_path, output_dir)
    return {
        "documents": enriched_docs,
        "enriched_ids": enriched_ids,
        "artifacts": artifacts,
    }


def resolve_database_targets(
    args: argparse.Namespace,
    default_to_sister_db: bool = False,
) -> tuple[Path, Path, Path, Path, bool]:
    """Resolve `(corpus_path, output_dir, readme_path, fixture_path, sync_fixture)` from CLI switches.

    Priority:
    1. `--db` / `--db-dir` / `-d` switch (or `READING_DB_DIR` environment variable)
    2. Explicit `--corpus` / `--output-dir` switches
    3. `DEFAULT_SISTER_DB` (`../reading-db`) when `default_to_sister_db=True` and `--local` is not set
    4. Local workspace `input/corpus.json` and `output/`
    """
    db_dir: Path | None = getattr(args, "db_dir", None)
    local_flag: bool = getattr(args, "local", False)
    explicit_corpus: Path | None = getattr(args, "corpus", None)
    explicit_output: Path | None = getattr(args, "output_dir", None)
    explicit_fixture: Path = getattr(args, "fixture", None) or DEFAULT_FIXTURE
    explicit_readme: Path = getattr(args, "readme", None) or DEFAULT_README
    no_sync_fixture: bool = getattr(args, "no_sync_fixture", False)

    if local_flag:
        corpus_path = explicit_corpus or DEFAULT_CORPUS
        output_dir = explicit_output or DEFAULT_OUTPUT
        readme_path = explicit_readme
        sync_fixture = not no_sync_fixture and (corpus_path == DEFAULT_CORPUS)
        return corpus_path, output_dir, readme_path, explicit_fixture, sync_fixture

    if db_dir is None and os.environ.get("READING_DB_DIR") and explicit_corpus is None:
        db_dir = Path(os.environ["READING_DB_DIR"])

    if db_dir is not None:
        if db_dir.suffix.lower() == ".json":
            corpus_path = db_dir
            base_dir = db_dir.parent
        else:
            base_dir = db_dir
            corpus_path = base_dir / "corpus.json"
        output_dir = explicit_output or base_dir
        readme_path = base_dir / "README.md"
        return corpus_path, output_dir, readme_path, explicit_fixture, False

    if explicit_corpus is not None:
        corpus_path = explicit_corpus
        output_dir = explicit_output or (
            corpus_path.parent if corpus_path != DEFAULT_CORPUS else DEFAULT_OUTPUT
        )
        readme_path = explicit_readme
        sync_fixture = not no_sync_fixture and (
            corpus_path == DEFAULT_CORPUS or explicit_fixture != DEFAULT_FIXTURE
        )
        return corpus_path, output_dir, readme_path, explicit_fixture, sync_fixture

    if default_to_sister_db:
        base_dir = DEFAULT_SISTER_DB
        return (
            base_dir / "corpus.json",
            explicit_output or base_dir,
            base_dir / "README.md",
            explicit_fixture,
            False,
        )

    corpus_path = DEFAULT_CORPUS
    output_dir = explicit_output or DEFAULT_OUTPUT
    sync_fixture = not no_sync_fixture
    return corpus_path, output_dir, explicit_readme, explicit_fixture, sync_fixture


def _print_classification_card(result: dict[str, Any], doc_id: str | None = None) -> None:
    header = f"Classification Summary ({doc_id})" if doc_id else "Classification Summary"
    print(f"=== {header} ===")
    if result.get("title"):
        print(f"Title:            {result['title']}")
    print(f"Word Count:       {result['word_count']}")
    techs = ", ".join(result["technology_areas"]) or "Unclassified"
    print(f"Technology Areas: {techs}")
    print("Taxonomy Hierarchy:")
    if result["taxonomy_paths"]:
        for path in result["taxonomy_paths"]:
            print(f"  - {path}")
    else:
        print("  - (none matched)")
    concepts = [f"{c['concept_id']} ({c['label']})" for c in result["matched_concepts"]]
    print(f"Matched Concepts: {', '.join(concepts) if concepts else '(none)'}")
    cands = ", ".join(result["candidate_terms"][:10]) or "(none)"
    print(f"Candidate Terms:  {cands}")
    top_kw = ", ".join(f"{t['term']} ({t['count']})" for t in result["top_terms"][:8])
    print(f"Top Keywords:     {top_kw}")


def _extract_subcommands_and_positinals(
    primary_command: str,
    raw_positionals: list[str],
) -> tuple[list[str], list[str]]:
    """Separate trailing/chained subcommand tokens from positional query/target arguments."""
    subcommands: list[str] = []
    remaining: list[str] = []
    for token in raw_positionals:
        lower_tok = token.lower().strip()
        if lower_tok in CHAINABLE_SUBCOMMANDS and lower_tok != primary_command:
            subcommands.append(lower_tok)
        elif lower_tok == primary_command and lower_tok in CHAINABLE_SUBCOMMANDS:
            subcommands.append(lower_tok)
        else:
            remaining.append(token)
    return subcommands, remaining


def execute_research_and_update(
    args: argparse.Namespace,
    topic: str,
    subcommands: list[str],
) -> int:
    """Discover papers on `topic`, synthesize a research note, classify, and update the target database."""
    corpus_path, output_dir, readme_path, fixture_path, sync_fixture = (
        resolve_database_targets(args, default_to_sister_db=True)
    )
    ensure_corpus_file(corpus_path, fixture_path)
    existing_docs = (
        load_corpus(corpus_path)
        if corpus_path.exists()
        else load_corpus(fixture_path)
    )

    bundle = research_topic(
        topic=topic,
        existing_docs=existing_docs,
        max_results=args.max_results,
    )

    print(f"=== Research Report: {topic!r} ===")
    print(
        f"Discovered {len(bundle['discovered_documents'])} primary papers + 1 synthesis note:"
    )
    for doc in bundle["all_documents"]:
        cls_info = bundle["classifications"][doc.doc_id]
        _print_classification_card(cls_info, doc_id=doc.doc_id)

    if args.dry_run:
        print("[dry-run] No files modified.")
        return 0

    new_by_id = {d.doc_id: d for d in bundle["all_documents"]}
    merged_docs: list[Document] = []
    seen: set[str] = set()
    for doc in existing_docs:
        if doc.doc_id in new_by_id:
            merged_docs.append(new_by_id[doc.doc_id])
            seen.add(doc.doc_id)
        else:
            merged_docs.append(doc)
    for doc in bundle["all_documents"]:
        if doc.doc_id not in seen:
            merged_docs.append(doc)
            seen.add(doc.doc_id)

    save_corpus(corpus_path, merged_docs)
    if sync_fixture and fixture_path != corpus_path:
        save_corpus(fixture_path, merged_docs)
    if readme_path.exists():
        sync_readme_corpus_section(readme_path, merged_docs)

    artifacts = run_build(corpus_path, output_dir)
    print(f"[populated] {corpus_path} (total documents: {len(merged_docs)})")
    for name, path in artifacts.items():
        print(f"  [ok] {name}: {path}")

    if "push" in subcommands or getattr(args, "push", False):
        _git_commit_and_push_db(output_dir, f"feat(corpus): research and add {topic!r}")

    return 0


def execute_add_and_update(
    args: argparse.Namespace,
    positionals: list[str],
    subcommands: list[str],
) -> int:
    """Add a single document (or run research if `--topic` / `research` subcommand is given) and update the target DB."""
    topic = getattr(args, "topic", "") or ""
    if "research" in subcommands or (topic and not getattr(args, "title", "")):
        effective_topic = topic or " ".join(positionals).strip() or getattr(args, "title", "")
        if not effective_topic:
            print("error: provide --topic or a positional topic to research and add.")
            return 2
        return execute_research_and_update(args, effective_topic, subcommands)

    corpus_path, output_dir, readme_path, fixture_path, sync_fixture = (
        resolve_database_targets(args, default_to_sister_db=False)
    )
    ensure_corpus_file(corpus_path, fixture_path)
    docs = load_corpus(corpus_path)

    url = args.url
    title = args.title
    for pos in positionals:
        if (pos.startswith("http://") or pos.startswith("https://") or extract_arxiv_id(pos)) and not url:
            url = pos
        elif not title:
            title = pos

    content = args.file.read_text(encoding="utf-8") if args.file else args.text
    arxiv_id = extract_arxiv_id(url) or extract_arxiv_id(title or "")
    if arxiv_id and not url:
        url = f"https://arxiv.org/abs/{arxiv_id}"

    if not title and arxiv_id:
        meta = fetch_arxiv_metadata(arxiv_id)
        if meta and meta.get("title"):
            title = meta["title"]
            if not content and meta.get("summary"):
                content = structure_abstract_into_sections(meta["summary"])
        else:
            title = f"arXiv:{arxiv_id}"

    if not title:
        print("error: provide --title (or a positional title / arXiv URL) for 'add'.")
        return 2

    if not content:
        content = title

    doc_id = args.doc_id or (f"arxiv-{arxiv_id}" if arxiv_id else _slugify(title))
    relations: list[DocumentRelation] = []
    if args.reports_on:
        relations.append(DocumentRelation("REPORTS_ON", args.reports_on.strip()))
    if args.cites:
        for target in [c.strip() for c in args.cites.split(",") if c.strip()]:
            relations.append(DocumentRelation("CITES", target))

    identifiers: dict[str, str] = {}
    if arxiv_id:
        identifiers["arxiv"] = arxiv_id
        identifiers["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"

    new_doc = Document(
        doc_id=doc_id,
        title=title,
        doc_type=args.doc_type,
        url=url,
        published_date=args.published,
        authors=[a.strip() for a in args.authors.split(",") if a.strip()],
        institutions=[i.strip() for i in args.institutions.split(",") if i.strip()],
        identifiers=identifiers,
        relations=relations,
        content=content,
        reading_status=args.status,
        priority=args.priority,
        tags=[t.strip() for t in args.tags.split(",") if t.strip()],
        notes=args.notes,
    )
    new_doc, _ = enrich_document(new_doc)

    cls_result = classify_content(new_doc.content, title=new_doc.title)
    _print_classification_card(cls_result, doc_id=doc_id)

    if args.dry_run:
        print("[dry-run] No files modified.")
        return 0

    updated_docs = [d for d in docs if d.doc_id != doc_id] + [new_doc]
    save_corpus(corpus_path, updated_docs)
    if sync_fixture and fixture_path != corpus_path:
        save_corpus(fixture_path, updated_docs)
    if readme_path.exists():
        sync_readme_corpus_section(readme_path, updated_docs)

    artifacts = run_build(corpus_path, output_dir)
    print(f"[saved] {corpus_path} (total documents: {len(updated_docs)})")
    if sync_fixture and fixture_path != corpus_path:
        print(f"[synced] {fixture_path} & {readme_path}")
    for name, path in artifacts.items():
        print(f"  [ok] {name}: {path}")

    if "push" in subcommands or getattr(args, "push", False):
        _git_commit_and_push_db(output_dir, f"feat(corpus): add {doc_id}")

    return 0


def _git_commit_and_push_db(db_dir: Path, message: str) -> None:
    """Optionally stage, commit, and push the target database directory if it is a git repository."""
    if not (db_dir / ".git").exists():
        return
    subprocess.run(["git", "-C", str(db_dir), "add", "."], check=False)
    subprocess.run(["git", "-C", str(db_dir), "commit", "-m", message], check=False)
    subprocess.run(["git", "-C", str(db_dir), "push", "origin", "main"], check=False)


def _add_shared_db_switches(p: argparse.ArgumentParser, default_db: Path | None = None) -> None:
    """Register unified database/corpus targeting flags on any command parser."""
    p.add_argument(
        "-d",
        "--db",
        "--db-dir",
        dest="db_dir",
        type=Path,
        default=default_db,
        help="Target reading list database directory (e.g. ../reading-db) or corpus JSON file to update and rebuild.",
    )
    p.add_argument(
        "--corpus",
        type=Path,
        default=None,
        help="Explicit corpus JSON path (default: <db-dir>/corpus.json or input/corpus.json).",
    )
    p.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="Tracked seed fixture to keep in sync when updating local corpus.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for generated artifacts (default: <db-dir> or output/).",
    )
    p.add_argument(
        "--readme",
        type=Path,
        default=DEFAULT_README,
        help="README.md path to sync.",
    )
    p.add_argument(
        "--local",
        action="store_true",
        help="Operate on local input/corpus.json and output/ instead of ../reading-db.",
    )
    p.add_argument(
        "--no-sync-fixture",
        action="store_true",
        help="Do not automatically sync changes to tests/fixtures/seed_corpus.json.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview classifications and changes without writing files.",
    )
    p.add_argument(
        "--push",
        action="store_true",
        help="Commit and push the updated reading database repository after building.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reading_list.cli",
        usage="python3 -m reading_list.cli <command> [switches] [subcommand(s)]",
        description=(
            "Unified CLI for researching topics, adding papers/articles, classifying content, "
            "and updating any specified reading list database (e.g., -d ../reading-db)."
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. research <switches> [subcommands / topic]
    res_p = sub.add_parser(
        "research",
        usage="python3 -m reading_list.cli research [switches] [subcommand(s)]",
        help="Research a topic, synthesize academic/technical papers, classify them, and update the specified reading database.",
    )
    res_p.add_argument(
        "-t",
        "--topic",
        default="",
        help="Research topic query (can also be passed positionally).",
    )
    res_p.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=4,
        help="Maximum number of primary papers to add alongside the synthesis note (default: 4).",
    )
    _add_shared_db_switches(res_p, default_db=None)
    res_p.add_argument(
        "extra",
        nargs="*",
        help="Optional subcommand(s) (e.g., 'add', 'publish', 'push') and/or positional topic string.",
    )

    # 2. add <switches> [subcommands / title_or_url]
    add_p = sub.add_parser(
        "add",
        usage="python3 -m reading_list.cli add [switches] [subcommand(s)]",
        help="Add, enrich, and classify a paper/article/note (or research a topic) into the specified reading database.",
    )
    add_p.add_argument("--id", dest="doc_id", default="", help="Explicit document ID (auto-generated if omitted).")
    add_p.add_argument("--title", default="", help="Title of the article, paper, or note.")
    add_p.add_argument(
        "-t",
        "--topic",
        default="",
        help="Optional research topic (when chaining 'add --topic ... research').",
    )
    add_p.add_argument(
        "-n",
        "--max-results",
        type=int,
        default=4,
        help="Max papers if running topic research.",
    )
    add_p.add_argument(
        "--type",
        dest="doc_type",
        default="technical_article",
        choices=["technical_article", "academic_paper", "technical_paper", "note"],
        help="Document category.",
    )
    add_p.add_argument("--url", default="", help="Source URL (e.g., https://arxiv.org/abs/...).")
    add_p.add_argument("--published", default="", help="Published date (YYYY-MM-DD or YYYY-MM).")
    add_p.add_argument("--authors", default="", help="Comma-separated author names.")
    add_p.add_argument("--institutions", default="", help="Comma-separated institutions.")
    add_p.add_argument("--text", default="", help="Inline abstract, excerpt, or markdown content.")
    add_p.add_argument("--file", type=Path, help="Read document content from a file.")
    add_p.add_argument("--reports-on", default="", help="Target doc_id this article reports on.")
    add_p.add_argument("--cites", default="", help="Comma-separated doc_ids cited by this document.")
    add_p.add_argument(
        "--status",
        default="to-read",
        choices=["to-read", "reading", "read", "archived"],
        help="Reading status.",
    )
    add_p.add_argument(
        "--priority",
        default="medium",
        choices=["high", "medium", "low"],
        help="Reading priority.",
    )
    add_p.add_argument("--tags", default="", help="Comma-separated custom tags.")
    add_p.add_argument("--notes", default="", help="Personal tracking notes.")
    _add_shared_db_switches(add_p, default_db=None)
    add_p.add_argument(
        "extra",
        nargs="*",
        help="Optional subcommand(s) (e.g., 'research', 'publish', 'push') or positional title/URL.",
    )

    # 3. update / sync
    for cmd_name in ("update", "sync"):
        upd_p = sub.add_parser(
            cmd_name,
            usage=f"python3 -m reading_list.cli {cmd_name} [switches] [subcommand(s)]",
            help="Enrich & classify corpus entries, sync README/fixtures, and rebuild all knowledge-graph and GitHub Pages artifacts.",
        )
        _add_shared_db_switches(upd_p, default_db=None)
        upd_p.add_argument("extra", nargs="*", help="Optional chained subcommand(s).")

    # 4. publish-db / publish
    for cmd_name in ("publish-db", "publish"):
        pub_p = sub.add_parser(
            cmd_name,
            usage=f"python3 -m reading_list.cli {cmd_name} [switches] [subcommand(s)]",
            help="Enrich and publish all knowledge-graph JSONs, Markdown reports, and GitHub Pages site to the specified reading-db directory.",
        )
        _add_shared_db_switches(pub_p, default_db=DEFAULT_SISTER_DB)
        pub_p.add_argument("extra", nargs="*", help="Optional chained subcommand(s) (e.g., 'push').")

    # 5. seed-input
    seed_p = sub.add_parser(
        "seed-input",
        help="Copy the tracked seed fixture corpus into input/corpus.json.",
    )
    seed_p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    seed_p.add_argument("--output", type=Path, default=DEFAULT_CORPUS)

    # 6. build
    build_p = sub.add_parser(
        "build",
        help="Generate semantic chunks, word cloud, taxonomy tree, knowledge graph, and GitHub Pages index.html.",
    )
    build_p.add_argument("--input", type=Path, default=DEFAULT_FIXTURE)
    _add_shared_db_switches(build_p, default_db=None)

    # 7. classify
    cls_p = sub.add_parser(
        "classify",
        help="Quickly classify a text snippet, abstract, or file without modifying the corpus.",
    )
    cls_p.add_argument("--title", default="", help="Optional title for context.")
    cls_p.add_argument("--text", default="", help="Inline text or abstract to classify.")
    cls_p.add_argument("--file", type=Path, help="Path to a text/markdown file to classify.")
    cls_p.add_argument("--json", action="store_true", help="Output raw JSON classification.")
    cls_p.add_argument("extra", nargs="*", help="Optional positional text to classify.")

    # 8. list
    list_p = sub.add_parser(
        "list",
        help="List and filter tracked documents in the specified database by status, priority, taxonomy category, concept, or keyword.",
    )
    _add_shared_db_switches(list_p, default_db=None)
    list_p.add_argument("--status", default="", help="Filter by reading_status (to-read, reading, read, archived).")
    list_p.add_argument("--priority", default="", help="Filter by priority (high, medium, low).")
    list_p.add_argument("--type", dest="doc_type", default="", help="Filter by doc_type.")
    list_p.add_argument("--tech-area", default="", help="Substring filter on technology area.")
    list_p.add_argument("--category", default="", help="Substring filter on taxonomy category path.")
    list_p.add_argument("--concept", default="", help="Substring filter on concept ID or label.")
    list_p.add_argument("--query", default="", help="Full-text keyword filter across title, content, and notes.")
    list_p.add_argument("extra", nargs="*", help="Optional positional search query.")

    # 9. status
    stat_p = sub.add_parser(
        "status",
        help="Update reading status, priority, tags, or notes for a tracked document in the specified database.",
    )
    stat_p.add_argument("doc_id", help="Document ID to update.")
    stat_p.add_argument(
        "--set",
        dest="reading_status",
        choices=["to-read", "reading", "read", "archived"],
        help="New reading status.",
    )
    stat_p.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        help="New priority.",
    )
    stat_p.add_argument("--tags", help="Comma-separated tags (replaces existing tags if provided).")
    stat_p.add_argument("--notes", help="Updated personal notes.")
    _add_shared_db_switches(stat_p, default_db=None)
    stat_p.add_argument("extra", nargs="*", help="Optional chained subcommand(s).")

    # 10. import-curriculum
    imp_p = sub.add_parser(
        "import-curriculum",
        help="Import a kitsumiko/papers checkout into a sibling reading database (default: ../ai-curriculum-db).",
    )
    imp_p.add_argument(
        "-s",
        "--source",
        type=Path,
        required=True,
        help="Path to local clone of kitsumiko/papers.",
    )
    _add_shared_db_switches(imp_p, default_db=Path("../ai-curriculum-db"))
    imp_p.add_argument("extra", nargs="*", help="Optional chained subcommand(s) (e.g., 'push').")

    return parser


def _normalize_argv(argv: Sequence[str]) -> list[str]:
    """Allow global switches before `<command>` as well as `<command> [switches] [subcommand(s)]`."""
    tokens = list(argv)
    if not tokens:
        return tokens
    if tokens[0] in PRIMARY_COMMANDS or tokens[0] in {"-h", "--help"}:
        return tokens
    for idx, tok in enumerate(tokens):
        if tok in PRIMARY_COMMANDS:
            # Move the primary command to the front so argparse subparsers dispatch cleanly
            return [tok, *tokens[:idx], *tokens[idx + 1 :]]
    return tokens


def main(argv: Sequence[str] | None = None) -> int:
    import sys

    raw_argv = list(sys.argv[1:] if argv is None else argv)
    normalized_argv = _normalize_argv(raw_argv)

    parser = build_parser()
    args = parser.parse_args(normalized_argv)

    extra_tokens: list[str] = getattr(args, "extra", []) or []
    subcommands, positionals = _extract_subcommands_and_positinals(
        args.command, extra_tokens
    )

    if args.command == "research":
        topic = (args.topic or " ".join(positionals)).strip()
        if not topic:
            parser.error("Provide --topic / -t '<topic>' or pass the topic positionally.")
        return execute_research_and_update(args, topic, subcommands)

    if args.command == "add":
        return execute_add_and_update(args, positionals, subcommands)

    if args.command == "seed-input":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.fixture, args.output)
        print(f"Seeded input corpus at {args.output}")
        return 0

    if args.command == "import-curriculum":
        corpus_path, output_dir, _, _, _ = resolve_database_targets(
            args, default_to_sister_db=False
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        docs = build_kitsumiko_corpus(args.source)
        if args.dry_run:
            print(f"[dry-run] Parsed {len(docs)} documents from {args.source}")
            return 0
        copy_upstream_reference_files(args.source, output_dir)
        save_corpus(corpus_path, docs)
        write_curriculum_db_readme(output_dir, docs)
        artifacts = run_build(corpus_path, output_dir)
        print(f"[imported] {len(docs)} documents into {output_dir} from {args.source}")
        for name, path in artifacts.items():
            print(f"  [ok] {name}: {path}")
        if "push" in subcommands or getattr(args, "push", False):
            _git_commit_and_push_db(output_dir, "feat(curriculum): sync kitsumiko/papers knowledge graph")
        return 0

    if args.command in {"publish-db", "publish"}:
        corpus_path, output_dir, readme_path, _, _ = resolve_database_targets(
            args, default_to_sister_db=True
        )
        res = run_update_pipeline(
            corpus_path=corpus_path,
            fixture_path=corpus_path,
            output_dir=output_dir,
            readme_path=readme_path,
            sync_fixture=False,
        )
        print(f"[published] {len(res['documents'])} documents to {output_dir}")
        for name, path in res["artifacts"].items():
            print(f"  [ok] {name}: {path}")
        if "push" in subcommands or getattr(args, "push", False):
            _git_commit_and_push_db(output_dir, "feat(pages): publish updated knowledge graph and site")
        return 0

    if args.command in {"update", "sync"}:
        corpus_path, output_dir, readme_path, fixture_path, sync_fixture = (
            resolve_database_targets(args, default_to_sister_db=False)
        )
        res = run_update_pipeline(
            corpus_path=corpus_path,
            fixture_path=fixture_path,
            output_dir=output_dir,
            readme_path=readme_path,
            sync_fixture=sync_fixture,
        )
        docs = res["documents"]
        if res["enriched_ids"]:
            print(
                f"[step 1/3] Enriched metadata/sections for: {', '.join(res['enriched_ids'])}"
            )
        else:
            print(
                f"[step 1/3] Verified metadata & semantic sections for {len(docs)} documents"
            )
        if sync_fixture and fixture_path != corpus_path:
            print(f"[step 2/3] Synced {corpus_path} -> {fixture_path} and {readme_path}")
        else:
            print(f"[step 2/3] Updated {corpus_path} and {readme_path}")
        print(
            "[step 3/3] Rebuilt knowledge graph, taxonomy tree, word cloud, and GitHub Pages site:"
        )
        for name, path in res["artifacts"].items():
            print(f"  [ok] {name}: {path}")
        if "push" in subcommands or getattr(args, "push", False):
            _git_commit_and_push_db(output_dir, "feat(corpus): update reading list database")
        return 0

    if args.command == "build":
        if args.db_dir is not None or args.corpus is not None:
            corpus_path, output_dir, _, _, _ = resolve_database_targets(
                args, default_to_sister_db=False
            )
            source = corpus_path if corpus_path.exists() else DEFAULT_FIXTURE
        else:
            source = args.input if args.input.exists() else DEFAULT_FIXTURE
            output_dir = args.output_dir or DEFAULT_OUTPUT
        outputs = run_build(source, output_dir)
        for name, path in outputs.items():
            print(f"[ok] {name}: {path}")
        return 0

    if args.command == "classify":
        text = (
            args.file.read_text(encoding="utf-8")
            if args.file
            else (args.text or " ".join(positionals))
        )
        if not text and not args.title:
            parser.error("Provide --text, --file, --title, or positional text to classify.")
        result = classify_content(text, title=args.title)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            _print_classification_card(result)
        return 0

    if args.command == "list":
        corpus_path, _, _, fixture_path, _ = resolve_database_targets(
            args, default_to_sister_db=False
        )
        active_corpus = corpus_path if corpus_path.exists() else fixture_path
        docs = load_corpus(active_corpus)
        matched_rows: list[tuple[Document, dict[str, Any]]] = []
        query_filter = args.query or " ".join(positionals).strip()

        for doc in docs:
            cls_info = classify_content(doc.content, title=doc.title)
            if args.status and doc.reading_status != args.status:
                continue
            if args.priority and doc.priority != args.priority:
                continue
            if args.doc_type and doc.doc_type != args.doc_type:
                continue
            if args.tech_area and not any(
                args.tech_area.lower() in ta.lower()
                for ta in cls_info["technology_areas"]
            ):
                continue
            if args.category and not any(
                args.category.lower() in p.lower()
                for p in cls_info["taxonomy_paths"]
            ):
                continue
            if args.concept and not any(
                args.concept.lower() in c["concept_id"].lower()
                or args.concept.lower() in c["label"].lower()
                for c in cls_info["matched_concepts"]
            ):
                continue
            if query_filter:
                haystack = (
                    f"{doc.title} {doc.content} {doc.notes} {' '.join(doc.tags)}".lower()
                )
                if query_filter.lower() not in haystack:
                    continue
            matched_rows.append((doc, cls_info))

        print(f"Tracked Documents in {active_corpus} ({len(matched_rows)}/{len(docs)}):")
        for doc, info in matched_rows:
            techs = ", ".join(info["technology_areas"]) or "Unclassified"
            concept_count = len(info["matched_concepts"])
            print(
                f"  - [{doc.reading_status.upper():8s} | {doc.priority:6s}] {doc.doc_id} ({doc.doc_type})"
            )
            print(f"    Title:      {doc.title}")
            print(f"    Tech Areas: {techs} | Concepts: {concept_count}")
            if doc.tags or doc.notes:
                print(f"    Tags/Notes: tags={doc.tags} notes={doc.notes!r}")
        return 0

    if args.command == "status":
        corpus_path, output_dir, readme_path, fixture_path, sync_fixture = (
            resolve_database_targets(args, default_to_sister_db=False)
        )
        ensure_corpus_file(corpus_path, fixture_path)
        docs = load_corpus(corpus_path)
        updated: list[Document] = []
        target_found = False

        for doc in docs:
            if doc.doc_id == args.doc_id:
                target_found = True
                raw = doc.to_dict()
                if args.reading_status:
                    raw["reading_status"] = args.reading_status
                if args.priority:
                    raw["priority"] = args.priority
                if args.tags is not None:
                    raw["tags"] = [
                        t.strip() for t in args.tags.split(",") if t.strip()
                    ]
                if args.notes is not None:
                    raw["notes"] = args.notes
                updated.append(Document.from_dict(raw))
            else:
                updated.append(doc)

        if not target_found:
            parser.error(f"Document ID '{args.doc_id}' not found in {corpus_path}")

        save_corpus(corpus_path, updated)
        if sync_fixture and fixture_path != corpus_path:
            save_corpus(fixture_path, updated)
        if readme_path.exists():
            sync_readme_corpus_section(readme_path, updated)
        run_build(corpus_path, output_dir)
        print(f"[updated] {args.doc_id} in {corpus_path}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
