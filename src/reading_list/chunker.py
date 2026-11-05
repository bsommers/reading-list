"""Semantic document chunking, fast content classification, and word-cloud term frequency extraction."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from reading_list.models import Document, SemanticChunk
from reading_list.taxonomy import (
    classify_taxonomy,
    extract_candidate_concepts,
    match_concepts,
)

STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "about",
        "across",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "few",
        "for",
        "from",
        "here",
        "in",
        "into",
        "is",
        "it",
        "its",
        "making",
        "many",
        "more",
        "near",
        "of",
        "on",
        "or",
        "our",
        "per",
        "such",
        "that",
        "the",
        "their",
        "these",
        "this",
        "through",
        "titled",
        "to",
        "toward",
        "under",
        "unlike",
        "up",
        "we",
        "where",
        "which",
        "whose",
        "with",
        "yet",
    }
)

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    """Tokenize text into normalized lowercase domain terms, preserving hyphenated words."""
    tokens: list[str] = []
    for match in TOKEN_PATTERN.finditer(text.lower()):
        tok = match.group(0)
        if len(tok) < 2 or tok in STOPWORDS or tok.isdigit():
            continue
        if tok in {"https", "http", "org", "abs", "pdf", "com"}:
            continue
        tokens.append(tok)
    return tokens


def split_sections(content: str, max_words_per_chunk: int = 120) -> list[tuple[str, str]]:
    """Split markdown content into (heading, body) semantic segments."""
    lines = content.strip().splitlines()
    sections: list[tuple[str, list[str]]] = []
    current_heading = "Overview"
    current_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_lines:
                sections.append((current_heading, current_lines))
                current_lines = []
            current_heading = stripped.lstrip("#").strip() or "Overview"
        elif stripped:
            current_lines.append(stripped)

    if current_lines:
        sections.append((current_heading, current_lines))

    results: list[tuple[str, str]] = []
    for heading, body_lines in sections:
        paragraph = " ".join(body_lines)
        words = paragraph.split()
        if len(words) <= max_words_per_chunk:
            results.append((heading, paragraph))
        else:
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
            buf: list[str] = []
            buf_words = 0
            part = 1
            for sent in sentences:
                sent_words = len(sent.split())
                if buf and buf_words + sent_words > max_words_per_chunk:
                    results.append((f"{heading} (Part {part})", " ".join(buf)))
                    part += 1
                    buf = [sent]
                    buf_words = sent_words
                else:
                    buf.append(sent)
                    buf_words += sent_words
            if buf:
                suffix = f" (Part {part})" if part > 1 else ""
                results.append((f"{heading}{suffix}", " ".join(buf)))

    return results


def chunk_document(doc: Document, max_words_per_chunk: int = 120) -> list[SemanticChunk]:
    """Semantically chunk a document and annotate each chunk with concepts and taxonomy paths."""
    raw_sections = split_sections(doc.content, max_words_per_chunk=max_words_per_chunk)
    chunks: list[SemanticChunk] = []

    for idx, (heading, body) in enumerate(raw_sections):
        combined_text = f"{doc.title}. {heading}. {body}" if idx == 0 else f"{heading}. {body}"
        tokens = tokenize(combined_text)
        term_counts = Counter(tokens).most_common(12)
        matched_concepts = match_concepts(combined_text)
        taxonomy_paths, tech_areas = classify_taxonomy(combined_text, matched_concepts)

        chunk = SemanticChunk(
            chunk_id=f"{doc.doc_id}#chunk-{idx + 1:02d}",
            doc_id=doc.doc_id,
            section_index=idx + 1,
            heading=heading,
            text=body,
            token_count=len(body.split()),
            key_terms=term_counts,
            concept_ids=sorted(c.concept_id for c in matched_concepts),
            taxonomy_paths=taxonomy_paths,
            technology_areas=tech_areas,
        )
        chunks.append(chunk)

    return chunks


def classify_content(text: str, title: str = "") -> dict[str, Any]:
    """Quickly classify raw text or an abstract into taxonomy categories, concepts, and key terms."""
    combined = f"{title}. {text}".strip() if title else text
    matched = match_concepts(combined)
    taxonomy_paths, tech_areas = classify_taxonomy(combined, matched)
    tokens = tokenize(combined)
    counts = Counter(tokens)
    max_freq = max(counts.values(), default=1)
    top_terms = [
        {"term": term, "count": count, "weight": round(count / max_freq, 4)}
        for term, count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))[:15]
    ]
    candidates = extract_candidate_concepts(combined)

    return {
        "title": title,
        "word_count": len(text.split()),
        "technology_areas": tech_areas,
        "taxonomy_paths": taxonomy_paths,
        "matched_concepts": [
            {
                "concept_id": c.concept_id,
                "label": c.label,
                "taxonomy_path": c.taxonomy_path,
            }
            for c in matched
        ],
        "candidate_terms": candidates,
        "top_terms": top_terms,
    }


def build_word_cloud(
    documents: list[Document],
    chunks_by_doc: dict[str, list[SemanticChunk]],
    top_k: int = 30,
) -> dict[str, Any]:
    """Compute global and per-document word cloud frequencies and normalized weights."""
    global_counter: Counter[str] = Counter()
    per_doc: dict[str, list[dict[str, Any]]] = {}

    for doc in documents:
        doc_counter: Counter[str] = Counter()
        for chunk in chunks_by_doc.get(doc.doc_id, []):
            doc_counter.update(tokenize(f"{chunk.heading} {chunk.text}"))
        global_counter.update(doc_counter)

        max_doc_freq = max(doc_counter.values(), default=1)
        per_doc[doc.doc_id] = [
            {
                "term": term,
                "count": count,
                "weight": round(count / max_doc_freq, 4),
            }
            for term, count in sorted(doc_counter.items(), key=lambda x: (-x[1], x[0]))[:top_k]
        ]

    max_global = max(global_counter.values(), default=1)
    global_terms = [
        {
            "term": term,
            "count": count,
            "weight": round(count / max_global, 4),
        }
        for term, count in sorted(global_counter.items(), key=lambda x: (-x[1], x[0]))[:top_k]
    ]

    return {
        "global_word_cloud": global_terms,
        "by_document": per_doc,
    }
