# ADR 0001: Lightweight Semantic Chunking and Conceptual Taxonomy Before OntoLogic Integration

- **Status:** Accepted
- **Date:** 2026-11-04

## Context

We are building a reading-list repository for technical articles, technical papers, and academic papers (starting with Semiconductor Engineering's coverage of *BARE-AI: Bit-Flip Attack Resilience in AI Hardware through Built-in Performance Monitors*, `arXiv:2610.08739v2`). We need to semantically chunk documents, compute word-cloud term distributions, categorize content into a conceptual hierarchy/taxonomy and technology areas, and connect everything in a knowledge graph. Later, the repository will integrate with **OntoLogic** for full ontological reasoning.

## Decision

1. Implement a zero-dependency Python 3.11+ core (`src/reading_list/`) that performs deterministic section/sentence semantic chunking, word-cloud frequency normalization, surface-form concept matching, and hierarchical taxonomy classification with ancestor rollup.
2. Emit JSON-LD compatible `@context` declarations and `ontologic_class_uri` identifiers on every taxonomy category and knowledge graph export (`output/knowledge_graph.json`) so future OntoLogic ingestion requires no schema migration.

## Consequences

- **Positive:** Immediate, deterministic execution with zero third-party runtime dependencies; every artifact in `output/` can be regenerated and verified in milliseconds.
- **Positive:** Forward-compatible with OntoLogic via pre-assigned `ontologic:*` URIs and SKOS/JSON-LD contexts.
- **Trade-off:** Surface-form and keyword matching is lexical/rule-based until vector embeddings or OntoLogic reasoners are attached in Phase 2.
