"""Static GitHub Pages dashboard generator for the reading-db sister repository."""

from __future__ import annotations

import json
from typing import Any

from reading_list.models import Document, KnowledgeGraph, SemanticChunk


def render_github_pages_html(
    documents: list[Document],
    chunks_by_doc: dict[str, list[SemanticChunk]],
    word_cloud: dict[str, Any],
    taxonomy_index: dict[str, Any],
    kg: KnowledgeGraph,
) -> str:
    """Render a self-contained, interactive GitHub Pages HTML application (`index.html`)."""
    docs_payload = []
    for doc in documents:
        doc_chunks = [c.to_dict() for c in chunks_by_doc.get(doc.doc_id, [])]
        all_concepts = sorted({cid for c in doc_chunks for cid in c["concept_ids"]})
        all_tax = sorted({p for c in doc_chunks for p in c["taxonomy_paths"]})
        all_tech = sorted({t for c in doc_chunks for t in c["technology_areas"]})
        docs_payload.append(
            {
                **doc.to_dict(),
                "chunks": doc_chunks,
                "concept_ids": all_concepts,
                "taxonomy_paths": all_tax,
                "technology_areas": all_tech,
                "word_cloud": word_cloud.get("by_document", {}).get(doc.doc_id, []),
            }
        )

    embedded_data = {
        "documents": docs_payload,
        "word_cloud": word_cloud.get("global_word_cloud", []),
        "taxonomy": taxonomy_index.get("taxonomy_categories", []),
        "knowledge_graph": kg.to_dict(),
    }

    data_json = json.dumps(embedded_data, sort_keys=True)
    jsonld_str = json.dumps(kg.to_dict(), indent=2, sort_keys=True)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Reading DB — Semantic Knowledge Graph &amp; Conceptual Taxonomy</title>
  <meta name="description" content="Interactive knowledge graph, semantic chunks, word cloud, and conceptual taxonomy for technical articles and academic papers." />
  <script type="application/ld+json">
{jsonld_str}
  </script>
  <style>
    :root {{
      --bg: #0b0f19;
      --bg-elevated: rgba(19, 27, 46, 0.78);
      --bg-card: rgba(23, 33, 56, 0.85);
      --bg-chip: rgba(56, 189, 248, 0.12);
      --border: rgba(148, 163, 184, 0.18);
      --border-strong: rgba(56, 189, 248, 0.45);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-2: #a855f7;
      --accent-3: #10b981;
      --accent-warn: #f59e0b;
      --accent-danger: #f43f5e;
      --shadow: 0 18px 40px -15px rgba(2, 6, 23, 0.75);
      --radius: 14px;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
    }}
    [data-theme="light"] {{
      --bg: #f8fafc;
      --bg-elevated: rgba(255, 255, 255, 0.88);
      --bg-card: #ffffff;
      --bg-chip: rgba(2, 132, 199, 0.1);
      --border: rgba(15, 23, 42, 0.12);
      --border-strong: rgba(2, 132, 199, 0.5);
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #0284c7;
      --accent-2: #7c3aed;
      --accent-3: #059669;
      --shadow: 0 12px 30px -10px rgba(15, 23, 42, 0.1);
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background:
        radial-gradient(circle at 12% 10%, rgba(56, 189, 248, 0.12), transparent 35%),
        radial-gradient(circle at 88% 12%, rgba(168, 85, 247, 0.12), transparent 38%),
        var(--bg);
      color: var(--text);
      line-height: 1.55;
      min-height: 100vh;
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .shell {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 1.75rem 1.5rem 4rem;
    }}
    header.hero {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1.25rem;
      padding: 1.5rem 1.75rem;
      border-radius: var(--radius);
      background: var(--bg-elevated);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 1.5rem;
    }}
    .brand-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      text-transform: uppercase;
      letter-spacing: 0.09em;
      color: var(--accent);
      background: var(--bg-chip);
      padding: 0.28rem 0.65rem;
      border-radius: 999px;
      border: 1px solid var(--border-strong);
      margin-bottom: 0.6rem;
    }}
    h1 {{
      margin: 0 0 0.4rem;
      font-size: clamp(1.55rem, 2.5vw, 2.15rem);
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      margin: 0;
      color: var(--text-muted);
      max-width: 760px;
      font-size: 0.96rem;
    }}
    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      align-items: center;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 0.46rem 0.82rem;
      border-radius: 9px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }}
    .btn:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
      text-decoration: none;
    }}
    .btn-sm {{
      padding: 0.28rem 0.6rem;
      font-size: 0.75rem;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border: none;
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
      gap: 0.9rem;
      margin-bottom: 1.5rem;
    }}
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1rem 1.15rem;
      box-shadow: var(--shadow);
    }}
    .kpi-value {{
      font-size: 1.75rem;
      font-weight: 800;
      font-family: var(--font-mono);
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .kpi-label {{
      font-size: 0.78rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-top: 0.2rem;
    }}
    .dashboard-grid {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 1.25rem;
      margin-bottom: 1.5rem;
    }}
    @media (max-width: 1024px) {{
      .dashboard-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .panel {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
    }}
    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 0.85rem;
    }}
    .panel-title {{
      margin: 0;
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }}
    .panel-subtitle {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    #graph-container {{
      position: relative;
      width: 100%;
      height: 430px;
      border-radius: 10px;
      background: rgba(2, 6, 23, 0.35);
      border: 1px solid var(--border);
      overflow: hidden;
      touch-action: none;
    }}
    .panel.graph-fullscreen {{
      position: fixed;
      inset: 0.75rem;
      z-index: 1000;
      margin: 0;
      width: calc(100vw - 1.5rem);
      height: calc(100vh - 1.5rem);
      background: var(--bg-card);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border-strong);
      box-shadow: 0 30px 90px rgba(0, 0, 0, 0.85);
    }}
    .panel.graph-fullscreen #graph-container {{
      flex: 1;
      height: auto;
      min-height: 0;
    }}
    body.has-fullscreen-graph {{
      overflow: hidden;
    }}
    [data-theme="light"] #graph-container {{
      background: #f1f5f9;
    }}
    #kg-svg {{
      width: 100%;
      height: 100%;
      cursor: grab;
      user-select: none;
      -webkit-user-select: none;
    }}
    #kg-svg.dragging-canvas, #kg-svg.dragging-node {{
      cursor: grabbing;
    }}
    .graph-toolbar {{
      position: absolute;
      top: 0.65rem;
      right: 0.65rem;
      display: flex;
      gap: 0.35rem;
      z-index: 4;
    }}
    .graph-status-banner {{
      position: absolute;
      left: 0.65rem;
      bottom: 0.65rem;
      right: 0.65rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      padding: 0.45rem 0.75rem;
      border-radius: 8px;
      background: var(--bg-elevated);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-strong);
      font-size: 0.78rem;
      z-index: 4;
      pointer-events: auto;
    }}
    .graph-status-banner[hidden] {{
      display: none !important;
    }}
    .graph-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 0.75rem;
      font-size: 0.76rem;
      color: var(--text-muted);
    }}
    .legend-item {{
      display: inline-flex;
      align-items: center;
      gap: 0.38rem;
      cursor: pointer;
      padding: 0.25rem 0.6rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--text);
      user-select: none;
      transition: all 0.15s ease;
    }}
    .legend-item:hover {{
      border-color: var(--accent);
    }}
    .legend-item.muted {{
      opacity: 0.38;
      text-decoration: line-through;
    }}
    .legend-dot {{
      width: 9px;
      height: 9px;
      border-radius: 50%;
    }}
    .word-cloud-box {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 0.45rem 0.65rem;
      padding: 0.9rem;
      border-radius: 10px;
      background: rgba(2, 6, 23, 0.25);
      border: 1px solid var(--border);
      min-height: 185px;
      margin-bottom: 1rem;
    }}
    [data-theme="light"] .word-cloud-box {{
      background: #f8fafc;
    }}
    .wc-term {{
      cursor: pointer;
      font-family: var(--font-mono);
      padding: 0.15rem 0.45rem;
      border-radius: 6px;
      transition: all 0.15s ease;
      border: 1px solid transparent;
      user-select: none;
    }}
    .wc-term:hover, .wc-term.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
      transform: scale(1.06);
    }}
    .taxonomy-list {{
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      max-height: 220px;
      overflow-y: auto;
      padding-right: 0.25rem;
    }}
    .tax-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      padding: 0.48rem 0.65rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      font-size: 0.8rem;
      cursor: pointer;
      transition: border-color 0.15s ease;
      user-select: none;
    }}
    .tax-item:hover, .tax-item.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
    }}
    .tax-uri {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--accent-2);
    }}
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 0.95rem 1.15rem;
      border-radius: var(--radius);
      margin-bottom: 1.2rem;
      box-shadow: var(--shadow);
    }}
    .filter-bar input, .filter-bar select {{
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 0.48rem 0.75rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-family: var(--font-sans);
    }}
    .filter-bar input {{
      flex: 1;
      min-width: 220px;
    }}
    .active-filters-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      align-items: center;
      margin-bottom: 1rem;
    }}
    .active-filters-row[hidden] {{
      display: none !important;
    }}
    .filter-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      padding: 0.25rem 0.65rem;
      border-radius: 999px;
      background: var(--bg-chip);
      border: 1px solid var(--border-strong);
      color: var(--accent);
      cursor: pointer;
    }}
    .doc-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 1.1rem;
    }}
    @media (max-width: 520px) {{
      .doc-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    .doc-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.2rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.85rem;
      transition: transform 0.15s ease, border-color 0.15s ease;
    }}
    .doc-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-strong);
    }}
    .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      align-items: center;
    }}
    .badge {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 600;
      padding: 0.18rem 0.5rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      text-transform: uppercase;
    }}
    .status-read {{ color: var(--accent-3); border-color: rgba(16, 185, 129, 0.4); }}
    .status-reading {{ color: var(--accent); border-color: rgba(56, 189, 248, 0.4); }}
    .status-to-read {{ color: var(--accent-warn); border-color: rgba(245, 158, 11, 0.4); }}
    .prio-high {{ color: var(--accent-danger); border-color: rgba(244, 63, 94, 0.4); }}
    .doc-title {{
      margin: 0.25rem 0;
      font-size: 1.05rem;
      font-weight: 700;
      line-height: 1.35;
    }}
    .doc-meta {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .chip-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
    }}
    .chip {{
      font-size: 0.72rem;
      font-family: var(--font-mono);
      padding: 0.16rem 0.48rem;
      border-radius: 6px;
      background: var(--bg-chip);
      color: var(--accent);
      border: 1px solid rgba(56, 189, 248, 0.22);
      cursor: pointer;
    }}
    .chip:hover {{
      border-color: var(--accent);
    }}
    .chip-concept {{
      color: var(--accent-2);
      background: rgba(168, 85, 247, 0.1);
      border-color: rgba(168, 85, 247, 0.25);
    }}
    dialog#chunk-modal {{
      width: min(860px, 94vw);
      max-height: 86vh;
      background: var(--bg-card);
      color: var(--text);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius);
      padding: 0;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75);
    }}
    dialog#chunk-modal::backdrop {{
      background: rgba(2, 6, 23, 0.72);
      backdrop-filter: blur(5px);
    }}
    .modal-head {{
      padding: 1.15rem 1.4rem;
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 1rem;
      position: sticky;
      top: 0;
      background: var(--bg-card);
    }}
    .modal-body {{
      padding: 1.25rem 1.4rem;
      overflow-y: auto;
      max-height: calc(86vh - 80px);
      display: flex;
      flex-direction: column;
      gap: 0.9rem;
    }}
    .chunk-box {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.95rem 1.1rem;
      background: rgba(2, 6, 23, 0.22);
    }}
    .chunk-head {{
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      color: var(--accent);
      margin-bottom: 0.45rem;
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <div>
        <div class="brand-eyebrow">OntoLogic-Ready Knowledge Base &bull; reading-db</div>
        <h1>Reading List Knowledge Graph &amp; Taxonomy</h1>
        <p class="subtitle">
          Semantically chunked technical articles, academic papers, and research notes linked across conceptual hierarchies, technology areas, and domain word clouds.
        </p>
      </div>
      <div class="hero-actions">
        <a class="btn" href="knowledge_graph.json" target="_blank" rel="noopener">JSON-LD Graph</a>
        <a class="btn" href="taxonomy_tree.json" target="_blank" rel="noopener">Taxonomy JSON</a>
        <a class="btn" href="chunks.json" target="_blank" rel="noopener">Chunks JSON</a>
        <a class="btn" href="summary.md" target="_blank" rel="noopener">Summary MD</a>
        <button class="btn btn-primary" id="theme-toggle" type="button">Toggle Theme</button>
      </div>
    </header>

    <section class="kpi-grid" id="kpi-grid"></section>

    <section class="dashboard-grid">
      <div class="panel" id="graph-panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title">Interactive Knowledge Graph</h2>
            <div class="panel-subtitle">Click any node to filter related documents &bull; Drag nodes to rearrange &bull; Drag canvas or use +/- to pan/zoom</div>
          </div>
          <div style="display:flex; gap:0.4rem; flex-wrap:wrap;">
            <button class="btn btn-sm" id="fullscreen-graph-btn" type="button" title="Toggle Full Web-Page View">&#x26F6; Full Page</button>
            <button class="btn btn-sm" id="relayout-graph-btn" type="button">Re-Layout</button>
            <button class="btn btn-sm" id="reset-graph-btn" type="button">Reset Filter</button>
          </div>
        </div>
        <div id="graph-container">
          <div class="graph-toolbar">
            <button class="btn btn-sm" id="zoom-in-btn" type="button" title="Zoom In">+</button>
            <button class="btn btn-sm" id="zoom-out-btn" type="button" title="Zoom Out">&minus;</button>
            <button class="btn btn-sm" id="zoom-fit-btn" type="button" title="Reset View">Fit</button>
            <button class="btn btn-sm" id="toolbar-fullscreen-btn" type="button" title="Toggle Full Web-Page View">&#x26F6;</button>
          </div>
          <svg id="kg-svg" viewBox="0 0 820 430" preserveAspectRatio="xMidYMid meet"></svg>
          <div class="graph-status-banner" id="graph-status-banner" hidden>
            <span id="graph-status-text"></span>
            <button class="btn btn-sm" id="graph-status-clear" type="button">&times; Clear</button>
          </div>
        </div>
        <div class="graph-legend" id="graph-legend"></div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title">Global Word Cloud &amp; Conceptual Hierarchy</h2>
            <div class="panel-subtitle">Click any term or taxonomy category to filter documents</div>
          </div>
        </div>
        <div class="word-cloud-box" id="word-cloud"></div>
        <div class="panel-subtitle" style="margin-bottom: 0.4rem; font-weight: 600;">Conceptual Taxonomy (with OntoLogic Class URIs)</div>
        <div class="taxonomy-list" id="taxonomy-list"></div>
      </div>
    </section>

    <section class="filter-bar">
      <input type="search" id="search-input" placeholder="Search title, abstract chunks, concepts, authors, or notes..." />
      <select id="status-filter">
        <option value="">All Statuses</option>
        <option value="to-read">To-Read</option>
        <option value="reading">Reading</option>
        <option value="read">Read</option>
      </select>
      <select id="priority-filter">
        <option value="">All Priorities</option>
        <option value="high">High Priority</option>
        <option value="medium">Medium Priority</option>
        <option value="low">Low Priority</option>
      </select>
      <select id="type-filter">
        <option value="">All Document Types</option>
        <option value="academic_paper">Academic Papers</option>
        <option value="technical_article">Technical Articles</option>
        <option value="technical_paper">Technical Papers</option>
        <option value="note">Research Notes</option>
      </select>
      <select id="tech-filter">
        <option value="">All Technology Areas</option>
      </select>
      <button class="btn" id="clear-filters" type="button">Clear All</button>
    </section>

    <div class="active-filters-row" id="active-filters-row" hidden></div>

    <section class="doc-grid" id="doc-grid"></section>
  </div>

  <dialog id="chunk-modal">
    <div class="modal-head">
      <div>
        <div class="brand-eyebrow" id="modal-doc-id"></div>
        <h3 id="modal-title" style="margin: 0.2rem 0 0;"></h3>
      </div>
      <button class="btn" id="close-modal" type="button">Close</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </dialog>

  <script>
    const DB = {data_json};

    const NODE_COLORS = {{
      Document: "#38bdf8",
      Concept: "#a855f7",
      TaxonomyCategory: "#10b981",
      TechnologyArea: "#f59e0b",
      Institution: "#f43f5e",
      Author: "#64748b",
      SemanticChunk: "#06b6d4"
    }};

    const state = {{
      query: "",
      status: "",
      priority: "",
      docType: "",
      techArea: "",
      taxonomyPath: "",
      conceptId: "",
      docId: "",
      selectedGraphNodeId: "",
      hiddenNodeTypes: new Set()
    }};

    let graphNodes = [];
    let graphEdges = [];
    let viewBox = {{ x: 0, y: 0, w: 820, h: 430 }};

    function escapeHtml(str) {{
      return String(str ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function getFilteredDocuments() {{
      return DB.documents.filter(doc => {{
        if (state.docId && doc.doc_id !== state.docId) return false;
        if (state.status && doc.reading_status !== state.status) return false;
        if (state.priority && doc.priority !== state.priority) return false;
        if (state.docType && doc.doc_type !== state.docType) return false;
        if (state.techArea && !doc.technology_areas.includes(state.techArea)) return false;
        if (state.taxonomyPath && !doc.taxonomy_paths.includes(state.taxonomyPath)) return false;
        if (state.conceptId && !doc.concept_ids.includes(state.conceptId)) return false;
        if (state.query) {{
          const q = state.query.toLowerCase();
          const hay = `${{doc.title}} ${{doc.content}} ${{doc.authors.join(" ")}} ${{doc.tags.join(" ")}} ${{doc.notes}}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});
    }}

    function initKPIs() {{
      const kpiGrid = document.getElementById("kpi-grid");
      const totalChunks = DB.documents.reduce((acc, d) => acc + d.chunks.length, 0);
      const concepts = DB.knowledge_graph.nodes.filter(n => n.node_type === "Concept").length;
      const kpis = [
        {{ label: "Tracked Documents", value: DB.documents.length }},
        {{ label: "Semantic Chunks", value: totalChunks }},
        {{ label: "Domain Concepts", value: concepts }},
        {{ label: "Taxonomy Classes", value: DB.taxonomy.length }},
        {{ label: "Graph Nodes", value: DB.knowledge_graph.summary.node_count }},
        {{ label: "Graph Edges", value: DB.knowledge_graph.summary.edge_count }}
      ];
      kpiGrid.innerHTML = kpis.map(k => `
        <div class="kpi-card">
          <div class="kpi-value">${{k.value}}</div>
          <div class="kpi-label">${{k.label}}</div>
        </div>
      `).join("");
    }}

    function initTechDropdown() {{
      const select = document.getElementById("tech-filter");
      const areas = new Set();
      DB.documents.forEach(d => d.technology_areas.forEach(t => areas.add(t)));
      [...areas].sort().forEach(area => {{
        const opt = document.createElement("option");
        opt.value = area;
        opt.textContent = area;
        select.appendChild(opt);
      }});
    }}

    function renderWordCloud() {{
      const box = document.getElementById("word-cloud");
      box.innerHTML = DB.word_cloud.slice(0, 26).map(item => {{
        const size = (0.76 + item.weight * 0.68).toFixed(2);
        const active = state.query.toLowerCase() === item.term.toLowerCase() ? "active" : "";
        return `<span class="wc-term ${{active}}" style="font-size:${{size}}rem" data-term="${{escapeHtml(item.term)}}" title="Frequency: ${{item.count}}">${{escapeHtml(item.term)}}</span>`;
      }}).join("");
      box.querySelectorAll(".wc-term").forEach(el => {{
        el.addEventListener("click", () => {{
          const term = el.dataset.term;
          state.query = state.query === term ? "" : term;
          document.getElementById("search-input").value = state.query;
          refreshAll();
        }});
      }});
    }}

    function renderTaxonomy() {{
      const list = document.getElementById("taxonomy-list");
      list.innerHTML = DB.taxonomy.map(cat => {{
        const active = state.taxonomyPath === cat.path ? "active" : "";
        const depth = (cat.path.match(/>/g) || []).length;
        const indent = depth * 12;
        return `
          <div class="tax-item ${{active}}" style="margin-left:${{indent}}px" data-path="${{escapeHtml(cat.path)}}">
            <div>
              <div style="font-weight:600">${{escapeHtml(cat.label)}}</div>
              <div class="tax-uri">${{escapeHtml(cat.ontologic_class_uri)}} &bull; ${{escapeHtml(cat.technology_area)}}</div>
            </div>
            <span class="badge">${{cat.document_ids.length}} docs</span>
          </div>
        `;
      }}).join("");
      list.querySelectorAll(".tax-item").forEach(el => {{
        el.addEventListener("click", () => {{
          const p = el.dataset.path;
          state.taxonomyPath = state.taxonomyPath === p ? "" : p;
          if (!state.taxonomyPath && state.selectedGraphNodeId.startsWith("taxonomy:")) {{
            state.selectedGraphNodeId = "";
          }}
          refreshAll();
        }});
      }});
    }}

    function renderActiveFilterPills(filteredDocs) {{
      const row = document.getElementById("active-filters-row");
      const pills = [];
      if (state.docId) pills.push({{ key: "docId", label: `Document: ${{state.docId}}` }});
      if (state.conceptId) pills.push({{ key: "conceptId", label: `Concept: ${{state.conceptId.replace("concept:", "")}}` }});
      if (state.taxonomyPath) pills.push({{ key: "taxonomyPath", label: `Taxonomy: ${{state.taxonomyPath}}` }});
      if (state.techArea) pills.push({{ key: "techArea", label: `Tech Area: ${{state.techArea}}` }});
      if (state.status) pills.push({{ key: "status", label: `Status: ${{state.status}}` }});
      if (state.priority) pills.push({{ key: "priority", label: `Priority: ${{state.priority}}` }});
      if (state.docType) pills.push({{ key: "docType", label: `Type: ${{state.docType}}` }});
      if (state.query) pills.push({{ key: "query", label: `Search: "${{state.query}}"` }});

      if (!pills.length) {{
        row.hidden = true;
        row.innerHTML = "";
      }} else {{
        row.hidden = false;
        row.innerHTML = `
          <span style="font-size:0.78rem; color:var(--text-muted);">Showing ${{filteredDocs.length}} of ${{DB.documents.length}} documents:</span>
          ${{pills.map(p => `<span class="filter-pill" data-key="${{p.key}}">${{escapeHtml(p.label)}} &times;</span>`).join("")}}
        `;
        row.querySelectorAll(".filter-pill").forEach(el => {{
          el.addEventListener("click", () => {{
            const k = el.dataset.key;
            state[k] = "";
            state.selectedGraphNodeId = "";
            if (k === "query") document.getElementById("search-input").value = "";
            if (k === "status") document.getElementById("status-filter").value = "";
            if (k === "priority") document.getElementById("priority-filter").value = "";
            if (k === "docType") document.getElementById("type-filter").value = "";
            if (k === "techArea") document.getElementById("tech-filter").value = "";
            refreshAll();
          }});
        }});
      }}

      const banner = document.getElementById("graph-status-banner");
      const bannerText = document.getElementById("graph-status-text");
      if (pills.length) {{
        banner.hidden = false;
        bannerText.textContent = `${{pills.map(p => p.label).join(" • ")}} (${{filteredDocs.length}} matching docs)`;
      }} else {{
        banner.hidden = true;
      }}
    }}

    function renderDocuments() {{
      const grid = document.getElementById("doc-grid");
      const filtered = getFilteredDocuments();
      renderActiveFilterPills(filtered);

      if (!filtered.length) {{
        grid.innerHTML = `<div class="panel" style="grid-column: 1 / -1; text-align:center; color: var(--text-muted);">No documents match the current filters. Click "Reset Filter" or "Clear All".</div>`;
        return;
      }}

      grid.innerHTML = filtered.map(doc => {{
        const statusClass = `status-${{doc.reading_status}}`;
        const prioClass = doc.priority === "high" ? "prio-high" : "";
        const authors = doc.authors.length ? doc.authors.join(", ") : "Staff / Research Note";
        const inst = doc.institutions.length ? ` &bull; ${{doc.institutions.join(", ")}}` : "";
        const relBadges = doc.relations.map(r => `<span class="badge">${{escapeHtml(r.relation_type)}} &rarr; ${{escapeHtml(r.target_doc_id)}}</span>`).join("");
        const techChips = doc.technology_areas.slice(0, 4).map(t => `<span class="chip doc-tech-chip" data-tech="${{escapeHtml(t)}}">${{escapeHtml(t)}}</span>`).join("");
        const conceptChips = doc.concept_ids.map(c => `<span class="chip chip-concept doc-concept-chip" data-concept="${{escapeHtml(c)}}">${{escapeHtml(c.replace("concept:", ""))}}</span>`).join("");
        return `
          <article class="doc-card">
            <div>
              <div class="badge-row">
                <span class="badge ${{statusClass}}">${{escapeHtml(doc.reading_status)}}</span>
                <span class="badge ${{prioClass}}">priority: ${{escapeHtml(doc.priority)}}</span>
                <span class="badge">${{escapeHtml(doc.doc_type.replace("_", " "))}}</span>
                ${{doc.published_date ? `<span class="badge">${{escapeHtml(doc.published_date)}}</span>` : ""}}
              </div>
              <h3 class="doc-title">
                ${{doc.url ? `<a href="${{escapeHtml(doc.url)}}" target="_blank" rel="noopener">${{escapeHtml(doc.title)}}</a>` : escapeHtml(doc.title)}}
              </h3>
              <div class="doc-meta">${{escapeHtml(authors)}}${{inst}}</div>
              ${{doc.notes ? `<p style="font-size:0.82rem; color: var(--text-muted); margin: 0.5rem 0 0;"><strong>Notes:</strong> ${{escapeHtml(doc.notes)}}</p>` : ""}}
            </div>
            <div>
              <div class="chip-list" style="margin-bottom:0.45rem;">${{techChips}}</div>
              <div class="chip-list" style="margin-bottom:0.65rem;">${{conceptChips}}</div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                <div class="badge-row">${{relBadges}}</div>
                <button class="btn inspect-btn" data-doc="${{escapeHtml(doc.doc_id)}}" type="button">
                  Inspect ${{doc.chunks.length}} Semantic Chunks
                </button>
              </div>
            </div>
          </article>
        `;
      }}).join("");

      grid.querySelectorAll(".inspect-btn").forEach(btn => {{
        btn.addEventListener("click", () => openChunkModal(btn.dataset.doc));
      }});
      grid.querySelectorAll(".doc-tech-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          const t = chip.dataset.tech;
          state.techArea = state.techArea === t ? "" : t;
          document.getElementById("tech-filter").value = state.techArea;
          refreshAll();
        }});
      }});
      grid.querySelectorAll(".doc-concept-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          const c = chip.dataset.concept;
          state.conceptId = state.conceptId === c ? "" : c;
          state.selectedGraphNodeId = state.conceptId;
          refreshAll();
        }});
      }});
    }}

    function openChunkModal(docId) {{
      const doc = DB.documents.find(d => d.doc_id === docId);
      if (!doc) return;
      document.getElementById("modal-doc-id").textContent = `${{doc.doc_id}} • ${{doc.doc_type}}`;
      document.getElementById("modal-title").textContent = doc.title;
      const body = document.getElementById("modal-body");
      body.innerHTML = doc.chunks.map(ch => `
        <div class="chunk-box">
          <div class="chunk-head">
            <span>${{escapeHtml(ch.chunk_id)}} &mdash; ${{escapeHtml(ch.heading)}}</span>
            <span>${{ch.token_count}} words</span>
          </div>
          <p style="margin: 0 0 0.65rem; font-size: 0.9rem;">${{escapeHtml(ch.text)}}</p>
          <div class="chip-list" style="margin-bottom: 0.35rem;">
            ${{ch.concept_ids.map(c => `<span class="chip chip-concept">${{escapeHtml(c)}}</span>`).join("")}}
          </div>
          <div class="chip-list">
            ${{ch.taxonomy_paths.map(p => `<span class="chip">${{escapeHtml(p)}}</span>`).join("")}}
          </div>
        </div>
      `).join("");
      document.getElementById("chunk-modal").showModal();
    }}

    function computeGraphLayout() {{
      const allowedTypes = new Set(["Document", "Concept", "TaxonomyCategory", "TechnologyArea"]);
      const rawNodes = DB.knowledge_graph.nodes.filter(n => allowedTypes.has(n.node_type));

      const byType = {{
        Document: [],
        Concept: [],
        TaxonomyCategory: [],
        TechnologyArea: []
      }};
      rawNodes.forEach(n => {{
        if (byType[n.node_type]) byType[n.node_type].push(n);
      }});

      graphNodes = [];
      const ringConfig = [
        {{ type: "Document", rx: 115, ry: 72, offset: 0.15 }},
        {{ type: "Concept", rx: 225, ry: 125, offset: 0.55 }},
        {{ type: "TaxonomyCategory", rx: 315, ry: 165, offset: 0.95 }},
        {{ type: "TechnologyArea", rx: 365, ry: 188, offset: 1.35 }}
      ];

      ringConfig.forEach(cfg => {{
        const list = byType[cfg.type] || [];
        list.forEach((n, idx) => {{
          const angle = cfg.offset + (2 * Math.PI * idx) / Math.max(1, list.length);
          graphNodes.push({{
            ...n,
            x: 410 + Math.cos(angle) * cfg.rx,
            y: 215 + Math.sin(angle) * cfg.ry
          }});
        }});
      }});

      const nodeById = Object.fromEntries(graphNodes.map(n => [n.node_id, n]));
      graphEdges = DB.knowledge_graph.edges.filter(e => nodeById[e.source] && nodeById[e.target]);

      // Force-directed repulsion + spring relaxation
      for (let iter = 0; iter < 80; iter++) {{
        for (let i = 0; i < graphNodes.length; i++) {{
          for (let j = i + 1; j < graphNodes.length; j++) {{
            const dx = graphNodes[j].x - graphNodes[i].x;
            const dy = graphNodes[j].y - graphNodes[i].y;
            const dist = Math.hypot(dx, dy) || 0.1;
            const minDist = 66;
            if (dist < minDist) {{
              const push = (minDist - dist) * 0.22;
              const ux = (dx / dist) * push;
              const uy = (dy / dist) * push;
              graphNodes[j].x += ux;
              graphNodes[j].y += uy;
              graphNodes[i].x -= ux;
              graphNodes[i].y -= uy;
            }}
          }}
        }}
        graphNodes.forEach(n => {{
          n.x = Math.max(48, Math.min(755, n.x));
          n.y = Math.max(30, Math.min(395, n.y));
        }});
      }}
    }}

    function isNodeActiveFilter(node) {{
      if (state.selectedGraphNodeId === node.node_id) return true;
      if (node.node_type === "Document" && state.docId && node.node_id === `doc:${{state.docId}}`) return true;
      if (node.node_type === "Concept" && state.conceptId === node.node_id) return true;
      if (node.node_type === "TechnologyArea" && state.techArea === node.label) return true;
      if (node.node_type === "TaxonomyCategory" && state.taxonomyPath && node.properties && node.properties.path === state.taxonomyPath) return true;
      return false;
    }}

    function handleGraphNodeClick(node) {{
      const alreadyActive = isNodeActiveFilter(node);
      // Reset previous graph-driven filter keys before setting the new one
      state.docId = "";
      state.conceptId = "";
      state.taxonomyPath = "";
      state.techArea = "";
      state.selectedGraphNodeId = "";
      document.getElementById("tech-filter").value = "";

      if (!alreadyActive) {{
        state.selectedGraphNodeId = node.node_id;
        if (node.node_type === "Document") {{
          state.docId = (node.properties && node.properties.doc_id) || node.node_id.replace("doc:", "");
        }} else if (node.node_type === "Concept") {{
          state.conceptId = node.node_id;
        }} else if (node.node_type === "TechnologyArea") {{
          state.techArea = node.label;
          document.getElementById("tech-filter").value = state.techArea;
        }} else if (node.node_type === "TaxonomyCategory") {{
          state.taxonomyPath = (node.properties && node.properties.path) || "";
          if (!state.taxonomyPath) {{
            const match = DB.taxonomy.find(t => t.label === node.label);
            if (match) state.taxonomyPath = match.path;
          }}
        }}
      }}
      refreshAll();
    }}

    function drawGraph() {{
      const svg = document.getElementById("kg-svg");
      const visibleNodes = graphNodes.filter(n => !state.hiddenNodeTypes.has(n.node_type));
      const nodeById = Object.fromEntries(visibleNodes.map(n => [n.node_id, n]));
      const visibleEdges = graphEdges.filter(e => nodeById[e.source] && nodeById[e.target]);

      // Determine active node(s) and their 1-hop neighbors for visual highlighting
      const activeIds = new Set(visibleNodes.filter(isNodeActiveFilter).map(n => n.node_id));
      const neighborIds = new Set(activeIds);
      visibleEdges.forEach(e => {{
        if (activeIds.has(e.source)) neighborIds.add(e.target);
        if (activeIds.has(e.target)) neighborIds.add(e.source);
      }});
      const hasHighlight = activeIds.size > 0;

      const edgeMarkup = visibleEdges.map((e, idx) => {{
        const s = nodeById[e.source];
        const t = nodeById[e.target];
        const connected = activeIds.has(e.source) || activeIds.has(e.target);
        const stroke = connected ? "var(--accent)" : "rgba(148,163,184,0.28)";
        const width = connected ? "2.4" : "1.2";
        const opacity = hasHighlight ? (connected ? "0.95" : "0.15") : "0.85";
        return `<line class="kg-edge" data-idx="${{idx}}" data-source="${{escapeHtml(e.source)}}" data-target="${{escapeHtml(e.target)}}" x1="${{s.x}}" y1="${{s.y}}" x2="${{t.x}}" y2="${{t.y}}" stroke="${{stroke}}" stroke-width="${{width}}" opacity="${{opacity}}" />`;
      }}).join("");

      const nodeMarkup = visibleNodes.map(n => {{
        const color = NODE_COLORS[n.node_type] || "#38bdf8";
        const isSelected = activeIds.has(n.node_id);
        const isNeighbor = neighborIds.has(n.node_id);
        const r = n.node_type === "Document" ? 11.5 : 8.5;
        const opacity = hasHighlight ? (isNeighbor ? "1" : "0.22") : "1";
        const shortLabel = n.label.length > 26 ? n.label.slice(0, 24) + "…" : n.label;
        const halo = isSelected
          ? `<circle class="kg-halo" r="${{r + 6}}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="3 2"></circle>`
          : "";
        return `
          <g class="kg-node" data-id="${{escapeHtml(n.node_id)}}" transform="translate(${{n.x}},${{n.y}})" opacity="${{opacity}}" style="cursor:grab">
            <title>${{escapeHtml(n.node_type)}}: ${{escapeHtml(n.label)}} (click to filter, drag to move)</title>
            ${{halo}}
            <circle r="${{r}}" fill="${{color}}" stroke="${{isSelected ? "#ffffff" : "#0f172a"}}" stroke-width="${{isSelected ? "2.8" : "2"}}"></circle>
            <text x="${{r + 5}}" y="4" fill="currentColor" font-size="${{isSelected ? "11.5" : "10.2"}}" font-weight="${{isSelected ? "700" : "500"}}" font-family="var(--font-sans)" pointer-events="none">${{escapeHtml(shortLabel)}}</text>
          </g>
        `;
      }}).join("");

      svg.innerHTML = `<g id="kg-viewport">${{edgeMarkup}}${{nodeMarkup}}</g>`;
    }}

    function renderGraphLegend() {{
      const legend = document.getElementById("graph-legend");
      const types = ["Document", "Concept", "TaxonomyCategory", "TechnologyArea"];
      legend.innerHTML = types.map(t => {{
        const muted = state.hiddenNodeTypes.has(t) ? "muted" : "";
        const count = graphNodes.filter(n => n.node_type === t).length;
        return `
          <button type="button" class="legend-item ${{muted}}" data-type="${{t}}" title="Click to show/hide ${{t}} nodes">
            <span class="legend-dot" style="background:${{NODE_COLORS[t]}}"></span>
            ${{t}} (${{count}})
          </button>
        `;
      }}).join("");

      legend.querySelectorAll(".legend-item").forEach(btn => {{
        btn.addEventListener("click", () => {{
          const t = btn.dataset.type;
          if (state.hiddenNodeTypes.has(t)) {{
            state.hiddenNodeTypes.delete(t);
          }} else {{
            state.hiddenNodeTypes.add(t);
          }}
          renderGraphLegend();
          drawGraph();
        }});
      }});
    }}

    function clientToSvgPoint(svg, clientX, clientY) {{
      const pt = svg.createSVGPoint();
      pt.x = clientX;
      pt.y = clientY;
      const ctm = svg.getScreenCTM();
      if (!ctm) return {{ x: clientX, y: clientY }};
      return pt.matrixTransform(ctm.inverse());
    }}

    function updateViewBox() {{
      const svg = document.getElementById("kg-svg");
      svg.setAttribute("viewBox", `${{viewBox.x.toFixed(1)}} ${{viewBox.y.toFixed(1)}} ${{viewBox.w.toFixed(1)}} ${{viewBox.h.toFixed(1)}}`);
    }}

    function setupGraphInteractions() {{
      const svg = document.getElementById("kg-svg");
      let dragState = null;

      svg.addEventListener("pointerdown", e => {{
        const nodeGroup = e.target.closest(".kg-node");
        if (nodeGroup) {{
          const nodeId = nodeGroup.dataset.id;
          const nodeObj = graphNodes.find(n => n.node_id === nodeId);
          if (!nodeObj) return;
          const startSvg = clientToSvgPoint(svg, e.clientX, e.clientY);
          dragState = {{
            mode: "node",
            nodeObj,
            nodeGroup,
            startClientX: e.clientX,
            startClientY: e.clientY,
            offsetX: nodeObj.x - startSvg.x,
            offsetY: nodeObj.y - startSvg.y,
            moved: false
          }};
          svg.classList.add("dragging-node");
          svg.setPointerCapture(e.pointerId);
          e.preventDefault();
        }} else {{
          dragState = {{
            mode: "pan",
            startClientX: e.clientX,
            startClientY: e.clientY,
            startViewX: viewBox.x,
            startViewY: viewBox.y,
            moved: false
          }};
          svg.classList.add("dragging-canvas");
          svg.setPointerCapture(e.pointerId);
        }}
      }});

      svg.addEventListener("pointermove", e => {{
        if (!dragState) return;
        const distPx = Math.hypot(e.clientX - dragState.startClientX, e.clientY - dragState.startClientY);
        if (distPx > 5) dragState.moved = true;

        if (dragState.mode === "node") {{
          const pt = clientToSvgPoint(svg, e.clientX, e.clientY);
          const nx = pt.x + dragState.offsetX;
          const ny = pt.y + dragState.offsetY;
          dragState.nodeObj.x = nx;
          dragState.nodeObj.y = ny;
          dragState.nodeGroup.setAttribute("transform", `translate(${{nx}},${{ny}})`);

          const id = dragState.nodeObj.node_id;
          svg.querySelectorAll(".kg-edge").forEach(line => {{
            if (line.dataset.source === id) {{
              line.setAttribute("x1", nx);
              line.setAttribute("y1", ny);
            }}
            if (line.dataset.target === id) {{
              line.setAttribute("x2", nx);
              line.setAttribute("y2", ny);
            }}
          }});
        }} else if (dragState.mode === "pan" && dragState.moved) {{
          const rect = svg.getBoundingClientRect();
          const scaleX = viewBox.w / Math.max(1, rect.width);
          const scaleY = viewBox.h / Math.max(1, rect.height);
          viewBox.x = dragState.startViewX - (e.clientX - dragState.startClientX) * scaleX;
          viewBox.y = dragState.startViewY - (e.clientY - dragState.startClientY) * scaleY;
          updateViewBox();
        }}
      }});

      function finishPointer(e) {{
        if (!dragState) return;
        const current = dragState;
        dragState = null;
        svg.classList.remove("dragging-node", "dragging-canvas");
        try {{
          if (e && e.pointerId != null && svg.hasPointerCapture(e.pointerId)) {{
            svg.releasePointerCapture(e.pointerId);
          }}
        }} catch (_) {{}}

        if (current.mode === "node" && !current.moved) {{
          handleGraphNodeClick(current.nodeObj);
        }}
      }}

      svg.addEventListener("pointerup", finishPointer);
      svg.addEventListener("pointercancel", finishPointer);

      svg.addEventListener("wheel", e => {{
        e.preventDefault();
        const factor = e.deltaY < 0 ? 0.88 : 1.14;
        const newW = Math.max(260, Math.min(1800, viewBox.w * factor));
        const newH = Math.max(136, Math.min(940, viewBox.h * factor));
        viewBox.x += (viewBox.w - newW) * 0.5;
        viewBox.y += (viewBox.h - newH) * 0.5;
        viewBox.w = newW;
        viewBox.h = newH;
        updateViewBox();
      }}, {{ passive: false }});

      document.getElementById("zoom-in-btn").addEventListener("click", () => {{
        viewBox.x += viewBox.w * 0.08;
        viewBox.y += viewBox.h * 0.08;
        viewBox.w *= 0.84;
        viewBox.h *= 0.84;
        updateViewBox();
      }});
      document.getElementById("zoom-out-btn").addEventListener("click", () => {{
        viewBox.x -= viewBox.w * 0.09;
        viewBox.y -= viewBox.h * 0.09;
        viewBox.w *= 1.18;
        viewBox.h *= 1.18;
        updateViewBox();
      }});
      document.getElementById("zoom-fit-btn").addEventListener("click", () => {{
        viewBox = {{ x: 0, y: 0, w: 820, h: 430 }};
        updateViewBox();
      }});
      document.getElementById("relayout-graph-btn").addEventListener("click", () => {{
        viewBox = {{ x: 0, y: 0, w: 820, h: 430 }};
        updateViewBox();
        computeGraphLayout();
        drawGraph();
      }});

      function toggleGraphFullscreen(forceState) {{
        const panel = document.getElementById("graph-panel");
        const headerBtn = document.getElementById("fullscreen-graph-btn");
        const toolbarBtn = document.getElementById("toolbar-fullscreen-btn");
        const isFull = typeof forceState === "boolean"
          ? forceState
          : !panel.classList.contains("graph-fullscreen");
        panel.classList.toggle("graph-fullscreen", isFull);
        document.body.classList.toggle("has-fullscreen-graph", isFull);
        headerBtn.innerHTML = isFull ? "&times; Normal View" : "&#x26F6; Full Page";
        toolbarBtn.innerHTML = isFull ? "&times;" : "&#x26F6;";
        toolbarBtn.title = isFull ? "Exit Full Web-Page View (Esc)" : "Expand to Full Web-Page View";
      }}

      document.getElementById("fullscreen-graph-btn").addEventListener("click", () => toggleGraphFullscreen());
      document.getElementById("toolbar-fullscreen-btn").addEventListener("click", () => toggleGraphFullscreen());
      document.addEventListener("keydown", e => {{
        if (e.key === "Escape") {{
          const panel = document.getElementById("graph-panel");
          if (panel && panel.classList.contains("graph-fullscreen")) {{
            toggleGraphFullscreen(false);
          }}
        }}
      }});
    }}

    function clearAllFilters() {{
      state.query = "";
      state.status = "";
      state.priority = "";
      state.docType = "";
      state.techArea = "";
      state.taxonomyPath = "";
      state.conceptId = "";
      state.docId = "";
      state.selectedGraphNodeId = "";
      document.getElementById("search-input").value = "";
      document.getElementById("status-filter").value = "";
      document.getElementById("priority-filter").value = "";
      document.getElementById("type-filter").value = "";
      document.getElementById("tech-filter").value = "";
      refreshAll();
    }}

    function refreshAll() {{
      drawGraph();
      renderWordCloud();
      renderTaxonomy();
      renderDocuments();
    }}

    document.getElementById("search-input").addEventListener("input", e => {{
      state.query = e.target.value.trim();
      refreshAll();
    }});
    document.getElementById("status-filter").addEventListener("change", e => {{
      state.status = e.target.value;
      refreshAll();
    }});
    document.getElementById("priority-filter").addEventListener("change", e => {{
      state.priority = e.target.value;
      refreshAll();
    }});
    document.getElementById("type-filter").addEventListener("change", e => {{
      state.docType = e.target.value;
      refreshAll();
    }});
    document.getElementById("tech-filter").addEventListener("change", e => {{
      state.techArea = e.target.value;
      refreshAll();
    }});
    document.getElementById("clear-filters").addEventListener("click", clearAllFilters);
    document.getElementById("reset-graph-btn").addEventListener("click", clearAllFilters);
    document.getElementById("graph-status-clear").addEventListener("click", clearAllFilters);
    document.getElementById("close-modal").addEventListener("click", () => {{
      document.getElementById("chunk-modal").close();
    }});
    document.getElementById("theme-toggle").addEventListener("click", () => {{
      const root = document.documentElement;
      root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    }});

    initKPIs();
    initTechDropdown();
    computeGraphLayout();
    renderGraphLegend();
    setupGraphInteractions();
    refreshAll();
  </script>
</body>
</html>
"""
