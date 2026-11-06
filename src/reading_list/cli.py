"""Command-line entry point for quick document tracking, content classification, research, and knowledge-graph builds."""

from __future__ import annotations

import argparse
import json
import re
import shutil
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
    sync_readme_corpus_section,
)
from reading_list.graph import (
    build_knowledge_graph,
    build_taxonomy_index,
    render_summary_markdown,
)
from reading_list.models import Document, DocumentRelation, SemanticChunk
from reading_list.research import research_topic
from reading_list.site import render_github_pages_html

DEFAULT_FIXTURE = Path("tests/fixtures/seed_corpus.json")
DEFAULT_CORPUS = Path("input/corpus.json")
DEFAULT_OUTPUT = Path("output")
DEFAULT_README = Path("README.md")
DEFAULT_SISTER_DB = Path("../reading-db")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48].strip("-") or "doc-entry"


def ensure_corpus_file(corpus_path: Path, fixture_path: Path = DEFAULT_FIXTURE) -> Path:
    """Ensure the mutable corpus JSON exists, seeding from the fixture if needed."""
    if not corpus_path.exists() and fixture_path.exists():
        corpus_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fixture_path, corpus_path)
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
    if sync_fixture:
        save_corpus(fixture_path, enriched_docs)
        sync_readme_corpus_section(readme_path, enriched_docs)

    artifacts = run_build(corpus_path, output_dir)
    return {
        "documents": enriched_docs,
        "enriched_ids": enriched_ids,
        "artifacts": artifacts,
    }


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


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="reading-list",
        description="Quick document tracker, research agent, semantic chunker, conceptual taxonomy classifier, and knowledge graph builder.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # 1. research (discover papers on a topic, generate synthesis note, classify, and populate reading-db or local corpus)
    res_p = sub.add_parser(
        "research",
        help="Research a technical topic, synthesize academic/technical papers, classify them into the taxonomy, and populate reading-db.",
    )
    res_p.add_argument(
        "--topic",
        required=True,
        help="Research topic query (e.g., 'Formal verification languages in chip and semiconductor design').",
    )
    res_p.add_argument(
        "--max-results",
        type=int,
        default=4,
        help="Maximum number of primary papers to add alongside the synthesis note.",
    )
    res_p.add_argument(
        "--db-dir",
        type=Path,
        default=DEFAULT_SISTER_DB,
        help="Target reading-db directory to populate and rebuild (default: ../reading-db).",
    )
    res_p.add_argument(
        "--local",
        action="store_true",
        help="Populate local input/corpus.json and output/ instead of ../reading-db.",
    )
    res_p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview discovered papers, synthesis note, and classifications without writing files.",
    )

    # 2. update (single command for steps 1, 2, 3: enrich, sync tracked corpus + README, rebuild all outputs)
    upd_p = sub.add_parser(
        "update",
        help="Single command to (1) enrich & classify corpus entries, (2) sync git-tracked seed_corpus.json & README.md, and (3) rebuild all output/ artifacts.",
    )
    upd_p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    upd_p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    upd_p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    upd_p.add_argument("--readme", type=Path, default=DEFAULT_README)

    # 3. publish-db (enrich & publish artifacts + GitHub Pages site to the sister reading-db repo)
    pub_p = sub.add_parser(
        "publish-db",
        help="Enrich and build all knowledge-graph JSONs, Markdown reports, and the interactive GitHub Pages site into the sister reading-db repository.",
    )
    pub_p.add_argument(
        "--db-dir",
        type=Path,
        default=DEFAULT_SISTER_DB,
        help="Path to the sister reading-db repository (default: ../reading-db).",
    )

    # 4. sync (alias for update)
    sync_p = sub.add_parser(
        "sync",
        help="Alias for 'update': enrich, sync input/corpus.json -> tests/fixtures/seed_corpus.json & README.md, and rebuild output/.",
    )
    sync_p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    sync_p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    sync_p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    sync_p.add_argument("--readme", type=Path, default=DEFAULT_README)

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
    build_p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)

    # 7. classify (ad-hoc content / snippet / file classification)
    cls_p = sub.add_parser(
        "classify",
        help="Quickly classify a text snippet, abstract, or file without modifying the corpus.",
    )
    cls_p.add_argument("--title", default="", help="Optional title for context.")
    cls_p.add_argument("--text", default="", help="Inline text or abstract to classify.")
    cls_p.add_argument("--file", type=Path, help="Path to a text/markdown file to classify.")
    cls_p.add_argument("--json", action="store_true", help="Output raw JSON classification.")

    # 8. add (track & classify a new document into corpus and run the full update pipeline)
    add_p = sub.add_parser(
        "add",
        help="Track, enrich, and classify a new article, paper, or note into the reading list and sync the repo.",
    )
    add_p.add_argument("--id", dest="doc_id", default="", help="Explicit document ID (auto-generated from title if omitted).")
    add_p.add_argument("--title", required=True, help="Title of the article, paper, or note.")
    add_p.add_argument(
        "--type",
        dest="doc_type",
        default="technical_article",
        choices=["technical_article", "academic_paper", "technical_paper", "note"],
        help="Document category.",
    )
    add_p.add_argument("--url", default="", help="Source URL.")
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
    add_p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS, help="Corpus file to update.")
    add_p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Tracked seed fixture to keep in sync.")
    add_p.add_argument(
        "--no-sync-fixture",
        action="store_true",
        help="Do not automatically sync changes to tests/fixtures/seed_corpus.json.",
    )
    add_p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Output directory to rebuild.")

    # 9. list (inspect & filter tracked reading list)
    list_p = sub.add_parser(
        "list",
        help="List and filter tracked documents by status, priority, taxonomy category, concept, or keyword.",
    )
    list_p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS, help="Corpus JSON to read.")
    list_p.add_argument("--status", default="", help="Filter by reading_status (to-read, reading, read, archived).")
    list_p.add_argument("--priority", default="", help="Filter by priority (high, medium, low).")
    list_p.add_argument("--type", dest="doc_type", default="", help="Filter by doc_type.")
    list_p.add_argument("--tech-area", default="", help="Substring filter on technology area.")
    list_p.add_argument("--category", default="", help="Substring filter on taxonomy category path.")
    list_p.add_argument("--concept", default="", help="Substring filter on concept ID or label.")
    list_p.add_argument("--query", default="", help="Full-text keyword filter across title, content, and notes.")

    # 10. status (update tracking status/priority/notes on an existing document)
    stat_p = sub.add_parser(
        "status",
        help="Update reading status, priority, tags, or notes for a tracked document.",
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
    stat_p.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS, help="Corpus JSON to update.")
    stat_p.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE, help="Tracked seed fixture to keep in sync.")
    stat_p.add_argument(
        "--no-sync-fixture",
        action="store_true",
        help="Do not automatically sync changes to tests/fixtures/seed_corpus.json.",
    )
    stat_p.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Output directory to rebuild.")

    args = parser.parse_args(argv)

    if args.command == "research":
        if args.local:
            target_corpus = ensure_corpus_file(DEFAULT_CORPUS, DEFAULT_FIXTURE)
            target_out = DEFAULT_OUTPUT
            target_readme = DEFAULT_README
        else:
            db_dir = args.db_dir
            target_corpus = db_dir / "corpus.json"
            target_out = db_dir
            target_readme = db_dir / "README.md"
            ensure_corpus_file(target_corpus, DEFAULT_FIXTURE)

        existing_docs = load_corpus(target_corpus) if target_corpus.exists() else load_corpus(DEFAULT_FIXTURE)
        bundle = research_topic(
            topic=args.topic,
            existing_docs=existing_docs,
            max_results=args.max_results,
        )

        print(f"=== Research Report: {args.topic!r} ===")
        print(f"Discovered {len(bundle['discovered_documents'])} primary papers + 1 synthesis note:")
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

        save_corpus(target_corpus, merged_docs)
        if target_readme.exists():
            sync_readme_corpus_section(target_readme, merged_docs)
        artifacts = run_build(target_corpus, target_out)
        print(f"[populated] {target_corpus} (total documents: {len(merged_docs)})")
        for name, path in artifacts.items():
            print(f"  [ok] {name}: {path}")
        return 0

    if args.command == "seed-input":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.fixture, args.output)
        print(f"Seeded input corpus at {args.output}")
        return 0

    if args.command == "publish-db":
        db_dir = args.db_dir
        corpus_path = db_dir / "corpus.json"
        readme_path = db_dir / "README.md"
        res = run_update_pipeline(
            corpus_path=corpus_path,
            fixture_path=corpus_path,
            output_dir=db_dir,
            readme_path=readme_path,
            sync_fixture=True,
        )
        print(f"[published] {len(res['documents'])} documents to {db_dir}")
        for name, path in res["artifacts"].items():
            print(f"  [ok] {name}: {path}")
        return 0

    if args.command in {"update", "sync"}:
        res = run_update_pipeline(
            corpus_path=args.corpus,
            fixture_path=args.fixture,
            output_dir=args.output_dir,
            readme_path=args.readme,
            sync_fixture=True,
        )
        docs = res["documents"]
        if res["enriched_ids"]:
            print(f"[step 1/3] Enriched metadata/sections for: {', '.join(res['enriched_ids'])}")
        else:
            print(f"[step 1/3] Verified metadata & semantic sections for {len(docs)} documents")
        print(f"[step 2/3] Synced {args.corpus} -> {args.fixture} and {args.readme}")
        print("[step 3/3] Rebuilt knowledge graph, taxonomy tree, word cloud, and GitHub Pages site:")
        for name, path in res["artifacts"].items():
            print(f"  [ok] {name}: {path}")
        return 0

    if args.command == "build":
        source = args.input if args.input.exists() else DEFAULT_FIXTURE
        outputs = run_build(source, args.output_dir)
        for name, path in outputs.items():
            print(f"[ok] {name}: {path}")
        return 0

    if args.command == "classify":
        text = args.file.read_text(encoding="utf-8") if args.file else args.text
        if not text and not args.title:
            parser.error("Provide --text, --file, or --title to classify.")
        result = classify_content(text, title=args.title)
        if args.json:
            print(json.dumps(result, indent=2, sort_keys=True))
        else:
            _print_classification_card(result)
        return 0

    if args.command == "add":
        corpus_path = ensure_corpus_file(args.corpus, args.fixture)
        docs = load_corpus(corpus_path)

        content = args.file.read_text(encoding="utf-8") if args.file else args.text
        if not content:
            content = args.title

        doc_id = args.doc_id or _slugify(args.title)
        relations: list[DocumentRelation] = []
        if args.reports_on:
            relations.append(DocumentRelation("REPORTS_ON", args.reports_on.strip()))
        if args.cites:
            for target in [c.strip() for c in args.cites.split(",") if c.strip()]:
                relations.append(DocumentRelation("CITES", target))

        identifiers: dict[str, str] = {}
        arxiv_id = extract_arxiv_id(args.url)
        if arxiv_id:
            identifiers["arxiv"] = arxiv_id
            identifiers["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"

        new_doc = Document(
            doc_id=doc_id,
            title=args.title,
            doc_type=args.doc_type,
            url=args.url,
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

        updated_docs = [d for d in docs if d.doc_id != doc_id] + [new_doc]
        save_corpus(corpus_path, updated_docs)
        should_sync = not args.no_sync_fixture and corpus_path == DEFAULT_CORPUS
        if should_sync:
            save_corpus(args.fixture, updated_docs)
            sync_readme_corpus_section(DEFAULT_README, updated_docs)
        run_build(corpus_path, args.output_dir)

        cls_result = classify_content(new_doc.content, title=new_doc.title)
        _print_classification_card(cls_result, doc_id=doc_id)
        print(f"[saved] {corpus_path} (total documents: {len(updated_docs)})")
        if should_sync:
            print(f"[synced] {args.fixture} & {DEFAULT_README}")
        return 0

    if args.command == "list":
        corpus_path = args.corpus if args.corpus.exists() else DEFAULT_FIXTURE
        docs = load_corpus(corpus_path)
        matched_rows: list[tuple[Document, dict[str, Any]]] = []

        for doc in docs:
            cls_info = classify_content(doc.content, title=doc.title)
            if args.status and doc.reading_status != args.status:
                continue
            if args.priority and doc.priority != args.priority:
                continue
            if args.doc_type and doc.doc_type != args.doc_type:
                continue
            if args.tech_area and not any(
                args.tech_area.lower() in ta.lower() for ta in cls_info["technology_areas"]
            ):
                continue
            if args.category and not any(
                args.category.lower() in p.lower() for p in cls_info["taxonomy_paths"]
            ):
                continue
            if args.concept and not any(
                args.concept.lower() in c["concept_id"].lower()
                or args.concept.lower() in c["label"].lower()
                for c in cls_info["matched_concepts"]
            ):
                continue
            if args.query:
                haystack = f"{doc.title} {doc.content} {doc.notes} {' '.join(doc.tags)}".lower()
                if args.query.lower() not in haystack:
                    continue
            matched_rows.append((doc, cls_info))

        print(f"Tracked Documents ({len(matched_rows)}/{len(docs)}):")
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
        corpus_path = ensure_corpus_file(args.corpus, args.fixture)
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
                    raw["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
                if args.notes is not None:
                    raw["notes"] = args.notes
                updated.append(Document.from_dict(raw))
            else:
                updated.append(doc)

        if not target_found:
            parser.error(f"Document ID '{args.doc_id}' not found in {corpus_path}")

        save_corpus(corpus_path, updated)
        if not args.no_sync_fixture and corpus_path == DEFAULT_CORPUS:
            save_corpus(args.fixture, updated)
            sync_readme_corpus_section(DEFAULT_README, updated)
        run_build(corpus_path, args.output_dir)
        print(f"[updated] {args.doc_id} in {corpus_path}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
