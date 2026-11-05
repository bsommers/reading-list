"""Core data models for documents, semantic chunks, taxonomy nodes, and the knowledge graph."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class DocumentRelation:
    """Directed relationship from one reading-list document to another."""

    relation_type: str
    target_doc_id: str


@dataclass(frozen=True)
class Document:
    """A technical article, academic paper, or technical report in the reading list."""

    doc_id: str
    title: str
    doc_type: str
    url: str
    published_date: str
    authors: list[str]
    institutions: list[str]
    identifiers: dict[str, str]
    relations: list[DocumentRelation]
    content: str
    reading_status: str = "to-read"
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    notes: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Document:
        relations = [
            DocumentRelation(
                relation_type=rel["relation_type"],
                target_doc_id=rel["target_doc_id"],
            )
            for rel in raw.get("relations", [])
        ]
        return cls(
            doc_id=raw["doc_id"],
            title=raw["title"],
            doc_type=raw.get("doc_type", "technical_article"),
            url=raw.get("url", ""),
            published_date=raw.get("published_date", ""),
            authors=list(raw.get("authors", [])),
            institutions=list(raw.get("institutions", [])),
            identifiers=dict(raw.get("identifiers", {})),
            relations=relations,
            content=raw.get("content", ""),
            reading_status=raw.get("reading_status", "to-read"),
            priority=raw.get("priority", "medium"),
            tags=list(raw.get("tags", [])),
            notes=raw.get("notes", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "doc_type": self.doc_type,
            "url": self.url,
            "published_date": self.published_date,
            "authors": self.authors,
            "institutions": self.institutions,
            "identifiers": self.identifiers,
            "relations": [
                {
                    "relation_type": r.relation_type,
                    "target_doc_id": r.target_doc_id,
                }
                for r in self.relations
            ],
            "reading_status": self.reading_status,
            "priority": self.priority,
            "tags": self.tags,
            "notes": self.notes,
            "content": self.content,
        }


@dataclass(frozen=True)
class SemanticChunk:
    """A semantically coherent segment of a document indexed for concepts and taxonomy."""

    chunk_id: str
    doc_id: str
    section_index: int
    heading: str
    text: str
    token_count: int
    key_terms: list[tuple[str, int]]
    concept_ids: list[str]
    taxonomy_paths: list[str]
    technology_areas: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "section_index": self.section_index,
            "heading": self.heading,
            "text": self.text,
            "token_count": self.token_count,
            "key_terms": [
                {"term": term, "count": count} for term, count in self.key_terms
            ],
            "concept_ids": self.concept_ids,
            "taxonomy_paths": self.taxonomy_paths,
            "technology_areas": self.technology_areas,
        }


@dataclass(frozen=True)
class TaxonomyNode:
    """Node in the conceptual taxonomy hierarchy (pre-OntoLogic class hierarchy)."""

    path: str
    label: str
    parent_path: str | None
    technology_area: str
    keywords: tuple[str, ...]
    description: str
    ontologic_class_uri: str


@dataclass(frozen=True)
class ConceptDefinition:
    """Canonical domain concept for indexing chunks, word clouds, and semantic links."""

    concept_id: str
    label: str
    taxonomy_path: str
    technology_area: str
    surface_forms: tuple[str, ...]
    related_concepts: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class GraphNode:
    """Vertex in the reading list knowledge graph."""

    node_id: str
    node_type: str
    label: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GraphEdge:
    """Directed, typed edge in the reading list knowledge graph."""

    source: str
    target: str
    predicate: str
    properties: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeGraph:
    """Property graph with JSON-LD `@context` hooks for future OntoLogic integration."""

    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)

    def add_node(self, node: GraphNode) -> None:
        if node.node_id not in self.nodes:
            self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        key = (edge.source, edge.target, edge.predicate)
        existing = {(e.source, e.target, e.predicate) for e in self.edges}
        if key not in existing:
            self.edges.append(edge)

    def to_dict(self) -> dict[str, Any]:
        sorted_nodes = [
            asdict(self.nodes[k]) for k in sorted(self.nodes.keys())
        ]
        sorted_edges = [
            asdict(e)
            for e in sorted(
                self.edges, key=lambda x: (x.source, x.predicate, x.target)
            )
        ]
        return {
            "@context": {
                "ontologic": "https://ontologic.dev/schema/v1#",
                "skos": "http://www.w3.org/2004/02/skos/core#",
                "dcterms": "http://purl.org/dc/terms/",
                "Document": "ontologic:Document",
                "SemanticChunk": "ontologic:SemanticChunk",
                "Concept": "skos:Concept",
                "TaxonomyCategory": "ontologic:TaxonomyCategory",
                "TechnologyArea": "ontologic:TechnologyArea",
            },
            "summary": {
                "node_count": len(sorted_nodes),
                "edge_count": len(sorted_edges),
            },
            "nodes": sorted_nodes,
            "edges": sorted_edges,
        }
