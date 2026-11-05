"""Knowledge graph construction, taxonomy tree export, and Markdown/Mermaid rendering."""

from __future__ import annotations

from typing import Any

from reading_list.models import (
    Document,
    GraphEdge,
    GraphNode,
    KnowledgeGraph,
    SemanticChunk,
)
from reading_list.taxonomy import CONCEPT_CATALOG, TAXONOMY_NODES


def _slug(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace(">", "-")
        .replace(" ", "-")
        .replace("--", "-")
        .strip("-")
    )


def build_knowledge_graph(
    documents: list[Document],
    chunks_by_doc: dict[str, list[SemanticChunk]],
) -> KnowledgeGraph:
    """Link documents, semantic chunks, concepts, taxonomy hierarchy, and technology areas."""
    kg = KnowledgeGraph()

    # 1. Register Taxonomy Category Hierarchy & Technology Areas
    for tax_node in TAXONOMY_NODES:
        cat_id = f"taxonomy:{_slug(tax_node.path)}"
        tech_id = f"tech_area:{_slug(tax_node.technology_area)}"

        kg.add_node(
            GraphNode(
                node_id=cat_id,
                node_type="TaxonomyCategory",
                label=tax_node.label,
                properties={
                    "path": tax_node.path,
                    "description": tax_node.description,
                    "ontologic_class_uri": tax_node.ontologic_class_uri,
                },
            )
        )
        kg.add_node(
            GraphNode(
                node_id=tech_id,
                node_type="TechnologyArea",
                label=tax_node.technology_area,
                properties={},
            )
        )
        kg.add_edge(
            GraphEdge(
                source=cat_id,
                target=tech_id,
                predicate="IN_TECH_AREA",
            )
        )
        if tax_node.parent_path:
            parent_id = f"taxonomy:{_slug(tax_node.parent_path)}"
            kg.add_edge(
                GraphEdge(
                    source=cat_id,
                    target=parent_id,
                    predicate="SUBCATEGORY_OF",
                )
            )

    # 2. Register Canonical Concepts and their Taxonomy/Concept links
    concept_map = {c.concept_id: c for c in CONCEPT_CATALOG}
    for concept in CONCEPT_CATALOG:
        kg.add_node(
            GraphNode(
                node_id=concept.concept_id,
                node_type="Concept",
                label=concept.label,
                properties={
                    "description": concept.description,
                    "taxonomy_path": concept.taxonomy_path,
                    "technology_area": concept.technology_area,
                },
            )
        )
        cat_id = f"taxonomy:{_slug(concept.taxonomy_path)}"
        kg.add_edge(
            GraphEdge(
                source=concept.concept_id,
                target=cat_id,
                predicate="IN_CATEGORY",
            )
        )
        for related_id in concept.related_concepts:
            if related_id in concept_map:
                kg.add_edge(
                    GraphEdge(
                        source=concept.concept_id,
                        target=related_id,
                        predicate="RELATED_CONCEPT",
                    )
                )

    # 3. Register Documents, Authors, Institutions, Relations, and Chunks
    for doc in documents:
        doc_node_id = f"doc:{doc.doc_id}"
        kg.add_node(
            GraphNode(
                node_id=doc_node_id,
                node_type="Document",
                label=doc.title,
                properties={
                    "doc_id": doc.doc_id,
                    "doc_type": doc.doc_type,
                    "url": doc.url,
                    "published_date": doc.published_date,
                    "reading_status": doc.reading_status,
                    "priority": doc.priority,
                    "tags": doc.tags,
                    "notes": doc.notes,
                    "identifiers": doc.identifiers,
                },
            )
        )

        for author in doc.authors:
            author_id = f"author:{_slug(author)}"
            kg.add_node(
                GraphNode(
                    node_id=author_id,
                    node_type="Author",
                    label=author,
                )
            )
            kg.add_edge(
                GraphEdge(
                    source=doc_node_id,
                    target=author_id,
                    predicate="AUTHORED_BY",
                )
            )

        for inst in doc.institutions:
            inst_id = f"institution:{_slug(inst)}"
            kg.add_node(
                GraphNode(
                    node_id=inst_id,
                    node_type="Institution",
                    label=inst,
                )
            )
            kg.add_edge(
                GraphEdge(
                    source=doc_node_id,
                    target=inst_id,
                    predicate="AFFILIATED_WITH",
                )
            )

        for rel in doc.relations:
            kg.add_edge(
                GraphEdge(
                    source=doc_node_id,
                    target=f"doc:{rel.target_doc_id}",
                    predicate=rel.relation_type,
                )
            )

        for chunk in chunks_by_doc.get(doc.doc_id, []):
            chunk_node_id = f"chunk:{chunk.chunk_id}"
            kg.add_node(
                GraphNode(
                    node_id=chunk_node_id,
                    node_type="SemanticChunk",
                    label=f"{doc.doc_id}: {chunk.heading}",
                    properties={
                        "chunk_id": chunk.chunk_id,
                        "heading": chunk.heading,
                        "token_count": chunk.token_count,
                    },
                )
            )
            kg.add_edge(
                GraphEdge(
                    source=doc_node_id,
                    target=chunk_node_id,
                    predicate="HAS_CHUNK",
                )
            )
            for cid in chunk.concept_ids:
                kg.add_edge(
                    GraphEdge(
                        source=chunk_node_id,
                        target=cid,
                        predicate="MENTIONS_CONCEPT",
                    )
                )
                kg.add_edge(
                    GraphEdge(
                        source=doc_node_id,
                        target=cid,
                        predicate="MENTIONS_CONCEPT",
                    )
                )
            for path in chunk.taxonomy_paths:
                cat_id = f"taxonomy:{_slug(path)}"
                kg.add_edge(
                    GraphEdge(
                        source=chunk_node_id,
                        target=cat_id,
                        predicate="IN_CATEGORY",
                    )
                )
                kg.add_edge(
                    GraphEdge(
                        source=doc_node_id,
                        target=cat_id,
                        predicate="IN_CATEGORY",
                    )
                )
            for tech in chunk.technology_areas:
                tech_id = f"tech_area:{_slug(tech)}"
                kg.add_edge(
                    GraphEdge(
                        source=doc_node_id,
                        target=tech_id,
                        predicate="IN_TECH_AREA",
                    )
                )

    return kg


