"""Smoke and integration tests for the reading_list package."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import reading_list
from reading_list.chunker import (
    build_word_cloud,
    chunk_document,
    classify_content,
)
from reading_list.cli import load_corpus, main, run_build
from reading_list.graph import build_knowledge_graph, build_taxonomy_index

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "seed_corpus.json"


class ReadingListScaffoldTests(unittest.TestCase):
    def test_package_version_and_fixture_load(self) -> None:
        self.assertEqual(reading_list.__version__, "0.1.0")
        docs = load_corpus(FIXTURE_PATH)
        self.assertEqual(len(docs), 2)
        doc_ids = {d.doc_id for d in docs}
        self.assertIn("semieng-2026-bare-ai-monitors", doc_ids)
        self.assertIn("arxiv-2610.08739v2", doc_ids)

    def test_semantic_chunking_and_taxonomy_hierarchy(self) -> None:
        docs = load_corpus(FIXTURE_PATH)
        chunks_by_doc = {d.doc_id: chunk_document(d) for d in docs}

        paper_chunks = chunks_by_doc["arxiv-2610.08739v2"]
        self.assertEqual(len(paper_chunks), 5)

        all_concepts = {
            cid for chunk in paper_chunks for cid in chunk.concept_ids
        }
        self.assertIn("concept:bare-ai", all_concepts)
        self.assertIn("concept:apc", all_concepts)
        self.assertIn("concept:pulse", all_concepts)
        self.assertIn("concept:asi", all_concepts)
        self.assertIn("concept:bit-flip-attack", all_concepts)

        all_taxonomy_paths = {
            path for chunk in paper_chunks for path in chunk.taxonomy_paths
        }
        self.assertIn(
            "Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
            all_taxonomy_paths,
        )
        self.assertIn(
            "Hardware & Semiconductor Systems > AI Accelerators",
            all_taxonomy_paths,
        )
        self.assertIn("Hardware & Semiconductor Systems", all_taxonomy_paths)
        self.assertIn(
            "Security & Resilience > Hardware Fault Attacks > Bit-Flip Attacks",
            all_taxonomy_paths,
        )

    def test_word_cloud_and_knowledge_graph_links(self) -> None:
        docs = load_corpus(FIXTURE_PATH)
        chunks_by_doc = {d.doc_id: chunk_document(d) for d in docs}

        wc = build_word_cloud(docs, chunks_by_doc)
        top_terms = {item["term"] for item in wc["global_word_cloud"]}
        self.assertIn("bare-ai", top_terms)
        self.assertIn("bit-flip", top_terms)

        kg = build_knowledge_graph(docs, chunks_by_doc)
        kg_dict = kg.to_dict()
        self.assertIn("@context", kg_dict)
        self.assertIn("ontologic", kg_dict["@context"])

        edges = {(e.source, e.predicate, e.target) for e in kg.edges}
        self.assertIn(
            (
                "doc:semieng-2026-bare-ai-monitors",
                "REPORTS_ON",
                "doc:arxiv-2610.08739v2",
            ),
            edges,
        )
        self.assertIn(
            (
                "doc:arxiv-2610.08739v2",
                "AFFILIATED_WITH",
                "institution:university-of-florida",
            ),
            edges,
        )
        self.assertIn(
            (
                "doc:arxiv-2610.08739v2",
                "AFFILIATED_WITH",
                "institution:university-of-texas-at-dallas",
            ),
            edges,
        )
        self.assertIn(
            (
                "doc:arxiv-2610.08739v2",
                "AFFILIATED_WITH",
                "institution:rensselaer-polytechnic-institute",
            ),
            edges,
        )

        tax_index = build_taxonomy_index(docs, chunks_by_doc)
        self.assertGreaterEqual(len(tax_index["taxonomy_categories"]), 7)

    def test_quick_classify_and_tracking_workflow(self) -> None:
        snippet = (
            "Rowhammer bit-flip fault injection in DRAM corrupts Vision Transformer "
            "weights on 28nm NPU accelerators without ECC."
        )
        info = classify_content(snippet, title="Rowhammer Faults in ViT NPUs")
        self.assertIn("Adversarial Fault Injection", info["technology_areas"])
        self.assertIn("Memory Subsystems & Chiplets", info["technology_areas"])
        concept_ids = {c["concept_id"] for c in info["matched_concepts"]}
        self.assertIn("concept:bit-flip-attack", concept_ids)
        self.assertIn("concept:ecc", concept_ids)
        self.assertIn("DRAM", info["candidate_terms"])

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            corpus_file = tmp_path / "corpus.json"
            out_dir = tmp_path / "output"

            # Add a new document via CLI
            rc = main(
                [
                    "add",
                    "--id",
                    "note-rowhammer-vit",
                    "--title",
                    "Rowhammer Faults in ViT NPUs",
                    "--type",
                    "note",
                    "--text",
                    snippet,
                    "--cites",
                    "arxiv-2610.08739v2",
                    "--status",
                    "reading",
                    "--priority",
                    "high",
                    "--tags",
                    "rowhammer,dram,vit",
                    "--corpus",
                    str(corpus_file),
                    "--output-dir",
                    str(out_dir),
                ]
            )
            self.assertEqual(rc, 0)
            docs = load_corpus(corpus_file)
            self.assertEqual(len(docs), 3)

            # Update status via CLI
            rc_stat = main(
                [
                    "status",
                    "note-rowhammer-vit",
                    "--set",
                    "read",
                    "--notes",
                    "Compare with BARE-AI APC overhead.",
                    "--corpus",
                    str(corpus_file),
                    "--output-dir",
                    str(out_dir),
                ]
            )
            self.assertEqual(rc_stat, 0)
            updated_docs = {d.doc_id: d for d in load_corpus(corpus_file)}
            self.assertEqual(updated_docs["note-rowhammer-vit"].reading_status, "read")
            self.assertEqual(
                updated_docs["note-rowhammer-vit"].notes,
                "Compare with BARE-AI APC overhead.",
            )

    def test_cli_build_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            artifacts = run_build(FIXTURE_PATH, out_dir)
            for path in artifacts.values():
                self.assertTrue(path.exists(), f"Missing artifact: {path}")
            kg_data = json.loads(
                artifacts["knowledge_graph"].read_text(encoding="utf-8")
            )
            self.assertGreater(kg_data["summary"]["node_count"], 20)
            self.assertGreater(kg_data["summary"]["edge_count"], 40)


if __name__ == "__main__":
    unittest.main()
