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
      padding: 0.5rem 0.85rem;
      border-radius: 9px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .btn:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
      text-decoration: none;
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
      gap: 0.75rem;
      margin-bottom: 0.9rem;
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
      height: 410px;
      border-radius: 10px;
      background: rgba(2, 6, 23, 0.35);
      border: 1px solid var(--border);
      overflow: hidden;
    }}
    [data-theme="light"] #graph-container {{
      background: #f1f5f9;
    }}
    #kg-svg {{
      width: 100%;
      height: 100%;
      cursor: grab;
    }}
    #kg-svg:active {{
      cursor: grabbing;
    }}
    .graph-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-top: 0.75rem;
      font-size: 0.76rem;
      color: var(--text-muted);
    }}
    .legend-item {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      cursor: pointer;
      padding: 0.2rem 0.5rem;
      border-radius: 6px;
      border: 1px solid var(--border);
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
      max-height: 210px;
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
      <div class="panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title">Interactive Knowledge Graph</h2>
            <div class="panel-subtitle">Click any node to filter related documents &bull; Drag nodes to rearrange</div>
          </div>
          <button class="btn" id="reset-graph-btn" type="button">Reset Filter</button>
        </div>
        <div id="graph-container">
          <svg id="kg-svg" viewBox="0 0 820 410" preserveAspectRatio="xMidYMid meet"></svg>
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
      <button class="btn" id="clear-filters" type="button">Clear</button>
    </section>

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
      docId: ""
    }};

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
        return `<span class="wc-term ${{active}}" style="font-size:${{size}}rem" data-term="${{item.term}}" title="Frequency: ${{item.count}}">${{item.term}}</span>`;
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
          <div class="tax-item ${{active}}" style="margin-left:${{indent}}px" data-path="${{cat.path}}">
            <div>
              <div style="font-weight:600">${{cat.label}}</div>
              <div class="tax-uri">${{cat.ontologic_class_uri}} &bull; ${{cat.technology_area}}</div>
            </div>
            <span class="badge">${{cat.document_ids.length}} docs</span>
          </div>
        `;
      }}).join("");
      list.querySelectorAll(".tax-item").forEach(el => {{
        el.addEventListener("click", () => {{
          const p = el.dataset.path;
          state.taxonomyPath = state.taxonomyPath === p ? "" : p;
          refreshAll();
        }});
      }});
    }}

    function renderDocuments() {{
      const grid = document.getElementById("doc-grid");
      const filtered = DB.documents.filter(doc => {{
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

      if (!filtered.length) {{
        grid.innerHTML = `<div class="panel" style="grid-column: 1 / -1; text-align:center; color: var(--text-muted);">No documents match the current filters.</div>`;
        return;
      }}

      grid.innerHTML = filtered.map(doc => {{
        const statusClass = `status-${{doc.reading_status}}`;
        const prioClass = doc.priority === "high" ? "prio-high" : "";
        const authors = doc.authors.length ? doc.authors.join(", ") : "Staff / Research Note";
        const inst = doc.institutions.length ? ` &bull; ${{doc.institutions.join(", ")}}` : "";
        const relBadges = doc.relations.map(r => `<span class="badge">${{r.relation_type}} &rarr; ${{r.target_doc_id}}</span>`).join("");
        const techChips = doc.technology_areas.slice(0, 4).map(t => `<span class="chip">${{t}}</span>`).join("");
        const conceptChips = doc.concept_ids.map(c => `<span class="chip chip-concept">${{c.replace("concept:", "")}}</span>`).join("");
        return `
          <article class="doc-card">
            <div>
              <div class="badge-row">
                <span class="badge ${{statusClass}}">${{doc.reading_status}}</span>
                <span class="badge ${{prioClass}}">priority: ${{doc.priority}}</span>
                <span class="badge">${{doc.doc_type.replace("_", " ")}}</span>
                ${{doc.published_date ? `<span class="badge">${{doc.published_date}}</span>` : ""}}
              </div>
              <h3 class="doc-title">
                ${{doc.url ? `<a href="${{doc.url}}" target="_blank" rel="noopener">${{doc.title}}</a>` : doc.title}}
              </h3>
              <div class="doc-meta">${{authors}}${{inst}}</div>
              ${{doc.notes ? `<p style="font-size:0.82rem; color: var(--text-muted); margin: 0.5rem 0 0;"><strong>Notes:</strong> ${{doc.notes}}</p>` : ""}}
            </div>
            <div>
              <div class="chip-list" style="margin-bottom:0.45rem;">${{techChips}}</div>
              <div class="chip-list" style="margin-bottom:0.65rem;">${{conceptChips}}</div>
              <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                <div class="badge-row">${{relBadges}}</div>
                <button class="btn inspect-btn" data-doc="${{doc.doc_id}}" type="button">
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
            <span>${{ch.chunk_id}} &mdash; ${{ch.heading}}</span>
            <span>${{ch.token_count}} words</span>
          </div>
          <p style="margin: 0 0 0.65rem; font-size: 0.9rem;">${{ch.text}}</p>
          <div class="chip-list" style="margin-bottom: 0.35rem;">
            ${{ch.concept_ids.map(c => `<span class="chip chip-concept">${{c}}</span>`).join("")}}
          </div>
          <div class="chip-list">
            ${{ch.taxonomy_paths.map(p => `<span class="chip">${{p}}</span>`).join("")}}
          </div>
        </div>
      `).join("");
      document.getElementById("chunk-modal").showModal();
    }}

    function renderGraph() {{
      const svg = document.getElementById("kg-svg");
      const allowedTypes = new Set(["Document", "Concept", "TaxonomyCategory", "TechnologyArea"]);
      const nodes = DB.knowledge_graph.nodes
        .filter(n => allowedTypes.has(n.node_type))
        .map((n, i, arr) => {{
          const angle = (2 * Math.PI * i) / arr.length;
          const radius = n.node_type === "Document" ? 85 : (n.node_type === "Concept" ? 145 : 175);
          return {{
            ...n,
            x: 410 + Math.cos(angle) * radius * 1.45,
            y: 205 + Math.sin(angle) * radius * 0.92
          }};
        }});
      const nodeById = Object.fromEntries(nodes.map(n => [n.node_id, n]));
      const edges = DB.knowledge_graph.edges.filter(e => nodeById[e.source] && nodeById[e.target]);

      // Simple relaxation pass for clean node separation
      for (let iter = 0; iter < 55; iter++) {{
        for (let i = 0; i < nodes.length; i++) {{
          for (let j = i + 1; j < nodes.length; j++) {{
            const dx = nodes[j].x - nodes[i].x;
            const dy = nodes[j].y - nodes[i].y;
            const dist = Math.hypot(dx, dy) || 1;
            if (dist < 68) {{
              const push = (68 - dist) * 0.16;
              const ux = (dx / dist) * push;
              const uy = (dy / dist) * push;
              nodes[j].x += ux;
              nodes[j].y += uy;
              nodes[i].x -= ux;
              nodes[i].y -= uy;
            }}
          }}
        }}
        nodes.forEach(n => {{
          n.x = Math.max(55, Math.min(765, n.x));
          n.y = Math.max(32, Math.min(378, n.y));
        }});
      }}

      function draw() {{
        const edgeMarkup = edges.map(e => {{
          const s = nodeById[e.source];
          const t = nodeById[e.target];
          return `<line x1="${{s.x}}" y1="${{s.y}}" x2="${{t.x}}" y2="${{t.y}}" stroke="rgba(148,163,184,0.26)" stroke-width="1.2" />`;
        }}).join("");

        const nodeMarkup = nodes.map(n => {{
          const color = NODE_COLORS[n.node_type] || "#38bdf8";
          const r = n.node_type === "Document" ? 11 : 8;
          const shortLabel = n.label.length > 26 ? n.label.slice(0, 24) + "…" : n.label;
          return `
            <g class="kg-node" data-id="${{n.node_id}}" data-type="${{n.node_type}}" data-label="${{n.label}}" transform="translate(${{n.x}},${{n.y}})" style="cursor:pointer">
              <circle r="${{r}}" fill="${{color}}" stroke="#0f172a" stroke-width="2"></circle>
              <text x="${{r + 5}}" y="4" fill="currentColor" font-size="10.5" font-family="var(--font-sans)">${{shortLabel}}</text>
            </g>
          `;
        }}).join("");

        svg.innerHTML = edgeMarkup + nodeMarkup;

        svg.querySelectorAll(".kg-node").forEach(g => {{
          g.addEventListener("click", () => {{
            const id = g.dataset.id;
            const type = g.dataset.type;
            const label = g.dataset.label;
            if (type === "Document") {{
              const rawDocId = id.replace("doc:", "");
              state.docId = state.docId === rawDocId ? "" : rawDocId;
            }} else if (type === "Concept") {{
              state.conceptId = state.conceptId === id ? "" : id;
            }} else if (type === "TechnologyArea") {{
              state.techArea = state.techArea === label ? "" : label;
              document.getElementById("tech-filter").value = state.techArea;
            }} else if (type === "TaxonomyCategory") {{
              const match = DB.taxonomy.find(t => t.label === label);
              if (match) {{
                state.taxonomyPath = state.taxonomyPath === match.path ? "" : match.path;
              }}
            }}
            refreshAll();
          }});
        }});
      }}

      draw();

      const legend = document.getElementById("graph-legend");
      legend.innerHTML = ["Document", "Concept", "TaxonomyCategory", "TechnologyArea"].map(t => `
        <span class="legend-item">
          <span class="legend-dot" style="background:${{NODE_COLORS[t]}}"></span>
          ${{t}}
        </span>
      `).join("");
    }}

    function refreshAll() {{
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
    document.getElementById("clear-filters").addEventListener("click", () => {{
      Object.keys(state).forEach(k => state[k] = "");
      document.getElementById("search-input").value = "";
      document.getElementById("status-filter").value = "";
      document.getElementById("priority-filter").value = "";
      document.getElementById("type-filter").value = "";
      document.getElementById("tech-filter").value = "";
      refreshAll();
    }});
    document.getElementById("reset-graph-btn").addEventListener("click", () => {{
      state.docId = "";
      state.conceptId = "";
      state.taxonomyPath = "";
      state.techArea = "";
      document.getElementById("tech-filter").value = "";
      refreshAll();
    }});
    document.getElementById("close-modal").addEventListener("click", () => {{
      document.getElementById("chunk-modal").close();
    }});
    document.getElementById("theme-toggle").addEventListener("click", () => {{
      const root = document.documentElement;
      root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    }});

    initKPIs();
    initTechDropdown();
    renderGraph();
    refreshAll();
  </script>
</body>
</html>
"""