def build_taxonomy_index(
    documents: list[Document],
    chunks_by_doc: dict[str, list[SemanticChunk]],
) -> dict[str, Any]:
    """Build a structured taxonomy hierarchy indexing documents and semantic chunks."""
    categories: list[dict[str, Any]] = []
    for node in TAXONOMY_NODES:
        matching_docs = sorted(
            {
                doc.doc_id
                for doc in documents
                for chunk in chunks_by_doc.get(doc.doc_id, [])
                if node.path in chunk.taxonomy_paths
            }
        )
        matching_chunks = sorted(
            {
                chunk.chunk_id
                for doc in documents
                for chunk in chunks_by_doc.get(doc.doc_id, [])
                if node.path in chunk.taxonomy_paths
            }
        )
        categories.append(
            {
                "path": node.path,
                "label": node.label,
                "parent_path": node.parent_path,
                "technology_area": node.technology_area,
                "ontologic_class_uri": node.ontologic_class_uri,
                "description": node.description,
                "document_ids": matching_docs,
                "chunk_ids": matching_chunks,
            }
        )
    return {"taxonomy_categories": categories}


def render_summary_markdown(
    documents: list[Document],
    chunks_by_doc: dict[str, list[SemanticChunk]],
    word_cloud: dict[str, Any],
    kg: KnowledgeGraph,
) -> str:
    """Render a Markdown report with document index, word cloud, and dynamic Mermaid graph."""
    lines: list[str] = [
        "# Reading List Knowledge Graph & Taxonomy Index",
        "",
        f"- **Documents Indexed:** {len(documents)}",
        f"- **Semantic Chunks:** {sum(len(v) for v in chunks_by_doc.values())}",
        f"- **Knowledge Graph Nodes:** {len(kg.nodes)}",
        f"- **Knowledge Graph Edges:** {len(kg.edges)}",
        "",
        "## 1. Indexed Documents & Tracking Status",
        "",
        "| ID | Status | Priority | Type | Title | Published | Links |",
        "|---|---|---|---|---|---|---|",
    ]
    for doc in documents:
        rels = ", ".join(f"`{r.relation_type}` -> `{r.target_doc_id}`" for r in doc.relations) or "—"
        title_cell = f"[{doc.title}]({doc.url})" if doc.url else doc.title
        lines.append(
            f"| `{doc.doc_id}` | `{doc.reading_status}` | `{doc.priority}` | `{doc.doc_type}` | {title_cell} | {doc.published_date} | {rels} |"
        )

    mermaid_lines: list[str] = [
        "",
        "## 2. Conceptual Taxonomy & Document Graph",
        "",
        "```mermaid",
        "flowchart TD",
    ]
    tax_ids: dict[str, str] = {}
    for idx, node in enumerate(TAXONOMY_NODES):
        tid = f"TAX{idx}"
        tax_ids[node.path] = tid
        mermaid_lines.append(f'    {tid}["{node.label}"]')
    for node in TAXONOMY_NODES:
        if node.parent_path and node.parent_path in tax_ids:
            mermaid_lines.append(f"    {tax_ids[node.parent_path]} --> {tax_ids[node.path]}")

    doc_node_ids = {doc.doc_id: f"DOC{i}" for i, doc in enumerate(documents)}
    for doc in documents:
        d_var = doc_node_ids[doc.doc_id]
        mermaid_lines.append(f'    {d_var}["{doc.doc_id}"]')
        for rel in doc.relations:
            if rel.target_doc_id in doc_node_ids:
                mermaid_lines.append(
                    f"    {d_var} -->|{rel.relation_type}| {doc_node_ids[rel.target_doc_id]}"
                )
        # Connect document to its leaf taxonomy categories
        doc_paths = {
            path
            for chunk in chunks_by_doc.get(doc.doc_id, [])
            for path in chunk.taxonomy_paths
        }
        parent_paths = {
            n.parent_path for n in TAXONOMY_NODES if n.path in doc_paths and n.parent_path
        }
        leaf_paths = sorted(doc_paths - parent_paths)
        for lp in leaf_paths:
            if lp in tax_ids:
                mermaid_lines.append(f"    {d_var} -->|IN_CATEGORY| {tax_ids[lp]}")

    mermaid_lines.extend(
        [
            "```",
            "",
            "## 3. Global Word Cloud (Top 15 Terms)",
            "",
            "| Term | Frequency | Normalized Weight |",
            "|---|---|---|",
        ]
    )
    lines.extend(mermaid_lines)

    for item in word_cloud.get("global_word_cloud", [])[:15]:
        lines.append(f"| `{item['term']}` | {item['count']} | {item['weight']:.2f} |")

    lines.extend(["", "## 4. Semantic Chunks by Document", ""])
    for doc in documents:
        lines.append(f"### `{doc.doc_id}` — {doc.title}")
        lines.append("")
        for chunk in chunks_by_doc.get(doc.doc_id, []):
            concepts_str = ", ".join(f"`{c}`" for c in chunk.concept_ids) or "none"
            tax_str = "; ".join(f"`{p}`" for p in chunk.taxonomy_paths) or "none"
            lines.append(f"- **`{chunk.chunk_id}` ({chunk.heading})** [{chunk.token_count} words]")
            lines.append(f"  - **Concepts:** {concepts_str}")
            lines.append(f"  - **Taxonomy:** {tax_str}")
        lines.append("")

    return "\n".join(lines)
