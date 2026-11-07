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
    """Render a self-contained, synoptic GitHub Pages HTML application (`index.html`) with hierarchical domain drill-down."""
    docs_payload = []
    for doc in documents:
        doc_chunks = [c.to_dict() for c in chunks_by_doc.get(doc.doc_id, [])]
        all_concepts = sorted({cid for c in doc_chunks for cid in c["concept_ids"]})
        all_tax = sorted({p for c in doc_chunks for p in c["taxonomy_paths"]})
        all_tech = sorted({t for c in doc_chunks for t in c["technology_areas"]})
        top_domains = sorted({p.split(" > ")[0] for p in all_tax if p})
        docs_payload.append(
            {
                **doc.to_dict(),
                "chunks": doc_chunks,
                "concept_ids": all_concepts,
                "taxonomy_paths": all_tax,
                "top_domains": top_domains,
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
  <title>Reading DB — Synoptic Knowledge Graph &amp; Domain Navigator</title>
  <meta name="description" content="Synoptic domain navigator, interactive knowledge graph, semantic chunks, word cloud, and conceptual taxonomy for technical articles and academic papers." />
  <script type="application/ld+json">
{jsonld_str}
  </script>
  <style>
    :root {{
      --bg: #0b0f19;
      --bg-elevated: rgba(19, 27, 46, 0.82);
      --bg-card: rgba(23, 33, 56, 0.88);
      --bg-chip: rgba(56, 189, 248, 0.12);
      --border: rgba(148, 163, 184, 0.18);
      --border-strong: rgba(56, 189, 248, 0.48);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-2: #a855f7;
      --accent-3: #10b981;
      --accent-warn: #f59e0b;
      --accent-danger: #f43f5e;
      --shadow: 0 16px 36px -14px rgba(2, 6, 23, 0.75);
      --radius: 13px;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
    }}
    [data-theme="light"] {{
      --bg: #f8fafc;
      --bg-elevated: rgba(255, 255, 255, 0.92);
      --bg-card: #ffffff;
      --bg-chip: rgba(2, 132, 199, 0.1);
      --border: rgba(15, 23, 42, 0.12);
      --border-strong: rgba(2, 132, 199, 0.5);
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #0284c7;
      --accent-2: #7c3aed;
      --accent-3: #059669;
      --shadow: 0 10px 26px -10px rgba(15, 23, 42, 0.1);
    }}
    [data-theme="tron"] {{
      --bg: #020813;
      --bg-elevated: rgba(3, 14, 30, 0.9);
      --bg-card: rgba(4, 18, 38, 0.92);
      --bg-chip: rgba(0, 240, 255, 0.14);
      --border: rgba(0, 240, 255, 0.34);
      --border-strong: #00f0ff;
      --text: #e2fbff;
      --text-muted: #5ec2e8;
      --accent: #00f0ff;
      --accent-2: #0088ff;
      --accent-3: #00ffaa;
      --accent-warn: #ff9e00;
      --accent-danger: #ff2a6d;
      --shadow: 0 0 22px rgba(0, 240, 255, 0.18), inset 0 0 14px rgba(0, 240, 255, 0.07);
    }}
    * {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background:
        radial-gradient(circle at 12% 10%, rgba(56, 189, 248, 0.11), transparent 35%),
        radial-gradient(circle at 88% 12%, rgba(168, 85, 247, 0.11), transparent 38%),
        var(--bg);
      color: var(--text);
      line-height: 1.5;
      min-height: 100vh;
    }}
    [data-theme="tron"] body {{
      background-color: #020813;
      background-image:
        radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.22), transparent 55%),
        radial-gradient(circle at 85% 20%, rgba(0, 136, 255, 0.18), transparent 45%),
        linear-gradient(rgba(0, 240, 255, 0.075) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.075) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px;
      background-attachment: fixed;
    }}
    [data-theme="tron"] header.hero,
    [data-theme="tron"] .panel,
    [data-theme="tron"] .navigator-panel,
    [data-theme="tron"] .kpi-card,
    [data-theme="tron"] .filter-bar,
    [data-theme="tron"] .synoptic-table-wrap,
    [data-theme="tron"] .doc-card {{
      border-color: rgba(0, 240, 255, 0.38);
      box-shadow: 0 0 18px rgba(0, 240, 255, 0.14), inset 0 0 12px rgba(0, 240, 255, 0.05);
    }}
    [data-theme="tron"] h1,
    [data-theme="tron"] .kpi-value,
    [data-theme="tron"] .brand-eyebrow {{
      text-shadow: 0 0 10px rgba(0, 240, 255, 0.55);
    }}
    [data-theme="tron"] #kg-svg .kg-node circle {{
      filter: drop-shadow(0 0 6px rgba(0, 240, 255, 0.75));
    }}
    a {{
      color: var(--accent);
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    .shell {{
      max-width: 1420px;
      margin: 0 auto;
      padding: 1.25rem 1.4rem 3rem;
    }}
    header.hero {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 1.1rem 1.4rem;
      border-radius: var(--radius);
      background: var(--bg-elevated);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 1rem;
    }}
    .brand-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      background: var(--bg-chip);
      padding: 0.2rem 0.6rem;
      border-radius: 999px;
      border: 1px solid var(--border-strong);
      margin-bottom: 0.35rem;
    }}
    h1 {{
      margin: 0 0 0.2rem;
      font-size: clamp(1.35rem, 2.1vw, 1.8rem);
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      margin: 0;
      color: var(--text-muted);
      max-width: 740px;
      font-size: 0.88rem;
    }}
    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      align-items: center;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.42rem 0.75rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      cursor: pointer;
      transition: all 0.14s ease;
      user-select: none;
    }}
    .btn:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
      text-decoration: none;
    }}
    .btn.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
      color: var(--accent);
    }}
    .btn-sm {{
      padding: 0.26rem 0.58rem;
      font-size: 0.73rem;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border: none;
    }}
    .theme-group {{
      display: inline-flex;
      align-items: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 0.18rem;
      gap: 0.2rem;
    }}
    .theme-opt {{
      font-size: 0.72rem;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 0.28rem 0.55rem;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.14s ease;
    }}
    .theme-opt:hover {{
      color: var(--accent);
    }}
    .theme-opt.active {{
      background: var(--bg-card);
      color: var(--accent);
      border-color: var(--border-strong);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }}
    .theme-opt[data-set-theme="tron"].active {{
      color: #00f0ff;
      border-color: #00f0ff;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.45);
      text-shadow: 0 0 8px rgba(0, 240, 255, 0.75);
    }}
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(195px, 1fr));
      gap: 0.75rem;
      margin-bottom: 0.85rem;
    }}
    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 0.75rem 0.95rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.48rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }}
    .kpi-card:hover, .kpi-card.active {{
      border-color: var(--border-strong);
      transform: translateY(-2px);
    }}
    .kpi-card.active {{
      background: var(--bg-chip);
      box-shadow: inset 0 0 0 1px var(--accent), var(--shadow);
    }}
    .kpi-top {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 0.5rem;
    }}
    .kpi-value {{
      font-size: 1.4rem;
      font-weight: 800;
      font-family: var(--font-mono);
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .kpi-label {{
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 700;
    }}
    .kpi-section-link {{
      font-size: 0.68rem;
      font-family: var(--font-mono);
      color: var(--accent);
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }}
    .kpi-doc-links {{
      display: flex;
      flex-direction: column;
      gap: 0.22rem;
      border-top: 1px solid var(--border);
      padding-top: 0.42rem;
    }}
    .kpi-doc-link {{
      font-size: 0.7rem;
      font-family: var(--font-mono);
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      padding: 0.1rem 0.3rem;
      border-radius: 4px;
      transition: all 0.12s ease;
    }}
    .kpi-doc-link:hover {{
      background: var(--bg-chip);
      color: var(--accent);
      text-decoration: none;
    }}
    .kpi-drawer {{
      background: var(--bg-card);
      border: 1px solid var(--border-strong);
      border-radius: var(--radius);
      padding: 0.95rem 1.15rem;
      box-shadow: var(--shadow);
      margin-bottom: 1rem;
    }}
    .kpi-drawer[hidden] {{
      display: none !important;
    }}
    .kpi-drawer-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 0.55rem;
      max-height: 270px;
      overflow-y: auto;
      margin-top: 0.65rem;
      padding-right: 0.25rem;
    }}
    .kpi-drawer-item {{
      display: flex;
      flex-direction: column;
      gap: 0.22rem;
      padding: 0.5rem 0.7rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: rgba(2, 6, 23, 0.22);
      font-size: 0.77rem;
    }}
    [data-theme="light"] .kpi-drawer-item {{
      background: #f8fafc;
    }}
    .kpi-drawer-item:hover {{
      border-color: var(--accent);
    }}

    /* Synoptic Domain & Slice Navigator */
    .navigator-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1rem 1.15rem;
      box-shadow: var(--shadow);
      margin-bottom: 1.1rem;
    }}
    .nav-top-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 0.85rem;
    }}
    .slice-tabs {{
      display: inline-flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      background: var(--bg);
      padding: 0.25rem;
      border-radius: 9px;
      border: 1px solid var(--border);
    }}
    .slice-tab {{
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.32rem 0.68rem;
      border-radius: 6px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.14s ease;
    }}
    .slice-tab.active {{
      background: var(--bg-card);
      color: var(--accent);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    }}
    .breadcrumb-bar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.8rem;
      font-family: var(--font-mono);
      padding: 0.45rem 0.75rem;
      border-radius: 8px;
      background: rgba(2, 6, 23, 0.28);
      border: 1px solid var(--border);
      margin-bottom: 0.85rem;
    }}
    [data-theme="light"] .breadcrumb-bar {{
      background: #f1f5f9;
    }}
    .crumb {{
      cursor: pointer;
      color: var(--accent);
      padding: 0.1rem 0.35rem;
      border-radius: 5px;
    }}
    .crumb:hover {{
      background: var(--bg-chip);
    }}
    .crumb.current {{
      color: var(--text);
      font-weight: 700;
    }}
    .crumb-sep {{
      color: var(--text-muted);
    }}
    .domain-cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 0.75rem;
    }}
    .domain-card {{
      background: rgba(2, 6, 23, 0.25);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.8rem 0.95rem;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.55rem;
    }}
    [data-theme="light"] .domain-card {{
      background: #f8fafc;
    }}
    .domain-card:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
    }}
    .domain-card.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
      box-shadow: inset 0 0 0 1px var(--accent);
    }}
    .domain-card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 0.5rem;
    }}
    .domain-card-title {{
      font-size: 0.88rem;
      font-weight: 700;
      margin: 0;
    }}
    .domain-card-count {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 700;
      padding: 0.12rem 0.45rem;
      border-radius: 999px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--accent);
      white-space: nowrap;
    }}
    .domain-sub-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
    }}
    .sub-pill {{
      font-size: 0.68rem;
      font-family: var(--font-mono);
      padding: 0.12rem 0.42rem;
      border-radius: 5px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-muted);
      cursor: pointer;
    }}
    .sub-pill:hover, .sub-pill.active {{
      border-color: var(--accent-2);
      color: var(--accent-2);
    }}

    /* Main 2-column synoptic visual area */
    .dashboard-grid {{
      display: grid;
      grid-template-columns: 1.35fr 1fr;
      gap: 1.1rem;
      margin-bottom: 1.1rem;
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
      padding: 1.05rem 1.15rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
    }}
    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.6rem;
      margin-bottom: 0.7rem;
    }}
    .panel-title {{
      margin: 0;
      font-size: 0.98rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }}
    .panel-subtitle {{
      font-size: 0.76rem;
      color: var(--text-muted);
    }}
    #graph-container {{
      position: relative;
      width: 100%;
      height: 360px;
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
      top: 0.55rem;
      right: 0.55rem;
      display: flex;
      gap: 0.3rem;
      z-index: 4;
    }}
    .graph-status-banner {{
      position: absolute;
      left: 0.55rem;
      bottom: 0.55rem;
      right: 0.55rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      padding: 0.4rem 0.7rem;
      border-radius: 8px;
      background: var(--bg-elevated);
      backdrop-filter: blur(10px);
      border: 1px solid var(--border-strong);
      font-size: 0.75rem;
      z-index: 4;
      pointer-events: auto;
    }}
    .graph-status-banner[hidden] {{
      display: none !important;
    }}
    .graph-legend {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-top: 0.65rem;
      font-size: 0.74rem;
      color: var(--text-muted);
    }}
    .legend-item {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      cursor: pointer;
      padding: 0.2rem 0.55rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: var(--bg-elevated);
      color: var(--text);
      user-select: none;
      transition: all 0.14s ease;
    }}
    .legend-item:hover {{
      border-color: var(--accent);
    }}
    .legend-item.muted {{
      opacity: 0.38;
      text-decoration: line-through;
    }}
    .legend-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}
    .word-cloud-box {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 0.38rem 0.55rem;
      padding: 0.75rem;
      border-radius: 10px;
      background: rgba(2, 6, 23, 0.25);
      border: 1px solid var(--border);
      min-height: 145px;
      margin-bottom: 0.75rem;
    }}
    [data-theme="light"] .word-cloud-box {{
      background: #f8fafc;
    }}
    .wc-term {{
      cursor: pointer;
      font-family: var(--font-mono);
      padding: 0.12rem 0.4rem;
      border-radius: 6px;
      transition: all 0.14s ease;
      border: 1px solid transparent;
      user-select: none;
    }}
    .wc-term:hover, .wc-term.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
      transform: scale(1.05);
    }}
    .taxonomy-list {{
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      max-height: 185px;
      overflow-y: auto;
      padding-right: 0.2rem;
    }}
    .tax-item {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      padding: 0.38rem 0.6rem;
      border-radius: 7px;
      border: 1px solid var(--border);
      font-size: 0.76rem;
      cursor: pointer;
      transition: border-color 0.14s ease;
      user-select: none;
    }}
    .tax-item:hover, .tax-item.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
    }}
    .tax-uri {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      color: var(--accent-2);
    }}

    /* Compact Filter & Synoptic Document Section */
    .filter-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.55rem;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid var(--border);
      padding: 0.75rem 1rem;
      border-radius: var(--radius);
      margin-bottom: 0.85rem;
      box-shadow: var(--shadow);
    }}
    .filter-bar input, .filter-bar select {{
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 0.42rem 0.68rem;
      border-radius: 7px;
      font-size: 0.8rem;
      font-family: var(--font-sans);
    }}
    .filter-bar input {{
      flex: 1;
      min-width: 200px;
    }}
    .active-filters-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.4rem;
      align-items: center;
      margin-bottom: 0.85rem;
    }}
    .active-filters-row[hidden] {{
      display: none !important;
    }}
    .filter-pill {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      padding: 0.2rem 0.58rem;
      border-radius: 999px;
      background: var(--bg-chip);
      border: 1px solid var(--border-strong);
      color: var(--accent);
      cursor: pointer;
    }}

    /* Synoptic Table View (Default to prevent page sprawl) */
    .synoptic-table-wrap {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow-x: auto;
    }}
    table.synoptic-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }}
    table.synoptic-table th, table.synoptic-table td {{
      padding: 0.68rem 0.85rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }}
    table.synoptic-table th {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      background: rgba(2, 6, 23, 0.22);
    }}
    table.synoptic-table tr:last-child td {{
      border-bottom: none;
    }}
    table.synoptic-table tbody tr:hover {{
      background: rgba(56, 189, 248, 0.05);
    }}
    .pagination-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0.65rem 1rem;
      border-top: 1px solid var(--border);
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    .doc-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 0.95rem;
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
      padding: 1rem 1.1rem;
      box-shadow: var(--shadow);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.7rem;
      transition: transform 0.14s ease, border-color 0.14s ease;
    }}
    .doc-card:hover {{
      transform: translateY(-2px);
      border-color: var(--border-strong);
    }}
    .badge-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      align-items: center;
    }}
    .badge {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 600;
      padding: 0.14rem 0.45rem;
      border-radius: 5px;
      border: 1px solid var(--border);
      text-transform: uppercase;
      white-space: nowrap;
    }}
    .status-read {{ color: var(--accent-3); border-color: rgba(16, 185, 129, 0.4); }}
    .status-reading {{ color: var(--accent); border-color: rgba(56, 189, 248, 0.4); }}
    .status-to-read {{ color: var(--accent-warn); border-color: rgba(245, 158, 11, 0.4); }}
    .prio-high {{ color: var(--accent-danger); border-color: rgba(244, 63, 94, 0.4); }}
    .doc-title {{
      margin: 0.2rem 0;
      font-size: 0.96rem;
      font-weight: 700;
      line-height: 1.35;
    }}
    .doc-meta {{
      font-size: 0.76rem;
      color: var(--text-muted);
    }}
    .chip-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.3rem;
    }}
    .chip {{
      font-size: 0.68rem;
      font-family: var(--font-mono);
      padding: 0.13rem 0.42rem;
      border-radius: 5px;
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
      padding: 1rem 1.3rem;
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
      padding: 1.15rem 1.3rem;
      overflow-y: auto;
      max-height: calc(86vh - 80px);
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
    }}
    .chunk-box {{
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.9rem 1.05rem;
      background: rgba(2, 6, 23, 0.22);
    }}
    .chunk-head {{
      display: flex;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent);
      margin-bottom: 0.4rem;
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <div>
        <div class="brand-eyebrow">OntoLogic-Ready Knowledge Base &bull; reading-db</div>
        <h1>Synoptic Knowledge Graph &amp; Domain Navigator</h1>
        <p class="subtitle">
          Top-level domain selector with hierarchical drill-downs into subdomains, technology slices, scoped knowledge graphs, and semantic chunks.
        </p>
      </div>
      <div class="hero-actions">
        <a class="btn" href="knowledge_graph.json" target="_blank" rel="noopener" title="Raw OntoLogic JSON-LD Property Graph">JSON-LD</a>
        <a class="btn" href="taxonomy.html" id="hero-taxonomy-btn" title="Rendered Conceptual Taxonomy Markdown &amp; Raw JSON">Taxonomy</a>
        <a class="btn" href="chunks.html" id="hero-chunks-btn" title="Rendered Semantic Chunks Markdown &amp; Raw JSON">Chunks</a>
        <a class="btn" href="summary.html" id="hero-summary-btn" title="Rendered Executive Summary Markdown &amp; Raw MD">Summary MD</a>
        <div class="theme-group" role="group" aria-label="Theme Selector">
          <button class="theme-opt active" type="button" data-set-theme="dark" title="Midnight Dark Theme">Dark</button>
          <button class="theme-opt" type="button" data-set-theme="tron" title="Neon-Blue TRON Cyber Grid Theme">&#x26A1; TRON</button>
          <button class="theme-opt" type="button" data-set-theme="light" title="Daylight Theme">Light</button>
        </div>
        <button class="btn btn-primary" id="theme-toggle" type="button" title="Cycle Theme (Dark / TRON / Light)">Theme</button>
      </div>
    </header>

    <section class="kpi-grid" id="kpi-grid"></section>
    <section class="kpi-drawer" id="kpi-linked-drawer" hidden></section>

    <!-- Synoptic Top-Level Domain & Slice Selector with Breadcrumb Drill-Down -->
    <section class="navigator-panel">
      <div class="nav-top-bar">
        <div>
          <h2 class="panel-title">Top-Level Domain &amp; Slice Navigator</h2>
          <div class="panel-subtitle">Select a top-level division and drill down into subcategories to scope the graph, word cloud, and document list</div>
        </div>
        <div class="slice-tabs" id="slice-dimension-tabs">
          <button type="button" class="slice-tab active" data-dim="domain">By Domain Hierarchy</button>
          <button type="button" class="slice-tab" data-dim="tech">By Technology Area</button>
          <button type="button" class="slice-tab" data-dim="workflow">By Reading Stage</button>
          <button type="button" class="slice-tab" data-dim="doctype">By Document Type</button>
        </div>
      </div>

      <div class="breadcrumb-bar" id="breadcrumb-bar"></div>
      <div class="domain-cards-grid" id="domain-cards-grid"></div>
    </section>

    <section class="dashboard-grid">
      <div class="panel" id="graph-panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title">Scoped Knowledge Graph <span class="badge" id="graph-scope-badge">All Domains</span></h2>
            <div class="panel-subtitle">Click any node to filter &bull; Drag nodes to rearrange &bull; Scoped to active domain/slice</div>
          </div>
          <div style="display:flex; gap:0.35rem; flex-wrap:wrap;">
            <button class="btn btn-sm" id="fullscreen-graph-btn" type="button" title="Toggle Full Web-Page View">&#x26F6; Full Page</button>
            <button class="btn btn-sm" id="relayout-graph-btn" type="button">Re-Layout</button>
            <button class="btn btn-sm" id="reset-graph-btn" type="button">Reset Scope</button>
          </div>
        </div>
        <div id="graph-container">
          <div class="graph-toolbar">
            <button class="btn btn-sm" id="zoom-in-btn" type="button" title="Zoom In">+</button>
            <button class="btn btn-sm" id="zoom-out-btn" type="button" title="Zoom Out">&minus;</button>
            <button class="btn btn-sm" id="zoom-fit-btn" type="button" title="Reset View">Fit</button>
            <button class="btn btn-sm" id="toolbar-fullscreen-btn" type="button" title="Toggle Full Web-Page View">&#x26F6;</button>
          </div>
          <svg id="kg-svg" viewBox="0 0 820 360" preserveAspectRatio="xMidYMid meet"></svg>
          <div class="graph-status-banner" id="graph-status-banner" hidden>
            <span id="graph-status-text"></span>
            <button class="btn btn-sm" id="graph-status-clear" type="button">&times; Clear</button>
          </div>
        </div>
        <div class="graph-legend" id="graph-legend"></div>
      </div>

      <div class="panel" id="word-cloud-panel">
        <div class="panel-header">
          <div>
            <h2 class="panel-title">Scoped Word Cloud &amp; Sub-Hierarchy</h2>
            <div class="panel-subtitle">Dynamically recomputed for the active domain/slice</div>
          </div>
        </div>
        <div class="word-cloud-box" id="word-cloud"></div>
        <div class="panel-subtitle" style="margin-bottom: 0.35rem; font-weight: 600;">Subcategory Drill-Down (OntoLogic Classes)</div>
        <div class="taxonomy-list" id="taxonomy-list"></div>
      </div>
    </section>

    <section class="filter-bar">
      <input type="search" id="search-input" placeholder="Search within current slice (title, abstract chunks, concepts, authors)..." />
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
        <option value="">All Types</option>
        <option value="academic_paper">Academic Papers</option>
        <option value="technical_article">Technical Articles</option>
        <option value="technical_paper">Technical Papers</option>
        <option value="note">Research Notes</option>
      </select>
      <select id="tech-filter">
        <option value="">All Tech Areas</option>
      </select>
      <div style="display:inline-flex; gap:0.3rem;">
        <button class="btn btn-sm active" id="view-table-btn" type="button" title="Compact Synoptic Table">Table View</button>
        <button class="btn btn-sm" id="view-cards-btn" type="button" title="Detailed Cards">Card View</button>
      </div>
      <button class="btn btn-sm" id="clear-filters" type="button">Reset All</button>
    </section>

    <div class="active-filters-row" id="active-filters-row" hidden></div>

    <section id="doc-results-container"></section>
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
      sliceDimension: "domain", // "domain" | "tech" | "workflow" | "doctype"
      query: "",
      status: "",
      priority: "",
      docType: "",
      techArea: "",
      taxonomyPath: "", // hierarchical prefix or exact path, e.g. "Hardware & Semiconductor Systems" or "Hardware & Semiconductor Systems > EDA & Hardware Verification"
      conceptId: "",
      docId: "",
      selectedGraphNodeId: "",
      hiddenNodeTypes: new Set(),
      viewMode: "table", // "table" (synoptic default) | "cards"
      activeKpiDrawer: "", // "" | "docs" | "chunks" | "concepts" | "taxonomy" | "nodes" | "edges"
      page: 1,
      pageSize: 8
    }};

    let graphNodes = [];
    let graphEdges = [];
    let viewBox = {{ x: 0, y: 0, w: 820, h: 360 }};

    function escapeHtml(str) {{
      return String(str ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function docMatchesTaxonomyPrefix(doc, prefix) {{
      if (!prefix) return true;
      return doc.taxonomy_paths.some(p => p === prefix || p.startsWith(prefix + " > "));
    }}

    function getFilteredDocuments() {{
      return DB.documents.filter(doc => {{
        if (state.docId && doc.doc_id !== state.docId) return false;
        if (state.status && doc.reading_status !== state.status) return false;
        if (state.priority && doc.priority !== state.priority) return false;
        if (state.docType && doc.doc_type !== state.docType) return false;
        if (state.techArea && !doc.technology_areas.includes(state.techArea)) return false;
        if (state.taxonomyPath && !docMatchesTaxonomyPrefix(doc, state.taxonomyPath)) return false;
        if (state.conceptId && !doc.concept_ids.includes(state.conceptId)) return false;
        if (state.query) {{
          const q = state.query.toLowerCase();
          const hay = `${{doc.title}} ${{doc.content}} ${{doc.authors.join(" ")}} ${{doc.tags.join(" ")}} ${{doc.notes}}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }}
        return true;
      }});
    }}

    function focusDocumentInSection(docId, sectionId, openModal = false) {{
      if (docId) {{
        const idx = DB.documents.findIndex(d => d.doc_id === docId);
        if (idx >= 0) {{
          state.docId = docId;
          state.selectedGraphNodeId = `doc:${{docId}}`;
          state.page = 1;
          refreshAll();
        }}
      }}
      if (openModal && docId) {{
        openChunkModal(docId);
      }}
      const targetEl = document.getElementById(sectionId || "doc-results-container");
      if (targetEl) {{
        targetEl.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }}
    }}

    function renderKPIs(filteredDocs) {{
      const kpiGrid = document.getElementById("kpi-grid");
      const totalChunks = filteredDocs.reduce((acc, d) => acc + d.chunks.length, 0);
      const activeConcepts = new Set();
      filteredDocs.forEach(d => d.concept_ids.forEach(c => activeConcepts.add(c)));
      const activeTax = new Set();
      filteredDocs.forEach(d => d.taxonomy_paths.forEach(p => activeTax.add(p)));

      const isScoped = filteredDocs.length !== DB.documents.length;
      const suffix = isScoped ? ` / ${{DB.documents.length}}` : "";

      const chunkSortedDocs = [...filteredDocs].sort((a, b) => b.chunks.length - a.chunks.length);
      const conceptDocs = filteredDocs.filter(d => d.concept_ids.length > 0);
      const taxDocs = filteredDocs.filter(d => d.taxonomy_paths.length > 0);
      const edgeConnectedDocs = filteredDocs.filter(d => (d.relations && d.relations.length > 0));
      const fallbackEdgeDocs = edgeConnectedDocs.length ? edgeConnectedDocs : filteredDocs;

      const kpis = [
        {{
          key: "docs",
          label: "Scoped Documents",
          value: `${{filteredDocs.length}}${{suffix}}`,
          sectionId: "doc-results-container",
          sectionLabel: "Document Catalog ↓",
          pageHref: "summary.html",
          docs: filteredDocs.slice(0, 3),
          openChunksOnDocClick: false
        }},
        {{
          key: "chunks",
          label: "Semantic Chunks",
          value: totalChunks,
          sectionId: "doc-results-container",
          sectionLabel: "Chunks MD ↗",
          pageHref: "chunks.html",
          docs: chunkSortedDocs.slice(0, 3),
          openChunksOnDocClick: true
        }},
        {{
          key: "concepts",
          label: "Active Concepts",
          value: activeConcepts.size,
          sectionId: "word-cloud-panel",
          sectionLabel: "Word Cloud & Concepts ↓",
          pageHref: "taxonomy.html",
          docs: (conceptDocs.length ? conceptDocs : filteredDocs).slice(0, 3),
          openChunksOnDocClick: false
        }},
        {{
          key: "taxonomy",
          label: "Taxonomy Nodes",
          value: activeTax.size,
          sectionId: "taxonomy-list",
          sectionLabel: "Taxonomy MD ↗",
          pageHref: "taxonomy.html",
          docs: (taxDocs.length ? taxDocs : filteredDocs).slice(0, 3),
          openChunksOnDocClick: false
        }},
        {{
          key: "nodes",
          label: "Total Graph Nodes",
          value: DB.knowledge_graph.summary.node_count,
          sectionId: "graph-panel",
          sectionLabel: "Knowledge Graph ↓",
          pageHref: "knowledge_graph.json",
          docs: filteredDocs.slice(0, 3),
          openChunksOnDocClick: false
        }},
        {{
          key: "edges",
          label: "Total Graph Edges",
          value: DB.knowledge_graph.summary.edge_count,
          sectionId: "graph-panel",
          sectionLabel: "Graph Edges ↓",
          pageHref: "summary.html",
          docs: fallbackEdgeDocs.slice(0, 3),
          openChunksOnDocClick: false
        }}
      ];

      kpiGrid.innerHTML = kpis.map(k => {{
        const isActive = state.activeKpiDrawer === k.key ? "active" : "";
        const docLinksHtml = k.docs.map(d => {{
          const shortTitle = d.title.length > 28 ? d.title.slice(0, 26) + "…" : d.title;
          return `<a href="#${{k.sectionId}}" class="kpi-doc-link" data-doc-id="${{escapeHtml(d.doc_id)}}" data-sec="${{k.sectionId}}" data-open-chunks="${{k.openChunksOnDocClick ? "1" : "0"}}" title="${{escapeHtml(d.title)}} (${{escapeHtml(d.doc_id)}})">&rarr; ${{escapeHtml(d.doc_id)}}: ${{escapeHtml(shortTitle)}}</a>`;
        }}).join("");
        const moreCount = Math.max(0, filteredDocs.length - k.docs.length);
        return `
          <div class="kpi-card ${{isActive}}" data-kpi-key="${{k.key}}" data-sec="${{k.sectionId}}">
            <div>
              <div class="kpi-top">
                <div class="kpi-label">${{k.label}}</div>
                <div class="kpi-value">${{k.value}}</div>
              </div>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.15rem;">
                <a href="#${{k.sectionId}}" class="kpi-section-link kpi-sec-jump" data-sec="${{k.sectionId}}">${{k.sectionLabel}}</a>
                <a href="${{k.pageHref}}" class="kpi-section-link" style="color:var(--accent-2);" onclick="event.stopPropagation()">Page &nearr;</a>
              </div>
            </div>
            <div class="kpi-doc-links">
              ${{docLinksHtml || `<span class="kpi-doc-link">No matching docs</span>`}}
              <span class="kpi-section-link" style="margin-top:0.1rem;">${{state.activeKpiDrawer === k.key ? "Hide linked list &▴;" : `Browse all (${{moreCount > 0 ? `+${{moreCount}} more` : filteredDocs.length}}) &▾;`}}</span>
            </div>
          </div>
        `;
      }}).join("");

      kpiGrid.querySelectorAll(".kpi-doc-link[data-doc-id]").forEach(link => {{
        link.addEventListener("click", e => {{
          e.preventDefault();
          e.stopPropagation();
          const docId = link.dataset.docId;
          const secId = link.dataset.sec;
          const openChunks = link.dataset.openChunks === "1";
          focusDocumentInSection(docId, secId, openChunks);
        }});
      }});

      kpiGrid.querySelectorAll(".kpi-sec-jump").forEach(jump => {{
        jump.addEventListener("click", e => {{
          e.preventDefault();
          e.stopPropagation();
          const secEl = document.getElementById(jump.dataset.sec);
          if (secEl) secEl.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }});
      }});

      kpiGrid.querySelectorAll(".kpi-card").forEach(card => {{
        card.addEventListener("click", () => {{
          const kKey = card.dataset.kpiKey;
          state.activeKpiDrawer = state.activeKpiDrawer === kKey ? "" : kKey;
          renderKPIs(filteredDocs);
          renderKpiDrawer(filteredDocs);
        }});
      }});

      renderKpiDrawer(filteredDocs);
    }}

    function renderKpiDrawer(filteredDocs) {{
      const drawer = document.getElementById("kpi-linked-drawer");
      if (!drawer) return;
      if (!state.activeKpiDrawer) {{
        drawer.hidden = true;
        drawer.innerHTML = "";
        return;
      }}
      drawer.hidden = false;
      const kKey = state.activeKpiDrawer;
      let headerTitle = "";
      let sectionId = "doc-results-container";
      let pageUrl = "summary.html";
      let pageLabel = "Open Rendered Summary MD";
      let itemsHtml = "";

      if (kKey === "docs") {{
        headerTitle = `Scoped Documents (${{filteredDocs.length}} Linked Documents)`;
        sectionId = "doc-results-container";
        pageUrl = "summary.html";
        pageLabel = "Open Summary MD Page";
        itemsHtml = filteredDocs.slice(0, 48).map(d => `
          <div class="kpi-drawer-item">
            <div style="display:flex; justify-content:space-between; gap:0.4rem;">
              <a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="doc-results-container" style="font-weight:700;">${{escapeHtml(d.title)}}</a>
              <span class="badge status-${{escapeHtml(d.reading_status)}}">${{escapeHtml(d.reading_status)}}</span>
            </div>
            <div class="doc-meta">${{escapeHtml(d.doc_id)}} &bull; ${{escapeHtml(d.doc_type.replace("_", " "))}} &bull; <a href="#graph-panel" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="graph-panel">View in Graph &rarr;</a></div>
          </div>
        `).join("");
      }} else if (kKey === "chunks") {{
        const totalChunks = filteredDocs.reduce((acc, d) => acc + d.chunks.length, 0);
        headerTitle = `Semantic Chunks (${{totalChunks}} Chunks across ${{filteredDocs.length}} Documents)`;
        sectionId = "doc-results-container";
        pageUrl = "chunks.html";
        pageLabel = "Open Rendered Chunks MD Page";
        itemsHtml = filteredDocs.slice(0, 48).map(d => `
          <div class="kpi-drawer-item">
            <div style="display:flex; justify-content:space-between; gap:0.4rem;">
              <a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="doc-results-container" data-chunks="1" style="font-weight:700;">${{escapeHtml(d.title)}}</a>
              <span class="badge">${{d.chunks.length}} chunks</span>
            </div>
            <div class="doc-meta">
              ${{d.chunks.slice(0, 3).map(c => `<a href="chunks.html" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="doc-results-container" data-chunks="1" style="margin-right:0.4rem;">[${{escapeHtml(c.heading)}}]</a>`).join("")}}
            </div>
          </div>
        `).join("");
      }} else if (kKey === "concepts") {{
        const conceptMap = new Map();
        filteredDocs.forEach(d => {{
          d.concept_ids.forEach(cid => {{
            if (!conceptMap.has(cid)) conceptMap.set(cid, []);
            conceptMap.get(cid).push(d);
          }});
        }});
        headerTitle = `Active Concepts (${{conceptMap.size}} Concepts with Linked Documents)`;
        sectionId = "word-cloud-panel";
        pageUrl = "taxonomy.html";
        pageLabel = "Open Taxonomy & Concepts MD Page";
        itemsHtml = [...conceptMap.entries()].map(([cid, docs]) => `
          <div class="kpi-drawer-item">
            <div style="display:flex; justify-content:space-between; gap:0.4rem;">
              <a href="#word-cloud-panel" class="kpi-drawer-concept-jump" data-concept="${{escapeHtml(cid)}}" style="font-weight:700;">${{escapeHtml(cid.replace("concept:", ""))}}</a>
              <span class="badge">${{docs.length}} linked docs</span>
            </div>
            <div class="doc-meta">
              ${{docs.slice(0, 4).map(d => `<a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="doc-results-container" style="margin-right:0.45rem;">&rarr; ${{escapeHtml(d.doc_id)}}</a>`).join("")}}
            </div>
          </div>
        `).join("");
      }} else if (kKey === "taxonomy") {{
        const taxMap = new Map();
        filteredDocs.forEach(d => {{
          d.taxonomy_paths.forEach(tp => {{
            if (!taxMap.has(tp)) taxMap.set(tp, []);
            taxMap.get(tp).push(d);
          }});
        }});
        headerTitle = `Taxonomy Nodes (${{taxMap.size}} Categories with Linked Documents)`;
        sectionId = "taxonomy-list";
        pageUrl = "taxonomy.html";
        pageLabel = "Open Rendered Taxonomy MD Page";
        itemsHtml = [...taxMap.entries()].map(([tp, docs]) => `
          <div class="kpi-drawer-item">
            <div style="display:flex; justify-content:space-between; gap:0.4rem;">
              <a href="#taxonomy-list" class="kpi-drawer-tax-jump" data-tax="${{escapeHtml(tp)}}" style="font-weight:700;">${{escapeHtml(tp)}}</a>
              <span class="badge">${{docs.length}} linked docs</span>
            </div>
            <div class="doc-meta">
              ${{docs.slice(0, 4).map(d => `<a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="doc-results-container" style="margin-right:0.45rem;">&rarr; ${{escapeHtml(d.doc_id)}}</a>`).join("")}}
            </div>
          </div>
        `).join("");
      }} else if (kKey === "nodes") {{
        headerTitle = `Total Graph Nodes (${{DB.knowledge_graph.summary.node_count}} Nodes Linked to Documents)`;
        sectionId = "graph-panel";
        pageUrl = "knowledge_graph.json";
        pageLabel = "Open Raw JSON-LD Graph";
        itemsHtml = filteredDocs.slice(0, 48).map(d => `
          <div class="kpi-drawer-item">
            <div style="display:flex; justify-content:space-between; gap:0.4rem;">
              <a href="#graph-panel" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(d.doc_id)}}" data-sec="graph-panel" style="font-weight:700;">doc:${{escapeHtml(d.doc_id)}}</a>
              <span class="badge">${{d.concept_ids.length}} concepts &bull; ${{d.taxonomy_paths.length}} classes</span>
            </div>
            <div class="doc-meta">${{escapeHtml(d.title)}}</div>
          </div>
        `).join("");
      }} else if (kKey === "edges") {{
        const docEdges = DB.knowledge_graph.edges.filter(e => e.source.startsWith("doc:") || e.target.startsWith("doc:"));
        headerTitle = `Total Graph Edges (${{DB.knowledge_graph.summary.edge_count}} Typed Edges Across Knowledge Graph)`;
        sectionId = "graph-panel";
        pageUrl = "summary.html";
        pageLabel = "Open Summary & Graph MD Page";
        itemsHtml = docEdges.slice(0, 48).map(e => {{
          const srcDoc = e.source.startsWith("doc:") ? e.source.replace("doc:", "") : "";
          const tgtDoc = e.target.startsWith("doc:") ? e.target.replace("doc:", "") : "";
          const primaryDoc = srcDoc || tgtDoc;
          return `
            <div class="kpi-drawer-item">
              <div style="display:flex; justify-content:space-between; gap:0.4rem;">
                <a href="#graph-panel" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(primaryDoc)}}" data-sec="graph-panel" style="font-weight:700;">${{escapeHtml(e.source)}} &mdash;[${{escapeHtml(e.predicate)}}]&rarr; ${{escapeHtml(e.target)}}</a>
              </div>
              <div class="doc-meta">
                ${{srcDoc ? `<a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(srcDoc)}}" data-sec="doc-results-container">Source: ${{escapeHtml(srcDoc)}}</a>` : ""}}
                ${{tgtDoc ? ` &bull; <a href="#doc-results-container" class="kpi-drawer-doc-jump" data-doc="${{escapeHtml(tgtDoc)}}" data-sec="doc-results-container">Target: ${{escapeHtml(tgtDoc)}}</a>` : ""}}
              </div>
            </div>
          `;
        }}).join("");
      }}

      drawer.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.6rem;">
          <div>
            <div class="brand-eyebrow" style="margin-bottom:0.2rem;">Interactive KPI Linked-Documents Inspector</div>
            <h3 style="margin:0; font-size:0.96rem;">${{headerTitle}}</h3>
          </div>
          <div style="display:flex; gap:0.45rem; align-items:center; flex-wrap:wrap;">
            <a href="#${{sectionId}}" class="btn btn-sm" id="kpi-drawer-sec-btn">Jump to Section &darr;</a>
            <a href="${{pageUrl}}" class="btn btn-sm">${{pageLabel}} &nearr;</a>
            <button type="button" class="btn btn-sm" id="kpi-drawer-close-btn">&times; Close</button>
          </div>
        </div>
        <div class="kpi-drawer-grid">${{itemsHtml}}</div>
      `;

      drawer.querySelector("#kpi-drawer-close-btn").addEventListener("click", () => {{
        state.activeKpiDrawer = "";
        renderKPIs(filteredDocs);
      }});
      drawer.querySelector("#kpi-drawer-sec-btn").addEventListener("click", e => {{
        e.preventDefault();
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
      }});
      drawer.querySelectorAll(".kpi-drawer-doc-jump").forEach(a => {{
        a.addEventListener("click", e => {{
          e.preventDefault();
          focusDocumentInSection(a.dataset.doc, a.dataset.sec, a.dataset.chunks === "1");
        }});
      }});
      drawer.querySelectorAll(".kpi-drawer-concept-jump").forEach(a => {{
        a.addEventListener("click", e => {{
          e.preventDefault();
          state.conceptId = a.dataset.concept;
          state.selectedGraphNodeId = state.conceptId;
          state.page = 1;
          refreshAll();
          const el = document.getElementById("word-cloud-panel");
          if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }});
      }});
      drawer.querySelectorAll(".kpi-drawer-tax-jump").forEach(a => {{
        a.addEventListener("click", e => {{
          e.preventDefault();
          state.taxonomyPath = a.dataset.tax;
          state.page = 1;
          refreshAll();
          const el = document.getElementById("taxonomy-list");
          if (el) el.scrollIntoView({{ behavior: "smooth", block: "start" }});
        }});
      }});
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

    /* Top-Level Domain & Slice Navigator + Breadcrumb Drill-Down */
    function renderDomainNavigator(filteredDocs) {{
      const crumbBar = document.getElementById("breadcrumb-bar");
      const grid = document.getElementById("domain-cards-grid");
      const scopeBadge = document.getElementById("graph-scope-badge");

      // 1. Render Breadcrumb Trail
      const crumbs = [{{ label: "All Domains Overview", action: () => {{
        state.taxonomyPath = "";
        state.techArea = "";
        state.status = "";
        state.docType = "";
        state.docId = "";
        state.conceptId = "";
        state.selectedGraphNodeId = "";
        document.getElementById("tech-filter").value = "";
        document.getElementById("status-filter").value = "";
        document.getElementById("type-filter").value = "";
        state.page = 1;
        refreshAll();
      }} }}];

      if (state.taxonomyPath) {{
        const parts = state.taxonomyPath.split(" > ");
        parts.forEach((part, idx) => {{
          const subPath = parts.slice(0, idx + 1).join(" > ");
          crumbs.push({{
            label: part,
            action: () => {{
              state.taxonomyPath = subPath;
              state.page = 1;
              refreshAll();
            }}
          }});
        }});
      }} else if (state.techArea) {{
        crumbs.push({{ label: `Tech Area: ${{state.techArea}}`, action: () => {{}} }});
      }} else if (state.status) {{
        crumbs.push({{ label: `Stage: ${{state.status.toUpperCase()}}`, action: () => {{}} }});
      }} else if (state.docType) {{
        crumbs.push({{ label: `Type: ${{state.docType.replace("_", " ")}}`, action: () => {{}} }});
      }}

      scopeBadge.textContent = crumbs[crumbs.length - 1].label;

      crumbBar.innerHTML = `<span style="color:var(--text-muted); margin-right:0.25rem;">Scope:</span>` +
        crumbs.map((c, idx) => {{
          const isLast = idx === crumbs.length - 1;
          return `<span class="crumb ${{isLast ? "current" : ""}}" data-idx="${{idx}}">${{escapeHtml(c.label)}}</span>` +
            (isLast ? "" : `<span class="crumb-sep">&rsaquo;</span>`);
        }}).join("") +
        `<span style="margin-left:auto; color:var(--text-muted); font-size:0.74rem;">${{filteredDocs.length}} matching docs</span>`;

      crumbBar.querySelectorAll(".crumb").forEach(el => {{
        el.addEventListener("click", () => {{
          const idx = Number(el.dataset.idx);
          if (crumbs[idx]) crumbs[idx].action();
        }});
      }});

      // 2. Render Top-Level Slice Cards based on active sliceDimension
      if (state.sliceDimension === "domain") {{
        // Root domains (parent_path === null)
        const roots = DB.taxonomy.filter(t => !t.parent_path);
        grid.innerHTML = roots.map(root => {{
          const rootDocs = DB.documents.filter(d => docMatchesTaxonomyPrefix(d, root.path));
          const isActive = state.taxonomyPath === root.path || state.taxonomyPath.startsWith(root.path + " > ");
          const children = DB.taxonomy.filter(t => t.parent_path && (t.parent_path === root.path || t.parent_path.startsWith(root.path + " > ")));
          return `
            <div class="domain-card ${{isActive ? "active" : ""}}" data-root="${{escapeHtml(root.path)}}">
              <div>
                <div class="domain-card-head">
                  <h3 class="domain-card-title">${{escapeHtml(root.label)}}</h3>
                  <span class="domain-card-count">${{rootDocs.length}} docs</span>
                </div>
                <div class="tax-uri" style="margin:0.15rem 0 0.45rem;">${{escapeHtml(root.ontologic_class_uri)}}</div>
              </div>
              <div class="domain-sub-pills">
                ${{children.map(ch => {{
                  const subActive = state.taxonomyPath === ch.path || state.taxonomyPath.startsWith(ch.path + " > ");
                  const depthPrefix = ch.parent_path === root.path ? "" : "↳ ";
                  return `<span class="sub-pill ${{subActive ? "active" : ""}}" data-subpath="${{escapeHtml(ch.path)}}">${{depthPrefix}}${{escapeHtml(ch.label)}} (${{ch.document_ids.length}})</span>`;
                }}).join("")}}
              </div>
            </div>
          `;
        }}).join("");

        grid.querySelectorAll(".domain-card").forEach(card => {{
          card.addEventListener("click", e => {{
            const subPill = e.target.closest(".sub-pill");
            if (subPill) {{
              e.stopPropagation();
              const sp = subPill.dataset.subpath;
              state.taxonomyPath = state.taxonomyPath === sp ? "" : sp;
            }} else {{
              const rp = card.dataset.root;
              state.taxonomyPath = state.taxonomyPath === rp ? "" : rp;
            }}
            state.page = 1;
            refreshAll();
          }});
        }});
      }} else if (state.sliceDimension === "tech") {{
        const areaMap = new Map();
        DB.documents.forEach(d => {{
          d.technology_areas.forEach(ta => {{
            if (!areaMap.has(ta)) areaMap.set(ta, []);
            areaMap.get(ta).push(d);
          }});
        }});
        const entries = [...areaMap.entries()].sort((a, b) => b[1].length - a[1].length);
        grid.innerHTML = entries.map(([ta, docs]) => {{
          const isActive = state.techArea === ta;
          const sampleConcepts = [...new Set(docs.flatMap(d => d.concept_ids))].slice(0, 3);
          return `
            <div class="domain-card ${{isActive ? "active" : ""}}" data-tech="${{escapeHtml(ta)}}">
              <div class="domain-card-head">
                <h3 class="domain-card-title">${{escapeHtml(ta)}}</h3>
                <span class="domain-card-count">${{docs.length}} docs</span>
              </div>
              <div class="domain-sub-pills">
                ${{sampleConcepts.map(c => `<span class="sub-pill">${{escapeHtml(c.replace("concept:", ""))}}</span>`).join("")}}
              </div>
            </div>
          `;
        }}).join("");
        grid.querySelectorAll(".domain-card").forEach(card => {{
          card.addEventListener("click", () => {{
            const ta = card.dataset.tech;
            state.techArea = state.techArea === ta ? "" : ta;
            document.getElementById("tech-filter").value = state.techArea;
            state.page = 1;
            refreshAll();
          }});
        }});
      }} else if (state.sliceDimension === "workflow") {{
        const stages = [
          {{ key: "to-read", label: "To-Read Queue", desc: "Queued papers & articles awaiting deep review" }},
          {{ key: "reading", label: "Currently Reading", desc: "Active deep-dive analysis in progress" }},
          {{ key: "read", label: "Completed & Synthesized", desc: "Reviewed and integrated into synthesis notes" }}
        ];
        grid.innerHTML = stages.map(st => {{
          const docs = DB.documents.filter(d => d.reading_status === st.key);
          const isActive = state.status === st.key;
          const highCount = docs.filter(d => d.priority === "high").length;
          return `
            <div class="domain-card ${{isActive ? "active" : ""}}" data-status="${{st.key}}">
              <div>
                <div class="domain-card-head">
                  <h3 class="domain-card-title">${{st.label}}</h3>
                  <span class="domain-card-count">${{docs.length}} docs</span>
                </div>
                <div class="panel-subtitle" style="margin-top:0.2rem;">${{st.desc}}</div>
              </div>
              <div class="domain-sub-pills">
                <span class="sub-pill">${{highCount}} high priority</span>
              </div>
            </div>
          `;
        }}).join("");
        grid.querySelectorAll(".domain-card").forEach(card => {{
          card.addEventListener("click", () => {{
            const st = card.dataset.status;
            state.status = state.status === st ? "" : st;
            document.getElementById("status-filter").value = state.status;
            state.page = 1;
            refreshAll();
          }});
        }});
      }} else if (state.sliceDimension === "doctype") {{
        const types = [
          {{ key: "academic_paper", label: "Academic Papers", desc: "Peer-reviewed & arXiv research papers" }},
          {{ key: "technical_paper", label: "Technical Papers", desc: "Industrial & architecture whitepapers" }},
          {{ key: "technical_article", label: "Technical Articles", desc: "Semiconductor Engineering & industry briefs" }},
          {{ key: "note", label: "Research & Synthesis Notes", desc: "Cross-paper synthesis & OntoLogic bridges" }}
        ];
        grid.innerHTML = types.map(tp => {{
          const docs = DB.documents.filter(d => d.doc_type === tp.key);
          const isActive = state.docType === tp.key;
          return `
            <div class="domain-card ${{isActive ? "active" : ""}}" data-doctype="${{tp.key}}">
              <div>
                <div class="domain-card-head">
                  <h3 class="domain-card-title">${{tp.label}}</h3>
                  <span class="domain-card-count">${{docs.length}} docs</span>
                </div>
                <div class="panel-subtitle" style="margin-top:0.2rem;">${{tp.desc}}</div>
              </div>
            </div>
          `;
        }}).join("");
        grid.querySelectorAll(".domain-card").forEach(card => {{
          card.addEventListener("click", () => {{
            const dt = card.dataset.doctype;
            state.docType = state.docType === dt ? "" : dt;
            document.getElementById("type-filter").value = state.docType;
            state.page = 1;
            refreshAll();
          }});
        }});
      }}
    }}

    function renderWordCloud(filteredDocs) {{
      const box = document.getElementById("word-cloud");
      // Compute scoped word cloud from currently filtered documents
      const counts = new Map();
      filteredDocs.forEach(doc => {{
        (doc.word_cloud || []).forEach(w => {{
          counts.set(w.term, (counts.get(w.term) || 0) + w.count);
        }});
      }});
      const sorted = [...counts.entries()]
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 24);
      const maxCount = sorted.length ? sorted[0][1] : 1;

      if (!sorted.length) {{
        box.innerHTML = `<span class="panel-subtitle">No terms in current filter scope.</span>`;
        return;
      }}

      box.innerHTML = sorted.map(([term, count]) => {{
        const weight = count / maxCount;
        const size = (0.74 + weight * 0.62).toFixed(2);
        const active = state.query.toLowerCase() === term.toLowerCase() ? "active" : "";
        return `<span class="wc-term ${{active}}" style="font-size:${{size}}rem" data-term="${{escapeHtml(term)}}" title="Scoped frequency: ${{count}}">${{escapeHtml(term)}}</span>`;
      }}).join("");
      box.querySelectorAll(".wc-term").forEach(el => {{
        el.addEventListener("click", () => {{
          const term = el.dataset.term;
          state.query = state.query === term ? "" : term;
          document.getElementById("search-input").value = state.query;
          state.page = 1;
          refreshAll();
        }});
      }});
    }}

    function renderTaxonomy() {{
      const list = document.getElementById("taxonomy-list");
      // If a top-level domain is selected, highlight or prioritize its subtree
      const items = state.taxonomyPath
        ? DB.taxonomy.filter(cat => cat.path === state.taxonomyPath || cat.path.startsWith(state.taxonomyPath + " > ") || state.taxonomyPath.startsWith(cat.path + " > "))
        : DB.taxonomy;

      list.innerHTML = items.map(cat => {{
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
          state.page = 1;
          refreshAll();
        }});
      }});
    }}

    function renderActiveFilterPills(filteredDocs) {{
      const row = document.getElementById("active-filters-row");
      const pills = [];
      if (state.taxonomyPath) pills.push({{ key: "taxonomyPath", label: `Domain Slice: ${{state.taxonomyPath}}` }});
      if (state.techArea) pills.push({{ key: "techArea", label: `Tech Area: ${{state.techArea}}` }});
      if (state.docId) pills.push({{ key: "docId", label: `Document: ${{state.docId}}` }});
      if (state.conceptId) pills.push({{ key: "conceptId", label: `Concept: ${{state.conceptId.replace("concept:", "")}}` }});
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
          <span style="font-size:0.76rem; color:var(--text-muted);">Active Slice (${{filteredDocs.length}} of ${{DB.documents.length}} docs):</span>
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
            state.page = 1;
            refreshAll();
          }});
        }});
      }}

      const banner = document.getElementById("graph-status-banner");
      const bannerText = document.getElementById("graph-status-text");
      if (pills.length) {{
        banner.hidden = false;
        bannerText.textContent = `${{pills.map(p => p.label).join(" • ")}} (${{filteredDocs.length}} docs in slice)`;
      }} else {{
        banner.hidden = true;
      }}
    }}

    function renderDocuments(filtered) {{
      const container = document.getElementById("doc-results-container");
      renderActiveFilterPills(filtered);

      if (!filtered.length) {{
        container.innerHTML = `<div class="panel" style="text-align:center; color: var(--text-muted);">No documents match the current domain slice or filters. Click "Reset All".</div>`;
        return;
      }}

      const totalPages = Math.max(1, Math.ceil(filtered.length / state.pageSize));
      if (state.page > totalPages) state.page = totalPages;
      const startIdx = (state.page - 1) * state.pageSize;
      const pageDocs = filtered.slice(startIdx, startIdx + state.pageSize);

      if (state.viewMode === "table") {{
        container.innerHTML = `
          <div class="synoptic-table-wrap">
            <table class="synoptic-table">
              <thead>
                <tr>
                  <th>Status / Priority</th>
                  <th>Document Title &amp; Authors</th>
                  <th>Type</th>
                  <th>Primary Domain &amp; Concepts</th>
                  <th>Chunks</th>
                </tr>
              </thead>
              <tbody>
                ${{pageDocs.map(doc => {{
                  const statusClass = `status-${{doc.reading_status}}`;
                  const prioClass = doc.priority === "high" ? "prio-high" : "";
                  const authors = doc.authors.length ? doc.authors.slice(0, 3).join(", ") + (doc.authors.length > 3 ? " et al." : "") : "Research Note";
                  const topConcepts = doc.concept_ids.slice(0, 4).map(c => `<span class="chip chip-concept doc-concept-chip" data-concept="${{escapeHtml(c)}}">${{escapeHtml(c.replace("concept:", ""))}}</span>`).join("");
                  const topTech = doc.technology_areas.slice(0, 2).map(t => `<span class="chip doc-tech-chip" data-tech="${{escapeHtml(t)}}">${{escapeHtml(t)}}</span>`).join("");
                  return `
                    <tr>
                      <td>
                        <div class="badge-row">
                          <span class="badge ${{statusClass}}">${{escapeHtml(doc.reading_status)}}</span>
                          <span class="badge ${{prioClass}}">${{escapeHtml(doc.priority)}}</span>
                        </div>
                      </td>
                      <td>
                        <div style="font-weight:700; margin-bottom:0.15rem;">
                          ${{doc.url ? `<a href="${{escapeHtml(doc.url)}}" target="_blank" rel="noopener">${{escapeHtml(doc.title)}}</a>` : escapeHtml(doc.title)}}
                        </div>
                        <div class="doc-meta">${{escapeHtml(doc.doc_id)}} &bull; ${{escapeHtml(authors)}} ${{doc.published_date ? `&bull; ${{escapeHtml(doc.published_date)}}` : ""}}</div>
                      </td>
                      <td><span class="badge">${{escapeHtml(doc.doc_type.replace("_", " "))}}</span></td>
                      <td>
                        <div class="chip-list" style="margin-bottom:0.25rem;">${{topTech}}</div>
                        <div class="chip-list">${{topConcepts}}</div>
                      </td>
                      <td>
                        <button class="btn btn-sm inspect-btn" data-doc="${{escapeHtml(doc.doc_id)}}" type="button">
                          ${{doc.chunks.length}} Chunks
                        </button>
                      </td>
                    </tr>
                  `;
                }}).join("")}}
              </tbody>
            </table>
            <div class="pagination-bar">
              <span>Showing ${{startIdx + 1}}&ndash;${{Math.min(filtered.length, startIdx + pageDocs.length)}} of ${{filtered.length}} documents in slice</span>
              <div style="display:flex; gap:0.4rem; align-items:center;">
                <button class="btn btn-sm" id="prev-page-btn" type="button" ${{state.page <= 1 ? "disabled" : ""}}>&larr; Prev</button>
                <span style="font-family:var(--font-mono); font-size:0.75rem;">Page ${{state.page}} / ${{totalPages}}</span>
                <button class="btn btn-sm" id="next-page-btn" type="button" ${{state.page >= totalPages ? "disabled" : ""}}>Next &rarr;</button>
              </div>
            </div>
          </div>
        `;
      }} else {{
        container.innerHTML = `
          <div class="doc-grid">
            ${{pageDocs.map(doc => {{
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
                    ${{doc.notes ? `<p style="font-size:0.8rem; color: var(--text-muted); margin: 0.45rem 0 0;"><strong>Notes:</strong> ${{escapeHtml(doc.notes)}}</p>` : ""}}
                  </div>
                  <div>
                    <div class="chip-list" style="margin-bottom:0.4rem;">${{techChips}}</div>
                    <div class="chip-list" style="margin-bottom:0.55rem;">${{conceptChips}}</div>
                    <div style="display:flex; justify-content:space-between; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                      <div class="badge-row">${{relBadges}}</div>
                      <button class="btn btn-sm inspect-btn" data-doc="${{escapeHtml(doc.doc_id)}}" type="button">
                        Inspect ${{doc.chunks.length}} Chunks
                      </button>
                    </div>
                  </div>
                </article>
              `;
            }}).join("")}}
          </div>
          <div class="pagination-bar" style="background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius); margin-top:0.85rem;">
            <span>Showing ${{startIdx + 1}}&ndash;${{Math.min(filtered.length, startIdx + pageDocs.length)}} of ${{filtered.length}} documents in slice</span>
            <div style="display:flex; gap:0.4rem; align-items:center;">
              <button class="btn btn-sm" id="prev-page-btn" type="button" ${{state.page <= 1 ? "disabled" : ""}}>&larr; Prev</button>
              <span style="font-family:var(--font-mono); font-size:0.75rem;">Page ${{state.page}} / ${{totalPages}}</span>
              <button class="btn btn-sm" id="next-page-btn" type="button" ${{state.page >= totalPages ? "disabled" : ""}}>Next &rarr;</button>
            </div>
          </div>
        `;
      }}

      container.querySelectorAll(".inspect-btn").forEach(btn => {{
        btn.addEventListener("click", () => openChunkModal(btn.dataset.doc));
      }});
      container.querySelectorAll(".doc-tech-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          const t = chip.dataset.tech;
          state.techArea = state.techArea === t ? "" : t;
          document.getElementById("tech-filter").value = state.techArea;
          state.page = 1;
          refreshAll();
        }});
      }});
      container.querySelectorAll(".doc-concept-chip").forEach(chip => {{
        chip.addEventListener("click", () => {{
          const c = chip.dataset.concept;
          state.conceptId = state.conceptId === c ? "" : c;
          state.selectedGraphNodeId = state.conceptId;
          state.page = 1;
          refreshAll();
        }});
      }});
      const prevBtn = document.getElementById("prev-page-btn");
      const nextBtn = document.getElementById("next-page-btn");
      if (prevBtn) prevBtn.addEventListener("click", () => {{ if (state.page > 1) {{ state.page--; renderDocuments(filtered); }} }});
      if (nextBtn) nextBtn.addEventListener("click", () => {{ if (state.page < totalPages) {{ state.page++; renderDocuments(filtered); }} }});
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
        {{ type: "Document", rx: 110, ry: 65, offset: 0.15 }},
        {{ type: "Concept", rx: 215, ry: 110, offset: 0.55 }},
        {{ type: "TaxonomyCategory", rx: 305, ry: 142, offset: 0.95 }},
        {{ type: "TechnologyArea", rx: 360, ry: 162, offset: 1.35 }}
      ];

      ringConfig.forEach(cfg => {{
        const list = byType[cfg.type] || [];
        list.forEach((n, idx) => {{
          const angle = cfg.offset + (2 * Math.PI * idx) / Math.max(1, list.length);
          graphNodes.push({{
            ...n,
            x: 410 + Math.cos(angle) * cfg.rx,
            y: 180 + Math.sin(angle) * cfg.ry
          }});
        }});
      }});

      const nodeById = Object.fromEntries(graphNodes.map(n => [n.node_id, n]));
      graphEdges = DB.knowledge_graph.edges.filter(e => nodeById[e.source] && nodeById[e.target]);

      for (let iter = 0; iter < 80; iter++) {{
        for (let i = 0; i < graphNodes.length; i++) {{
          for (let j = i + 1; j < graphNodes.length; j++) {{
            const dx = graphNodes[j].x - graphNodes[i].x;
            const dy = graphNodes[j].y - graphNodes[i].y;
            const dist = Math.hypot(dx, dy) || 0.1;
            const minDist = 62;
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
          n.x = Math.max(45, Math.min(755, n.x));
          n.y = Math.max(26, Math.min(335, n.y));
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
      state.docId = "";
      state.conceptId = "";
      state.selectedGraphNodeId = "";

      if (!alreadyActive) {{
        state.selectedGraphNodeId = node.node_id;
        if (node.node_type === "Document") {{
          state.docId = (node.properties && node.properties.doc_id) || node.node_id.replace("doc:", "");
        }} else if (node.node_type === "Concept") {{
          state.conceptId = node.node_id;
        }} else if (node.node_type === "TechnologyArea") {{
          state.techArea = state.techArea === node.label ? "" : node.label;
          document.getElementById("tech-filter").value = state.techArea;
        }} else if (node.node_type === "TaxonomyCategory") {{
          const path = (node.properties && node.properties.path) || "";
          state.taxonomyPath = state.taxonomyPath === path ? "" : path;
        }}
      }}
      state.page = 1;
      refreshAll();
    }}

    function drawGraph(filteredDocs) {{
      const svg = document.getElementById("kg-svg");
      const allowedDocIds = new Set(filteredDocs.map(d => `doc:${{d.doc_id}}`));
      const isSliceScoped = filteredDocs.length < DB.documents.length && !state.docId;

      // Keep nodes that belong to the active slice (or are connected to visible documents in the slice)
      const sliceConnectedNodeIds = new Set(allowedDocIds);
      if (isSliceScoped) {{
        graphEdges.forEach(e => {{
          if (allowedDocIds.has(e.source)) sliceConnectedNodeIds.add(e.target);
          if (allowedDocIds.has(e.target)) sliceConnectedNodeIds.add(e.source);
        }});
      }}

      const visibleNodes = graphNodes.filter(n => {{
        if (state.hiddenNodeTypes.has(n.node_type)) return false;
        if (isSliceScoped && !sliceConnectedNodeIds.has(n.node_id)) return false;
        return true;
      }});

      const nodeById = Object.fromEntries(visibleNodes.map(n => [n.node_id, n]));
      const visibleEdges = graphEdges.filter(e => nodeById[e.source] && nodeById[e.target]);

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
        const opacity = hasHighlight ? (connected ? "0.95" : "0.18") : "0.85";
        return `<line class="kg-edge" data-idx="${{idx}}" data-source="${{escapeHtml(e.source)}}" data-target="${{escapeHtml(e.target)}}" x1="${{s.x}}" y1="${{s.y}}" x2="${{t.x}}" y2="${{t.y}}" stroke="${{stroke}}" stroke-width="${{width}}" opacity="${{opacity}}" />`;
      }}).join("");

      const nodeMarkup = visibleNodes.map(n => {{
        const color = NODE_COLORS[n.node_type] || "#38bdf8";
        const isSelected = activeIds.has(n.node_id);
        const isNeighbor = neighborIds.has(n.node_id);
        const r = n.node_type === "Document" ? 11 : 8;
        const opacity = hasHighlight ? (isNeighbor ? "1" : "0.24") : "1";
        const shortLabel = n.label.length > 26 ? n.label.slice(0, 24) + "…" : n.label;
        const halo = isSelected
          ? `<circle class="kg-halo" r="${{r + 6}}" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-dasharray="3 2"></circle>`
          : "";
        return `
          <g class="kg-node" data-id="${{escapeHtml(n.node_id)}}" transform="translate(${{n.x}},${{n.y}})" opacity="${{opacity}}" style="cursor:grab">
            <title>${{escapeHtml(n.node_type)}}: ${{escapeHtml(n.label)}} (click to filter, drag to move)</title>
            ${{halo}}
            <circle r="${{r}}" fill="${{color}}" stroke="${{isSelected ? "#ffffff" : "#0f172a"}}" stroke-width="${{isSelected ? "2.8" : "2"}}"></circle>
            <text x="${{r + 5}}" y="4" fill="currentColor" font-size="${{isSelected ? "11.2" : "10"}}" font-weight="${{isSelected ? "700" : "500"}}" font-family="var(--font-sans)" pointer-events="none">${{escapeHtml(shortLabel)}}</text>
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
          drawGraph(getFilteredDocuments());
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
        const newH = Math.max(120, Math.min(820, viewBox.h * factor));
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
        viewBox = {{ x: 0, y: 0, w: 820, h: 360 }};
        updateViewBox();
      }});
      document.getElementById("relayout-graph-btn").addEventListener("click", () => {{
        viewBox = {{ x: 0, y: 0, w: 820, h: 360 }};
        updateViewBox();
        computeGraphLayout();
        drawGraph(getFilteredDocuments());
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
      state.page = 1;
      document.getElementById("search-input").value = "";
      document.getElementById("status-filter").value = "";
      document.getElementById("priority-filter").value = "";
      document.getElementById("type-filter").value = "";
      document.getElementById("tech-filter").value = "";
      refreshAll();
    }}

    function refreshAll() {{
      const filteredDocs = getFilteredDocuments();
      renderKPIs(filteredDocs);
      renderDomainNavigator(filteredDocs);
      drawGraph(filteredDocs);
      renderWordCloud(filteredDocs);
      renderTaxonomy();
      renderDocuments(filteredDocs);
    }}

    document.querySelectorAll("#slice-dimension-tabs .slice-tab").forEach(tab => {{
      tab.addEventListener("click", () => {{
        document.querySelectorAll("#slice-dimension-tabs .slice-tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        state.sliceDimension = tab.dataset.dim;
        refreshAll();
      }});
    }});

    document.getElementById("view-table-btn").addEventListener("click", () => {{
      state.viewMode = "table";
      document.getElementById("view-table-btn").classList.add("active");
      document.getElementById("view-cards-btn").classList.remove("active");
      renderDocuments(getFilteredDocuments());
    }});
    document.getElementById("view-cards-btn").addEventListener("click", () => {{
      state.viewMode = "cards";
      document.getElementById("view-cards-btn").classList.add("active");
      document.getElementById("view-table-btn").classList.remove("active");
      renderDocuments(getFilteredDocuments());
    }});

    document.getElementById("search-input").addEventListener("input", e => {{
      state.query = e.target.value.trim();
      state.page = 1;
      refreshAll();
    }});
    document.getElementById("status-filter").addEventListener("change", e => {{
      state.status = e.target.value;
      state.page = 1;
      refreshAll();
    }});
    document.getElementById("priority-filter").addEventListener("change", e => {{
      state.priority = e.target.value;
      state.page = 1;
      refreshAll();
    }});
    document.getElementById("type-filter").addEventListener("change", e => {{
      state.docType = e.target.value;
      state.page = 1;
      refreshAll();
    }});
    document.getElementById("tech-filter").addEventListener("change", e => {{
      state.techArea = e.target.value;
      state.page = 1;
      refreshAll();
    }});
    document.getElementById("clear-filters").addEventListener("click", clearAllFilters);
    document.getElementById("reset-graph-btn").addEventListener("click", clearAllFilters);
    document.getElementById("graph-status-clear").addEventListener("click", clearAllFilters);
    document.getElementById("close-modal").addEventListener("click", () => {{
      document.getElementById("chunk-modal").close();
    }});
    const THEMES = ["dark", "tron", "light"];
    function applyTheme(themeName) {{
      const valid = THEMES.includes(themeName) ? themeName : "dark";
      document.documentElement.dataset.theme = valid;
      try {{ localStorage.setItem("reading_db_theme", valid); }} catch (_) {{}}
      document.querySelectorAll(".theme-opt").forEach(btn => {{
        btn.classList.toggle("active", btn.dataset.setTheme === valid);
      }});
    }}
    document.querySelectorAll(".theme-opt").forEach(btn => {{
      btn.addEventListener("click", () => applyTheme(btn.dataset.setTheme));
    }});
    document.getElementById("theme-toggle").addEventListener("click", () => {{
      const curr = document.documentElement.dataset.theme || "dark";
      const next = THEMES[(THEMES.indexOf(curr) + 1) % THEMES.length];
      applyTheme(next);
    }});
    try {{
      const savedTheme = localStorage.getItem("reading_db_theme");
      if (savedTheme) applyTheme(savedTheme);
    }} catch (_) {{}}

    initTechDropdown();
    computeGraphLayout();
    renderGraphLegend();
    setupGraphInteractions();

    // Support deep-linking from taxonomy.html / chunks.html / summary.html via #doc=<doc_id>
    if (window.location.hash && window.location.hash.startsWith("#doc=")) {{
      const targetDocId = decodeURIComponent(window.location.hash.slice(5));
      if (DB.documents.some(d => d.doc_id === targetDocId)) {{
        state.docId = targetDocId;
        state.selectedGraphNodeId = `doc:${{targetDocId}}`;
      }}
    }}
    refreshAll();
  </script>
</body>
</html>
"""


def render_markdown_artifact_html(
    page_key: str,
    page_title: str,
    page_subtitle: str,
    markdown_text: str,
    raw_links: list[dict[str, str]],
) -> str:
    """Render a standalone, themed HTML page (`taxonomy.html`, `chunks.html`, `summary.html`) that renders Markdown and preserves download/raw file links."""
    md_json = json.dumps(markdown_text)
    tax_active = "active" if page_key == "taxonomy" else ""
    chunks_active = "active" if page_key == "chunks" else ""
    summary_active = "active" if page_key == "summary" else ""

    raw_buttons_html = "\n".join(
        f'<a class="btn btn-sm" href="{link["href"]}" '
        + (f'download="{link["download"]}"' if link.get("download") else 'target="_blank" rel="noopener"')
        + f'>{link["label"]}</a>'
        for link in raw_links
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{page_title} — Reading DB Markdown Render</title>
  <style>
    :root {{
      --bg: #0b0f19;
      --bg-elevated: rgba(19, 27, 46, 0.85);
      --bg-card: rgba(23, 33, 56, 0.9);
      --bg-chip: rgba(56, 189, 248, 0.12);
      --border: rgba(148, 163, 184, 0.18);
      --border-strong: rgba(56, 189, 248, 0.48);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent-2: #a855f7;
      --accent-3: #10b981;
      --accent-warn: #f59e0b;
      --accent-danger: #f43f5e;
      --shadow: 0 16px 36px -14px rgba(2, 6, 23, 0.75);
      --radius: 13px;
      --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
    }}
    [data-theme="light"] {{
      --bg: #f8fafc;
      --bg-elevated: rgba(255, 255, 255, 0.94);
      --bg-card: #ffffff;
      --bg-chip: rgba(2, 132, 199, 0.1);
      --border: rgba(15, 23, 42, 0.12);
      --border-strong: rgba(2, 132, 199, 0.5);
      --text: #0f172a;
      --text-muted: #475569;
      --accent: #0284c7;
      --accent-2: #7c3aed;
      --accent-3: #059669;
      --shadow: 0 10px 26px -10px rgba(15, 23, 42, 0.1);
    }}
    [data-theme="tron"] {{
      --bg: #020813;
      --bg-elevated: rgba(3, 14, 30, 0.9);
      --bg-card: rgba(4, 18, 38, 0.92);
      --bg-chip: rgba(0, 240, 255, 0.14);
      --border: rgba(0, 240, 255, 0.34);
      --border-strong: #00f0ff;
      --text: #e2fbff;
      --text-muted: #5ec2e8;
      --accent: #00f0ff;
      --accent-2: #0088ff;
      --accent-3: #00ffaa;
      --accent-warn: #ff9e00;
      --accent-danger: #ff2a6d;
      --shadow: 0 0 22px rgba(0, 240, 255, 0.18), inset 0 0 14px rgba(0, 240, 255, 0.07);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: var(--font-sans);
      background:
        radial-gradient(circle at 12% 10%, rgba(56, 189, 248, 0.11), transparent 35%),
        radial-gradient(circle at 88% 12%, rgba(168, 85, 247, 0.11), transparent 38%),
        var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
    }}
    [data-theme="tron"] body {{
      background-color: #020813;
      background-image:
        radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.22), transparent 55%),
        radial-gradient(circle at 85% 20%, rgba(0, 136, 255, 0.18), transparent 45%),
        linear-gradient(rgba(0, 240, 255, 0.075) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 240, 255, 0.075) 1px, transparent 1px);
      background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px;
      background-attachment: fixed;
    }}
    [data-theme="tron"] header.hero,
    [data-theme="tron"] .artifact-toolbar,
    [data-theme="tron"] .toc-panel,
    [data-theme="tron"] .md-panel {{
      border-color: rgba(0, 240, 255, 0.38);
      box-shadow: 0 0 18px rgba(0, 240, 255, 0.14), inset 0 0 12px rgba(0, 240, 255, 0.05);
    }}
    [data-theme="tron"] h1,
    [data-theme="tron"] .brand-eyebrow,
    [data-theme="tron"] .md-body h2 {{
      text-shadow: 0 0 10px rgba(0, 240, 255, 0.55);
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .shell {{
      max-width: 1420px;
      margin: 0 auto;
      padding: 1.25rem 1.4rem 3rem;
    }}
    header.hero {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding: 1.1rem 1.4rem;
      border-radius: var(--radius);
      background: var(--bg-elevated);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 1rem;
    }}
    .brand-eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent);
      background: var(--bg-chip);
      padding: 0.2rem 0.6rem;
      border-radius: 999px;
      border: 1px solid var(--border-strong);
      margin-bottom: 0.35rem;
    }}
    h1 {{
      margin: 0 0 0.2rem;
      font-size: clamp(1.3rem, 2vw, 1.75rem);
      letter-spacing: -0.02em;
    }}
    .subtitle {{
      margin: 0;
      color: var(--text-muted);
      max-width: 760px;
      font-size: 0.88rem;
    }}
    .hero-actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      align-items: center;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.42rem 0.75rem;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: var(--bg-card);
      color: var(--text);
      cursor: pointer;
      transition: all 0.14s ease;
      user-select: none;
    }}
    .btn:hover {{
      border-color: var(--accent);
      transform: translateY(-1px);
      text-decoration: none;
    }}
    .btn.active {{
      border-color: var(--accent);
      background: var(--bg-chip);
      color: var(--accent);
    }}
    .btn-sm {{
      padding: 0.28rem 0.62rem;
      font-size: 0.74rem;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #fff;
      border: none;
    }}
    .theme-group {{
      display: inline-flex;
      align-items: center;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 0.18rem;
      gap: 0.2rem;
    }}
    .theme-opt {{
      font-size: 0.72rem;
      font-family: var(--font-mono);
      font-weight: 600;
      padding: 0.28rem 0.55rem;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
    }}
    .theme-opt.active {{
      background: var(--bg-card);
      color: var(--accent);
      border-color: var(--border-strong);
    }}
    .theme-opt[data-set-theme="tron"].active {{
      color: #00f0ff;
      border-color: #00f0ff;
      box-shadow: 0 0 12px rgba(0, 240, 255, 0.45);
      text-shadow: 0 0 8px rgba(0, 240, 255, 0.75);
    }}
    .artifact-toolbar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.75rem;
      padding: 0.8rem 1.1rem;
      border-radius: var(--radius);
      background: var(--bg-card);
      border: 1px solid var(--border);
      box-shadow: var(--shadow);
      margin-bottom: 1rem;
    }}
    .artifact-layout {{
      display: grid;
      grid-template-columns: 290px 1fr;
      gap: 1.1rem;
      align-items: start;
    }}
    @media (max-width: 980px) {{
      .artifact-layout {{
        grid-template-columns: 1fr;
      }}
    }}
    .toc-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 0.95rem 1rem;
      box-shadow: var(--shadow);
      position: sticky;
      top: 1rem;
      max-height: calc(100vh - 2rem);
      overflow-y: auto;
    }}
    .toc-list {{
      display: flex;
      flex-direction: column;
      gap: 0.28rem;
      margin-top: 0.55rem;
    }}
    .toc-link {{
      font-size: 0.76rem;
      color: var(--text-muted);
      padding: 0.24rem 0.45rem;
      border-radius: 6px;
      display: block;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .toc-link:hover {{
      background: var(--bg-chip);
      color: var(--accent);
      text-decoration: none;
    }}
    .toc-link.depth-3 {{
      padding-left: 1.1rem;
      font-size: 0.72rem;
    }}
    .md-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 1.4rem 1.65rem;
      box-shadow: var(--shadow);
      min-width: 0;
    }}
    .md-body h1 {{
      font-size: 1.55rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.5rem;
      margin-top: 0;
    }}
    .md-body h2 {{
      font-size: 1.22rem;
      color: var(--accent);
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.35rem;
      margin-top: 1.8rem;
    }}
    .md-body h3 {{
      font-size: 1.02rem;
      margin-top: 1.35rem;
      color: var(--text);
    }}
    .md-body h4 {{
      font-size: 0.9rem;
      font-family: var(--font-mono);
      color: var(--accent-2);
      margin-top: 1.1rem;
    }}
    .md-body code {{
      font-family: var(--font-mono);
      font-size: 0.78rem;
      background: var(--bg-chip);
      color: var(--accent);
      padding: 0.12rem 0.38rem;
      border-radius: 5px;
      border: 1px solid var(--border);
    }}
    .md-body pre {{
      background: rgba(2, 6, 23, 0.55);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.95rem 1.1rem;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 0.78rem;
    }}
    [data-theme="light"] .md-body pre {{
      background: #f1f5f9;
    }}
    .md-body pre code {{
      background: transparent;
      border: none;
      padding: 0;
      color: var(--text);
    }}
    .md-table-wrap {{
      overflow-x: auto;
      margin: 0.85rem 0 1.25rem;
      border: 1px solid var(--border);
      border-radius: 10px;
    }}
    .md-body table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.81rem;
    }}
    .md-body th, .md-body td {{
      padding: 0.58rem 0.8rem;
      text-align: left;
      border-bottom: 1px solid var(--border);
    }}
    .md-body th {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      text-transform: uppercase;
      color: var(--text-muted);
      background: rgba(2, 6, 23, 0.25);
    }}
    .md-body ul {{
      padding-left: 1.35rem;
    }}
    .md-body li {{
      margin-bottom: 0.32rem;
    }}
    .search-input {{
      background: var(--bg);
      color: var(--text);
      border: 1px solid var(--border);
      padding: 0.4rem 0.7rem;
      border-radius: 7px;
      font-size: 0.8rem;
      min-width: 240px;
    }}
  </style>
</head>
<body>
  <div class="shell">
    <header class="hero">
      <div>
        <div class="brand-eyebrow">OntoLogic-Ready Knowledge Base &bull; Rendered Markdown View</div>
        <h1>{page_title}</h1>
        <p class="subtitle">{page_subtitle}</p>
      </div>
      <div class="hero-actions">
        <a class="btn" href="index.html">&larr; Dashboard</a>
        <a class="btn" href="knowledge_graph.json" target="_blank" rel="noopener">JSON-LD</a>
        <a class="btn {tax_active}" href="taxonomy.html">Taxonomy</a>
        <a class="btn {chunks_active}" href="chunks.html">Chunks</a>
        <a class="btn {summary_active}" href="summary.html">Summary MD</a>
        <div class="theme-group" role="group" aria-label="Theme Selector">
          <button class="theme-opt active" type="button" data-set-theme="dark">Dark</button>
          <button class="theme-opt" type="button" data-set-theme="tron">&#x26A1; TRON</button>
          <button class="theme-opt" type="button" data-set-theme="light">Light</button>
        </div>
        <button class="btn btn-primary" id="theme-toggle" type="button">Theme</button>
      </div>
    </header>

    <section class="artifact-toolbar">
      <div style="display:flex; flex-wrap:wrap; gap:0.45rem; align-items:center;">
        <span style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted); margin-right:0.2rem;">Raw &amp; Download Links:</span>
        {raw_buttons_html}
        <button class="btn btn-sm" id="copy-md-btn" type="button">Copy Markdown</button>
        <button class="btn btn-sm" id="toggle-raw-view-btn" type="button">View Raw Markdown Source</button>
      </div>
      <div style="display:flex; gap:0.45rem; align-items:center;">
        <input type="search" id="md-filter-input" class="search-input" placeholder="Filter sections, headings, or documents..." />
      </div>
    </section>

    <div class="artifact-layout">
      <aside class="toc-panel">
        <div style="font-family:var(--font-mono); font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--accent);">Table of Contents</div>
        <nav class="toc-list" id="toc-list"></nav>
      </aside>
      <main class="md-panel">
        <div class="md-body" id="md-rendered"></div>
        <pre id="md-raw-source" hidden style="margin:0; white-space:pre-wrap;"></pre>
      </main>
    </div>
  </div>

  <script>
    const RAW_MD = {md_json};

    function escapeHtml(str) {{
      return String(str ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
    }}

    function slugify(text) {{
      return String(text || "")
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "") || "section";
    }}

    function formatInline(text) {{
      let s = escapeHtml(text);
      s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
      s = s.replace(/\\*\\*([^*]+)\\*\\*/g, "<strong>$1</strong>");
      s = s.replace(/\\*([^*]+)\\*/g, "<em>$1</em>");
      s = s.replace(/\\[([^\\]]+)\\]\\(([^)]+)\\)/g, (_, label, url) => {{
        const isExt = url.startsWith("http://") || url.startsWith("https://");
        const attrs = isExt ? ' target="_blank" rel="noopener"' : "";
        return `<a href="${{url}}"${{attrs}}>${{label}}</a>`;
      }});
      return s;
    }}

    function renderMarkdown(mdText, filterQuery = "") {{
      const lines = mdText.split(/\\r?\\n/);
      const toc = [];
      let html = "";
      let inCode = false;
      let codeLang = "";
      let codeBuf = [];
      let inTable = false;
      let tableRows = [];
      let inList = false;

      function flushList() {{
        if (inList) {{
          html += "</ul>";
          inList = false;
        }}
      }}

      function flushTable() {{
        if (!inTable) return;
        inTable = false;
        if (tableRows.length < 2) return;
        const headerCells = tableRows[0].split("|").slice(1, -1).map(c => c.trim());
        const bodyRows = tableRows.slice(2);
        const q = filterQuery.toLowerCase();
        const filteredBody = q
          ? bodyRows.filter(r => r.toLowerCase().includes(q))
          : bodyRows;
        html += `<div class="md-table-wrap"><table><thead><tr>` +
          headerCells.map(h => `<th>${{formatInline(h)}}</th>`).join("") +
          `</tr></thead><tbody>` +
          filteredBody.map(row => {{
            const cells = row.split("|").slice(1, -1).map(c => c.trim());
            return `<tr>` + cells.map(c => `<td>${{formatInline(c)}}</td>`).join("") + `</tr>`;
          }}).join("") +
          `</tbody></table></div>`;
        tableRows = [];
      }}

      for (let i = 0; i < lines.length; i++) {{
        const line = lines[i];
        if (line.startsWith("```")) {{
          flushList();
          flushTable();
          if (!inCode) {{
            inCode = true;
            codeLang = line.slice(3).trim();
            codeBuf = [];
          }} else {{
            inCode = false;
            html += `<pre data-lang="${{escapeHtml(codeLang)}}"><code>${{escapeHtml(codeBuf.join("\\n"))}}</code></pre>`;
            codeBuf = [];
          }}
          continue;
        }}
        if (inCode) {{
          codeBuf.push(line);
          continue;
        }}

        if (line.trim().startsWith("|") && line.trim().endsWith("|")) {{
          flushList();
          inTable = true;
          tableRows.push(line.trim());
          continue;
        }} else if (inTable) {{
          flushTable();
        }}

        const hMatch = line.match(/^(#{{1,4}})\\s+(.*)$/);
        if (hMatch) {{
          flushList();
          const level = hMatch[1].length;
          const rawHeading = hMatch[2].trim();
          const id = `${{slugify(rawHeading)}}-${{i}}`;
          if (level === 2 || level === 3) {{
            toc.push({{ level, id, label: rawHeading.replace(/`/g, "") }});
          }}
          html += `<h${{level}} id="${{id}}">${{formatInline(rawHeading)}}</h${{level}}>`;
          continue;
        }}

        if (line.match(/^\\s*-\\s+/)) {{
          if (filterQuery && !line.toLowerCase().includes(filterQuery.toLowerCase())) {{
            continue;
          }}
          if (!inList) {{
            html += "<ul>";
            inList = true;
          }}
          const itemText = line.replace(/^\\s*-\\s+/, "");
          html += `<li>${{formatInline(itemText)}}</li>`;
          continue;
        }} else {{
          flushList();
        }}

        if (!line.trim()) {{
          continue;
        }}

        if (!filterQuery || line.toLowerCase().includes(filterQuery.toLowerCase())) {{
          html += `<p>${{formatInline(line)}}</p>`;
        }}
      }}
      flushList();
      flushTable();

      document.getElementById("md-rendered").innerHTML = html;
      document.getElementById("md-raw-source").textContent = mdText;

      const tocEl = document.getElementById("toc-list");
      const q = filterQuery.toLowerCase();
      const visibleToc = q ? toc.filter(t => t.label.toLowerCase().includes(q)) : toc.slice(0, 120);
      tocEl.innerHTML = visibleToc.map(t => `
        <a class="toc-link depth-${{t.level}}" href="#${{t.id}}" title="${{escapeHtml(t.label)}}">${{escapeHtml(t.label)}}</a>
      `).join("");
    }}

    const THEMES = ["dark", "tron", "light"];
    function applyTheme(themeName) {{
      const valid = THEMES.includes(themeName) ? themeName : "dark";
      document.documentElement.dataset.theme = valid;
      try {{ localStorage.setItem("reading_db_theme", valid); }} catch (_) {{}}
      document.querySelectorAll(".theme-opt").forEach(btn => {{
        btn.classList.toggle("active", btn.dataset.setTheme === valid);
      }});
    }}
    document.querySelectorAll(".theme-opt").forEach(btn => {{
      btn.addEventListener("click", () => applyTheme(btn.dataset.setTheme));
    }});
    document.getElementById("theme-toggle").addEventListener("click", () => {{
      const curr = document.documentElement.dataset.theme || "dark";
      const next = THEMES[(THEMES.indexOf(curr) + 1) % THEMES.length];
      applyTheme(next);
    }});
    try {{
      const savedTheme = localStorage.getItem("reading_db_theme");
      if (savedTheme) applyTheme(savedTheme);
    }} catch (_) {{}}

    document.getElementById("md-filter-input").addEventListener("input", e => {{
      renderMarkdown(RAW_MD, e.target.value.trim());
    }});
    document.getElementById("copy-md-btn").addEventListener("click", async e => {{
      try {{
        await navigator.clipboard.writeText(RAW_MD);
        e.target.textContent = "Copied!";
        setTimeout(() => {{ e.target.textContent = "Copy Markdown"; }}, 1400);
      }} catch (_) {{}}
    }});
    let showingRaw = false;
    document.getElementById("toggle-raw-view-btn").addEventListener("click", e => {{
      showingRaw = !showingRaw;
      document.getElementById("md-rendered").hidden = showingRaw;
      document.getElementById("md-raw-source").hidden = !showingRaw;
      e.target.textContent = showingRaw ? "View Rendered Markdown" : "View Raw Markdown Source";
    }});

    renderMarkdown(RAW_MD);
  </script>
</body>
</html>
"""
