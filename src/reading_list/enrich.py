"""Automatic metadata/abstract enrichment and README synchronization for reading-list documents."""

from __future__ import annotations

import html
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from reading_list.models import Document

ARXIV_URL_RE = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)")
ARXIV_ID_RE = re.compile(r"^([0-9]{4}\.[0-9]{4,5}(?:v\d+)?)$")


def extract_arxiv_id(url_or_id: str) -> str | None:
    """Return the arXiv identifier from a URL or raw ID string if present."""
    raw = url_or_id.strip()
    m = ARXIV_URL_RE.search(raw)
    if m:
        return m.group(1)
    m2 = ARXIV_ID_RE.match(raw)
    if m2:
        return m2.group(1)
    return None


def structure_abstract_into_sections(abstract: str) -> str:
    """Split a single-block abstract into semantic Markdown sections if no headings exist."""
    cleaned = " ".join(abstract.strip().split())
    if not cleaned:
        return ""
    if "##" in abstract:
        return abstract.strip()

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    if len(sentences) <= 3:
        return f"## Overview & Core Contribution\n{cleaned}"

    third = max(1, len(sentences) // 3)
    part1 = " ".join(sentences[:third])
    part2 = " ".join(sentences[third : 2 * third])
    part3 = " ".join(sentences[2 * third :])

    sections = [f"## Problem Statement & Context\n{part1}"]
    if part2:
        sections.append(f"## Proposed Mechanism & Architecture\n{part2}")
    if part3:
        sections.append(f"## Evaluation & Key Findings\n{part3}")
    return "\n\n".join(sections)


def fetch_arxiv_metadata(arxiv_id: str, timeout: float = 8.0) -> dict[str, Any] | None:
    """Fetch title, authors, published date, and abstract from the arXiv Atom API."""
    base_id = re.sub(r"v\d+$", "", arxiv_id)
    api_url = f"https://export.arxiv.org/api/query?id_list={base_id}"
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "reading-list-indexer/0.1"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_bytes = resp.read()
    except Exception:
        return None

    try:
        root = ET.fromstring(xml_bytes)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        entry = root.find("atom:entry", ns)
        if entry is None:
            return None

        title_el = entry.find("atom:title", ns)
        summary_el = entry.find("atom:summary", ns)
        published_el = entry.find("atom:published", ns)
        cat_el = entry.find("arxiv:primary_category", ns)

        title = " ".join((title_el.text or "").split()) if title_el is not None else ""
        summary = " ".join((summary_el.text or "").split()) if summary_el is not None else ""
        published = (published_el.text or "")[:10] if published_el is not None else ""
        primary_cat = cat_el.attrib.get("term", "") if cat_el is not None else ""

        authors: list[str] = []
        for author_el in entry.findall("atom:author", ns):
            name_el = author_el.find("atom:name", ns)
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        if not title and not summary:
            return None

        return {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "published_date": published,
            "primary_category": primary_cat,
            "summary": summary,
            "url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
        }
    except Exception:
        return None


def fetch_web_article_metadata(url: str, timeout: float = 8.0) -> dict[str, Any] | None:
    """Fetch basic title and paragraph excerpt from an HTML article URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; reading-list/0.1)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw_html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    title_match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
    title = html.unescape(" ".join(title_match.group(1).split())) if title_match else ""

    paragraphs: list[str] = []
    for p_match in re.finditer(r"<p[^>]*>(.*?)</p>", raw_html, re.IGNORECASE | re.DOTALL):
        text = re.sub(r"<[^>]+>", "", p_match.group(1))
        text = html.unescape(" ".join(text.split()))
        if len(text.split()) >= 12:
            paragraphs.append(text)
        if len(paragraphs) >= 6:
            break

    if not title and not paragraphs:
        return None

    return {
        "title": title,
        "content": structure_abstract_into_sections(" ".join(paragraphs)),
    }


def enrich_document(doc: Document) -> tuple[Document, bool]:
    """Enrich a stub Document with metadata and structured sections if needed."""
    is_stub_content = (
        not doc.content.strip()
        or doc.content.strip() == doc.title.strip()
        or len(doc.content.split()) < 20
    )
    arxiv_id = doc.identifiers.get("arxiv") or extract_arxiv_id(doc.url)

    raw = doc.to_dict()
    changed = False

    if arxiv_id and "arxiv" not in raw["identifiers"]:
        raw["identifiers"]["arxiv"] = arxiv_id
        raw["identifiers"]["pdf_url"] = f"https://arxiv.org/pdf/{arxiv_id}"
        changed = True

    if arxiv_id and (is_stub_content or not doc.authors or not doc.published_date):
        meta = fetch_arxiv_metadata(arxiv_id)
        if meta:
            if (not doc.title or doc.title == arxiv_id) and meta["title"]:
                raw["title"] = meta["title"]
            if not doc.authors and meta["authors"]:
                raw["authors"] = meta["authors"]
            if not doc.published_date and meta["published_date"]:
                raw["published_date"] = meta["published_date"]
            if meta["primary_category"]:
                raw["identifiers"]["primary_category"] = meta["primary_category"]
            if raw["doc_type"] == "technical_article":
                raw["doc_type"] = "academic_paper"
            if is_stub_content and meta["summary"]:
                raw["content"] = structure_abstract_into_sections(meta["summary"])
            changed = True

    elif doc.url and is_stub_content:
        web_meta = fetch_web_article_metadata(doc.url)
        if web_meta:
            if not doc.title and web_meta["title"]:
                raw["title"] = web_meta["title"]
            if web_meta["content"]:
                raw["content"] = web_meta["content"]
                changed = True

    if "##" not in raw["content"] and len(raw["content"].split()) >= 35:
        raw["content"] = structure_abstract_into_sections(raw["content"])
        changed = True

    return Document.from_dict(raw), changed


def sync_readme_corpus_section(readme_path: Path, documents: list[Document]) -> bool:
    """Update the numbered Tracked Reading List Corpus section in README.md."""
    if not readme_path.exists():
        return False

    original = readme_path.read_text(encoding="utf-8")
    header = "## Tracked Reading List Corpus (`tests/fixtures/seed_corpus.json`)"
    if header not in original:
        return False

    type_labels = {
        "technical_article": "Technical Article",
        "academic_paper": "Academic Paper",
        "technical_paper": "Technical Paper",
        "note": "Research Note",
    }

    bullet_lines: list[str] = []
    for idx, doc in enumerate(documents, start=1):
        t_label = type_labels.get(doc.doc_type, doc.doc_type)
        title_link = f"[*{doc.title}*]({doc.url})" if doc.url else f"*{doc.title}*"
        meta_parts: list[str] = [f"`{doc.doc_id}`"]
        if doc.authors:
            meta_parts.append(", ".join(doc.authors))
        if doc.institutions:
            meta_parts.append("; ".join(doc.institutions))
        meta_str = " — ".join(meta_parts)
        bullet_lines.append(f"{idx}. **{t_label}:** {title_link} ({meta_str})")

    new_block = header + "\n\n" + "\n".join(bullet_lines) + "\n\n"
    pattern = re.compile(
        re.escape(header) + r"\n\n(?:[0-9]+\..*\n)+\n*",
        re.MULTILINE,
    )
    updated, count = pattern.subn(new_block, original, count=1)
    if count > 0 and updated != original:
        readme_path.write_text(updated, encoding="utf-8")
        return True
    return False
