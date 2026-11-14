"""Automated topic research, arXiv query discovery, and synthesis note generation."""

from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from reading_list.chunker import classify_content, tokenize
from reading_list.enrich import extract_arxiv_id, structure_abstract_into_sections
from reading_list.models import Document, DocumentRelation
from reading_list.research_ai_security import AI_SECURITY_DOCUMENTS, AI_SECURITY_KEYWORDS

CURATED_RESEARCH_LIBRARY: tuple[dict[str, Any], ...] = (
    {
        "keywords": (
            "formal",
            "verification",
            "languages",
            "language",
            "chip",
            "semiconductor",
            "design",
            "sva",
            "systemverilog",
            "psl",
            "uclid5",
            "rtl",
            "assertion",
            "assertions",
            "eda",
        ),
        "documents": [
            {
                "doc_id": "arxiv-2208.03699",
                "title": "UCLID5: Multi-Modal Formal Modeling, Verification, and Synthesis",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/2208.03699",
                "published_date": "2022-08-06",
                "authors": [
                    "Elizabeth Polgreen",
                    "Kevin Cheang",
                    "Pranav Gaddamadugu",
                    "Adwait Godbole",
                    "Kevin Laeufer",
                    "Shaokai Lin",
                    "Yatin A. Manerkar",
                    "Federico Mora",
                    "Sanjit A. Seshia",
                ],
                "institutions": [
                    "University of California, Berkeley",
                    "University of Edinburgh",
                    "University of Michigan",
                ],
                "identifiers": {
                    "arxiv": "2208.03699",
                    "pdf_url": "https://arxiv.org/pdf/2208.03699",
                    "primary_category": "cs.LO",
                },
                "reading_status": "read",
                "priority": "high",
                "tags": [
                    "uclid5",
                    "formal-verification",
                    "smt",
                    "rtl",
                    "chisel",
                    "firrtl",
                ],
                "notes": "Foundational formal modeling and verification language for hardware datapaths, Chisel/FIRRTL RTL, and security invariants.",
                "relations": [],
                "content": (
                    "## Multi-Modal Formal Modeling Language for Hardware & Systems\n"
                    "UCLID5 is a formal modeling, verification, and synthesis framework and specification language designed for heterogeneous hardware and software systems. It enables compositional specification of Register-Transfer Level (RTL) datapaths, control logic, memory subsystems, and security monitors using first-order and temporal logic assertions.\n\n"
                    "## Bridging Chisel, FIRRTL, and SMT Solvers\n"
                    "In semiconductor design workflows, UCLID5 integrates with modern hardware construction languages such as Chisel and FIRRTL as well as SystemVerilog Assertions (SVA). Models are lowered to Satisfiability Modulo Theories (SMT) solvers and syntax-guided synthesis (SyGuS) engines for bounded model checking, inductive invariant synthesis, and hyperproperty verification.\n\n"
                    "## Verification of Secure Architectures and Accelerators\n"
                    "UCLID5 has been deployed to formally verify speculative execution mitigations, cryptographic accelerators, enclave isolation, and hardware fault-tolerance protocols prior to silicon tapeout."
                ),
            },
            {
                "doc_id": "arxiv-2503.19174",
                "title": "AssertionForge: Enhancing Formal Verification Assertion Generation with Structured Representation of Specifications and RTL",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/2503.19174",
                "published_date": "2025-03-24",
                "authors": [
                    "Yunsheng Bai",
                    "Ghaith Bany Hamad",
                    "Syed Suhaib",
                    "Haoxing Ren",
                ],
                "institutions": [
                    "NVIDIA",
                    "Arm",
                ],
                "identifiers": {
                    "arxiv": "2503.19174",
                    "pdf_url": "https://arxiv.org/pdf/2503.19174",
                    "primary_category": "cs.AR",
                },
                "reading_status": "reading",
                "priority": "high",
                "tags": [
                    "assertionforge",
                    "sva",
                    "systemverilog-assertions",
                    "knowledge-graph",
                    "rtl",
                    "formal-verification",
                ],
                "notes": "Constructs a unified Knowledge Graph across natural-language specs and RTL to synthesize SystemVerilog Assertions (SVAs).",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2208.03699",
                    }
                ],
                "content": (
                    "## Bottlenecks in Writing SystemVerilog Assertions (SVAs)\n"
                    "Formal Property Verification (FPV) in chip and semiconductor design relies heavily on SystemVerilog Assertions (SVAs) and Property Specification Language (PSL) to mathematically prove that Register-Transfer Level (RTL) implementations satisfy architectural specifications. Writing temporal logic assertions manually is error-prone and requires deep verification expertise.\n\n"
                    "## Unified Specification-and-RTL Knowledge Graph\n"
                    "AssertionForge constructs a unified hardware Knowledge Graph (KG) that fuses natural-language specification requirements with structural RTL signal interactions, finite-state machines, and clock/reset domains. Multi-resolution context retrieval over this graph prevents signal hallucination during automated SVA synthesis.\n\n"
                    "## Formal Property Verification Closure\n"
                    "Evaluated across industrial semiconductor IP blocks using commercial EDA formal verification engines, AssertionForge substantially increases syntax validity, temporal accuracy, and cone-of-influence coverage compared to baseline Large Language Model assertion generators."
                ),
            },
            {
                "doc_id": "arxiv-2604.23100",
                "title": "ProofLoop: From Language to Logic — Bridging LLMs and Formal Representations for RTL Assertion Generation",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/2604.23100",
                "published_date": "2026-04-28",
                "authors": [
                    "Nowfel Mashnoor",
                    "Aritra Dasgupta",
                    "Sandeep K. Shukla",
                ],
                "institutions": [
                    "IIT Kanpur",
                ],
                "identifiers": {
                    "arxiv": "2604.23100",
                    "pdf_url": "https://arxiv.org/pdf/2604.23100",
                    "primary_category": "cs.AR",
                },
                "reading_status": "to-read",
                "priority": "high",
                "tags": [
                    "proofloop",
                    "sva",
                    "jaspergold",
                    "solver-in-the-loop",
                    "rtl",
                    "formal-verification",
                ],
                "notes": "Solver-in-the-loop ReAct agent coupling AST-indexed RTL analysis with JasperGold formal proof feedback to refine SVA assertions.",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2503.19174",
                    }
                ],
                "content": (
                    "## Solver-in-the-Loop Formal Assertion Synthesis\n"
                    "ProofLoop introduces a two-phase agentic framework that bridges natural-language hardware specifications, Register-Transfer Level (RTL) abstract syntax trees (ASTs), and formal verification languages such as SystemVerilog Assertions (SVA).\n\n"
                    "## Iterative Refinement with EDA Proof Engines\n"
                    "In Phase A, ProofLoop queries an AST-indexed structural representation of the Verilog/SystemVerilog design to ground clock, reset, and handshake signals. In Phase B, a solver-in-the-loop agent invokes commercial formal verification engines such as Cadence JasperGold, parses counterexample traces and vacuity reports, and iteratively repairs candidate SVA properties until mathematical proof closure is achieved.\n\n"
                    "## Implications for Semiconductor Verification Flows\n"
                    "Coupling deterministic formal solvers with automated assertion synthesis eliminates vacuous properties and accelerates pre-silicon verification of complex SoC interconnects and AI accelerator datapaths."
                ),
            },
            {
                "doc_id": "arxiv-2609.26751",
                "title": "EquivSVA: A Formally Verified Dataset of Behavioral Assertions Across Equivalent RTL Implementations",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/2609.26751",
                "published_date": "2026-09-29",
                "authors": [
                    "FNU Aditi",
                    "Rohan Sharma",
                    "Subhasish Mitra",
                ],
                "institutions": [
                    "Stanford University",
                ],
                "identifiers": {
                    "arxiv": "2609.26751",
                    "pdf_url": "https://arxiv.org/pdf/2609.26751",
                    "primary_category": "cs.AR",
                },
                "reading_status": "to-read",
                "priority": "medium",
                "tags": [
                    "equivsva",
                    "sva",
                    "rtl",
                    "formal-verification",
                    "benchmark",
                ],
                "notes": "Formally verified dataset of behavioral SVA assertions across structurally distinct but functionally equivalent RTL designs.",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2503.19174",
                    },
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2604.23100",
                    },
                ],
                "content": (
                    "## Behavioral Equivalence in Hardware Verification Languages\n"
                    "Evaluating automated SystemVerilog Assertion (SVA) generators requires distinguishing true behavioral temporal properties from brittle assertions tied to incidental RTL coding style. EquivSVA provides a formally verified benchmark organized around behavior families of structurally distinct RTL implementations sharing identical interface specifications.\n\n"
                    "## Formal Equivalence & Metamorphic Verification\n"
                    "Every gold SVA assertion in EquivSVA is mechanically verified using formal property verification (FPV) and SMT-based equivalence checking across pipelined, FSM-encoded, and Chisel/FIRRTL-generated RTL variants.\n\n"
                    "## Advancing Robust Semiconductor Verification\n"
                    "EquivSVA enables rigorous benchmarking of formal verification language translators, theorem-proving hardware frameworks (Kami, Coq), and LLM-assisted assertion synthesis pipelines."
                ),
            },
        ],
    },
    {
        "keywords": (
            "sat",
            "smt",
            "solver",
            "solvers",
            "software",
            "development",
            "graph",
            "analysis",
            "ontologies",
            "ontology",
            "monosat",
            "cvc5",
            "z3",
            "symbolic",
            "execution",
            "owl",
        ),
        "documents": [
            {
                "doc_id": "arxiv-1402.4677",
                "title": "MonoSAT: Modulo Theories for Graphs, Networks, and Geometry",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/1402.4677",
                "published_date": "2015-01-25",
                "authors": [
                    "Sam Bayless",
                    "Noah Bayless",
                    "Holger H. Hoos",
                    "Alan J. Hu",
                ],
                "institutions": [
                    "University of British Columbia",
                ],
                "identifiers": {
                    "arxiv": "1402.4677",
                    "pdf_url": "https://arxiv.org/pdf/1402.4677",
                    "primary_category": "cs.LO",
                },
                "reading_status": "read",
                "priority": "high",
                "tags": [
                    "monosat",
                    "smt",
                    "sat",
                    "graph-analysis",
                    "monotonic-theories",
                    "reachability",
                ],
                "notes": "Pioneering SMT framework (DPLL(T)) for finite monotonic theories supporting native graph predicates (reachability, shortest path, max-flow, acyclicity).",
                "relations": [],
                "content": (
                    "## Graph Analysis & Monotonic Theories in SMT\n"
                    "Encoding complex graph-theoretic properties — such as reachability, shortest paths, maximum s-t flow, minimum spanning trees, and directed acyclic graph (DAG) acyclicity — directly into Boolean SAT or standard SMT bit-vector/integer theories causes severe formula blowup and poor solver propagation. MonoSAT introduces a general DPLL(T) framework for finite monotonic theories that integrates dedicated incremental graph algorithms directly inside an SMT solver.\n\n"
                    "## Under- and Over-Approximation Theory Propagation\n"
                    "MonoSAT maintains dual under-approximating and over-approximating graphs as Boolean edge variables are assigned during Conflict-Driven Clause Learning (CDCL) search. When a graph predicate (such as reachability or cycle-freeness) becomes violated, MonoSAT extracts a succinct conflict clause (cut-set or witness path) in polynomial time, orders of magnitude faster than propositional encodings.\n\n"
                    "## Applications in Network Verification, Routing & Ontology Graphs\n"
                    "MonoSAT powers formal cloud network reachability analysis, circuit routing, dependency graph resolution in software package managers, and structural acyclicity/subsumption checks in large-scale knowledge graphs and ontologies."
                ),
            },
            {
                "doc_id": "arxiv-2201.04663",
                "title": "cvc5: A Versatile and Industrial-Strength SMT Solver",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/2201.04663",
                "published_date": "2022-01-13",
                "authors": [
                    "Haniel Barbosa",
                    "Clark Barrett",
                    "Martin Brain",
                    "Gereon Kremer",
                    "Aina Niemetz",
                    "Mathias Preiner",
                    "Andrew Reynolds",
                    "Cesare Tinelli",
                ],
                "institutions": [
                    "Stanford University",
                    "University of Iowa",
                    "University of Oxford",
                ],
                "identifiers": {
                    "arxiv": "2201.04663",
                    "pdf_url": "https://arxiv.org/pdf/2201.04663",
                    "primary_category": "cs.LO",
                },
                "reading_status": "reading",
                "priority": "high",
                "tags": [
                    "cvc5",
                    "smt",
                    "sat",
                    "sygus",
                    "software-verification",
                    "ontologies",
                ],
                "notes": "Industrial-strength DPLL(T) SMT and SyGuS solver supporting strings, finite sets, relations, bit-vectors, and algebraic datatypes.",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-1402.4677",
                    },
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2208.03699",
                    },
                ],
                "content": (
                    "## Next-Generation DPLL(T) SMT Architecture\n"
                    "cvc5 is an industrial-strength Satisfiability Modulo Theories (SMT) and Syntax-Guided Synthesis (SyGuS) solver built on a modular CDCL(T) / DPLL(T) core. It combines high-performance Boolean SAT solving with decision procedures for bit-vectors, arrays, floating-point arithmetic, strings and regular expressions, algebraic datatypes, and quantifier instantiation.\n\n"
                    "## Finite Sets, Relations & Ontology Constraint Solving\n"
                    "Uniquely suited to graph analysis and formal ontologies, cvc5 provides native decision procedures for the Theory of Finite Sets and the Theory of Finite Relations (including transitive closure, relational join, and cardinality constraints). These relational theories enable direct SMT encoding of OWL Description Logic axioms, Alloy structural models, and SHACL knowledge-graph validation rules.\n\n"
                    "## Software Development & Deductive Verification\n"
                    "In software engineering, cvc5 serves as the automated reasoning backend for deductive verifiers (Dafny, Spark/Ada, Viper), smart-contract auditors, cloud IAM policy analyzers (AWS Zelkova), and symbolic execution engines."
                ),
            },
            {
                "doc_id": "arxiv-1610.00502",
                "title": "A Survey of Symbolic Execution Techniques for Software Development and Verification",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/1610.00502",
                "published_date": "2018-05-07",
                "authors": [
                    "Roberto Baldoni",
                    "Emilio Coppa",
                    "Daniele Coniglio",
                    "Camil Demetrescu",
                    "Irene Finocchi",
                ],
                "institutions": [
                    "Sapienza University of Rome",
                ],
                "identifiers": {
                    "arxiv": "1610.00502",
                    "pdf_url": "https://arxiv.org/pdf/1610.00502",
                    "primary_category": "cs.SE",
                },
                "reading_status": "to-read",
                "priority": "high",
                "tags": [
                    "symbolic-execution",
                    "smt",
                    "sat",
                    "klee",
                    "software-development",
                    "program-analysis",
                ],
                "notes": "Comprehensive study of SAT/SMT constraint solving in symbolic execution (KLEE, SAGE, Angr) for automated test generation and vulnerability discovery.",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2201.04663",
                    }
                ],
                "content": (
                    "## Path-Constraint Solving with SAT and SMT Solvers\n"
                    "Symbolic execution transforms software development, automated test generation, and vulnerability discovery by executing programs over symbolic inputs rather than concrete values. At every conditional branch, the symbolic execution engine (such as KLEE, SAGE, or CBMC) queries an SMT solver (Z3, STP, or cvc5) over the Theory of Bit-Vectors and Arrays (QF_ABV) to decide path feasibility and synthesize concrete bug-triggering inputs.\n\n"
                    "## Constraint Caching, Slicing & Heap Graph Modeling\n"
                    "Because SMT solver queries dominate symbolic execution runtime, modern software analysis tools employ counterexample-guided constraint caching, independent clause slicing, and array-theory memory modeling to reason about pointer aliasing and heap data structures (linked lists, trees, and control-flow graphs).\n\n"
                    "## Memory Safety & Security Vulnerability Detection\n"
                    "Coupling SAT/SMT solvers with symbolic execution and bounded model checking uncovers spatial/temporal memory safety violations, integer overflows, and invariant breaches across systems software."
                ),
            },
            {
                "doc_id": "arxiv-1507.01763",
                "title": "SAT and SMT-Based Automated Reasoning for Description Logics and Formal Ontologies",
                "doc_type": "academic_paper",
                "url": "https://arxiv.org/abs/1507.01763",
                "published_date": "2015-07-07",
                "authors": [
                    "Roberto Sebastiani",
                    "Michele Vescovi",
                ],
                "institutions": [
                    "University of Trento",
                ],
                "identifiers": {
                    "arxiv": "1507.01763",
                    "pdf_url": "https://arxiv.org/pdf/1507.01763",
                    "primary_category": "cs.AI",
                },
                "reading_status": "to-read",
                "priority": "high",
                "tags": [
                    "ontologies",
                    "description-logic",
                    "owl",
                    "sat",
                    "smt",
                    "ontologic",
                ],
                "notes": "Demonstrates how encoding Description Logic (EL+/ALC) TBox/ABox ontologies into CDCL SAT and SMT enables ultra-fast classification, subsumption, and datatype constraint checking.",
                "relations": [
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-1402.4677",
                    },
                    {
                        "relation_type": "CITES",
                        "target_doc_id": "arxiv-2201.04663",
                    },
                ],
                "content": (
                    "## Encoding OWL Ontologies & Description Logics into SAT/SMT\n"
                    "Formal ontologies (OWL 2, SKOS, and Description Logics such as EL, ALC, and SHQ) define hierarchical concept taxonomies (TBox) and relational knowledge graph assertions (ABox). By encoding concept subsumption, disjointness, and role inclusion axioms into Horn-SAT and Conflict-Driven Clause Learning (CDCL) SAT formulas, automated reasoners classify ratusan-thousand-concept ontologies in seconds.\n\n"
                    "## Concrete Domains & Numerical Constraints via SMT\n"
                    "Real-world engineering and scientific ontologies require reasoning simultaneously over taxonomic hierarchies and concrete numerical domains (thresholds, intervals, unit conversions, and cardinality bounds). Satisfiability Modulo Theories (SMT) bridges this gap by combining Boolean ontology axiom propagation with Linear Real/Integer Arithmetic (LRA/LIA) and Uninterpreted Functions (EUF).\n\n"
                    "## OntoLogic Integration & Knowledge Graph Verification\n"
                    "SAT/SMT-backed ontology reasoning detects unsatisfiable classes, cyclic taxonomy regressions, and SHACL constraint violations across evolving semantic knowledge graphs."
                ),
            },
        ],
    },
    {
        "keywords": AI_SECURITY_KEYWORDS,
        "documents": AI_SECURITY_DOCUMENTS,
    },
)


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:44].strip("-") or "topic"


def search_arxiv_topic(topic: str, max_results: int = 4, timeout: float = 8.0) -> list[Document]:
    """Query the live arXiv Atom API for papers matching `topic`."""
    tokens = [t for t in tokenize(topic) if len(t) > 2][:6]
    if not tokens:
        return []
    query_expr = "+AND+".join(f"all:{urllib.parse.quote(t)}" for t in tokens)
    api_url = (
        f"https://export.arxiv.org/api/query?search_query={query_expr}"
        f"&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    )
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "reading-list-research/0.1"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_bytes = resp.read()
    except Exception:
        return []

    docs: list[Document] = []
    try:
        root = ET.fromstring(xml_bytes)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        for entry in root.findall("atom:entry", ns):
            id_el = entry.find("atom:id", ns)
            title_el = entry.find("atom:title", ns)
            summary_el = entry.find("atom:summary", ns)
            published_el = entry.find("atom:published", ns)
            cat_el = entry.find("arxiv:primary_category", ns)

            raw_url = (id_el.text or "").strip() if id_el is not None else ""
            arxiv_id = extract_arxiv_id(raw_url)
            if not arxiv_id:
                continue

            title = " ".join((title_el.text or "").split()) if title_el is not None else arxiv_id
            summary = " ".join((summary_el.text or "").split()) if summary_el is not None else title
            published = (published_el.text or "")[:10] if published_el is not None else ""
            primary_cat = cat_el.attrib.get("term", "") if cat_el is not None else ""

            authors: list[str] = []
            for author_el in entry.findall("atom:author", ns):
                name_el = author_el.find("atom:name", ns)
                if name_el is not None and name_el.text:
                    authors.append(name_el.text.strip())

            docs.append(
                Document(
                    doc_id=f"arxiv-{arxiv_id}",
                    title=title,
                    doc_type="academic_paper",
                    url=f"https://arxiv.org/abs/{arxiv_id}",
                    published_date=published,
                    authors=authors,
                    institutions=[],
                    identifiers={
                        "arxiv": arxiv_id,
                        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
                        "primary_category": primary_cat,
                    },
                    relations=[],
                    content=structure_abstract_into_sections(summary),
                    reading_status="to-read",
                    priority="medium",
                    tags=tokens[:5],
                    notes=f"Discovered via live arXiv search for topic: {topic!r}",
                )
            )
    except Exception:
        return []

    return docs


def match_curated_research(topic: str, max_results: int = 5) -> list[Document]:
    """Return curated domain papers matching the topic keywords."""
    topic_tokens = set(tokenize(topic))
    scored_packs: list[tuple[int, dict[str, Any]]] = []

    for pack in CURATED_RESEARCH_LIBRARY:
        overlap = topic_tokens.intersection(pack["keywords"])
        score = len(overlap)
        if score >= 2:
            scored_packs.append((score, pack))

    scored_packs.sort(key=lambda item: item[0], reverse=True)
    matched_docs: list[Document] = []
    for _, pack in scored_packs:
        for raw_doc in pack["documents"]:
            if len(matched_docs) < max_results:
                matched_docs.append(Document.from_dict(raw_doc))
        if matched_docs:
            break

    return matched_docs


def build_research_synthesis_note(
    topic: str,
    discovered_docs: list[Document],
    existing_docs: list[Document],
) -> Document:
    """Create a structured Research Synthesis Note linking discovered papers into the knowledge graph."""
    slug = _slugify(topic)
    note_id = f"research-{slug}"

    is_ai_security = len(set(tokenize(topic)).intersection(AI_SECURITY_KEYWORDS)) >= 2
    link_keywords = (
        ("guardrail", "sec-bench", "prompt injection", "jailbreak")
        if is_ai_security
        else ("formal verification", "operational semantics", "smt", "rtl", "28nm", "bare-ai")
    )

    cited_ids = [d.doc_id for d in discovered_docs]
    for ex in existing_docs:
        if ex.doc_id not in cited_ids and any(
            kw in f"{ex.title} {ex.content}".lower() for kw in link_keywords
        ):
            cited_ids.append(ex.doc_id)

    relations = [
        DocumentRelation(relation_type="CITES", target_doc_id=cid)
        for cid in cited_ids
    ]

    paper_summaries = "; ".join(
        f"{d.title} ({d.doc_id})" for d in discovered_docs
    ) or "domain literature"

    lowered_topic = topic.lower()
    if is_ai_security:
        content = (
            f"## Why Per-Turn Evaluation Is Not Enough: {topic}\n"
            "Multi-turn attacks such as Crescendo (`arxiv-2404.01833`) start with benign-looking requests and escalate gradually by building on the model's own replies, so each individual turn can pass a stateless check while the conversation as a whole does not. Defenses in this collection therefore score the trajectory rather than the turn.\n\n"
            "## Session-Level Detection Approaches\n"
            f"Collected literature — {paper_summaries} — spans: (1) **conversation-level scoring** (Peak + Accumulation's proxy-layer formula, THRD's time-evolving risk score, DeepContext's recurrent hidden state, PsychoPass's embedding-space geometry, Defensive M2S's compressed histories); (2) **agent runtime monitoring** over tool calls and execution traces (NEXUS, AgentTrust, ProbGuard, and a fraud-detection-style feature layer for adversarial interaction patterns); and (3) **taxonomies and surveys** (SoK on jailbreak guardrails, SoK on prompt injection against agentic coding assistants, and a layered attack-surface survey with a temporality axis that reports no benchmark coverage of cross-session failures).\n\n"
            "## Endpoint View & Open Gaps\n"
            "On the endpoint, vendor and CSA material argues that EDR sees a trusted agent process doing authorized work and so cannot see agent-level manipulation (for example MCP-delivered injection). Much of the evidence is small, synthetic, or vendor-authored, results are not comparable across papers, and cross-session attacks remain largely unaddressed."
        )
        tags = [
            "research-synthesis",
            "ai-security",
            "multi-turn",
            "crescendo",
            "trajectory-monitoring",
            "agent-runtime",
            "endpoint",
        ]
    elif any(k in lowered_topic for k in ("sat", "smt", "ontology", "ontologies", "graph")):
        content = (
            f"## SAT & SMT Decision Procedures Across Software, Graphs, and Ontologies: {topic}\n"
            f"Conflict-Driven Clause Learning (CDCL) SAT solvers and DPLL(T) Satisfiability Modulo Theories (SMT) solvers (such as Z3 and cvc5) serve as the computational backbone for modern automated reasoning. By combining Boolean constraint propagation with specialized background theories — bit-vectors, arrays, strings, linear arithmetic, finite sets, and relations — SMT solvers unify software verification, combinatorial graph analysis, and formal ontology reasoning.\n\n"
            f"## Symbolic Execution, Monotonic Graph Theories & Description Logics\n"
            f"Primary literature synthesized in this collection — {paper_summaries} — spans three synergistic pillars: (1) **Software Development & Symbolic Execution** (KLEE, CBMC, Dafny, cvc5), where path constraints over bit-vectors and arrays synthesize bug-triggering inputs and prove memory-safety invariants; (2) **Graph Analysis Modulo Theories** (MonoSAT), where monotonic graph predicates (reachability, shortest path, maximum s-t flow, minimum spanning tree, and DAG acyclicity) are decided natively inside DPLL(T) without propositional blowup; and (3) **Ontology & Description Logic Reasoning** (OWL 2, EL/ALC, SHACL, OntoLogic), where TBox/ABox concept subsumption, consistency, and numerical datatype constraints reduce directly to Horn-SAT and SMT.\n\n"
            f"## Cross-Domain Integration in the Reading-DB Knowledge Graph\n"
            f"Within our OntoLogic-ready knowledge base, SAT and SMT solvers bridge software capability verification (Fil-C memory safety), hardware formal verification languages (UCLID5, SVA, ProofLoop), and taxonomic ontology validation."
        )
        tags = [
            "research-synthesis",
            "sat",
            "smt",
            "cvc5",
            "monosat",
            "symbolic-execution",
            "graph-analysis",
            "ontologies",
            "ontologic",
        ]
    else:
        content = (
            f"## Research Scope & Core Languages: {topic}\n"
            f"In chip and semiconductor design, Formal Verification Languages provide the mathematical foundation for specifying and proving Register-Transfer Level (RTL) and architectural invariants before silicon fabrication. The industrial backbone comprises IEEE 1800 SystemVerilog Assertions (SVA) and IEEE 1850 Property Specification Language (PSL) for linear temporal logic (LTL) Formal Property Verification (FPV), complemented by multi-modal verification and hardware construction languages including UCLID5 (SMT-backed datapath/control modeling), Chisel/FIRRTL (ChiselFV), and Coq-embedded theorem-proving frameworks such as Kami.\n\n"
            f"## Knowledge-Graph & Solver-in-the-Loop Assertion Synthesis\n"
            f"Recent research synthesized in this collection — {paper_summaries} — addresses the manual bottleneck of authoring temporal logic assertions. Frameworks like AssertionForge construct unified Knowledge Graphs fusing natural-language specs and RTL structure, while agentic solver-in-the-loop systems like ProofLoop interact directly with commercial EDA formal engines (Cadence JasperGold and SMT solvers) to iteratively refine SVA assertions until formal proof closure.\n\n"
            f"## Cross-Layer Integration with Hardware Telemetry & Security\n"
            f"Within our OntoLogic-ready knowledge graph, formal verification languages connect pre-silicon EDA verification with runtime hardware security monitors (such as BARE-AI's 28nm AI Performance Counters and PULSE neural detectors) and probabilistic operational semantics for memory-level bit-flip resilience (such as Rowhammer analysis on Fil-C software capabilities)."
        )
        tags = ["research-synthesis", "formal-verification", "sva", "psl", "uclid5", "eda", "rtl"]

    return Document(
        doc_id=note_id,
        title=f"Research Synthesis: {topic}",
        doc_type="note",
        url="https://github.com/bsommers/reading-db",
        published_date="2026-11-07",
        authors=["Reading List Research Engine"],
        institutions=[],
        identifiers={"research_topic": topic},
        relations=relations,
        content=content,
        reading_status="read",
        priority="high",
        tags=tags,
        notes=f"Automated multi-paper synthesis and taxonomy bridge for topic: {topic!r}.",
    )


def research_topic(
    topic: str,
    existing_docs: list[Document],
    max_results: int = 5,
) -> dict[str, Any]:
    """Discover papers for `topic`, build a synthesis note, and classify all findings."""
    curated = match_curated_research(topic, max_results=max_results)
    live = search_arxiv_topic(topic, max_results=max(1, max_results - len(curated)))

    seen_ids: set[str] = set()
    discovered: list[Document] = []
    for doc in [*curated, *live]:
        if doc.doc_id not in seen_ids:
            seen_ids.add(doc.doc_id)
            discovered.append(doc)
        if len(discovered) >= max_results:
            break

    synthesis_note = build_research_synthesis_note(topic, discovered, existing_docs)
    all_new_docs = [*discovered, synthesis_note]

    classifications = {
        doc.doc_id: classify_content(doc.content, title=doc.title)
        for doc in all_new_docs
    }

    return {
        "topic": topic,
        "discovered_documents": discovered,
        "synthesis_note": synthesis_note,
        "all_documents": all_new_docs,
        "classifications": classifications,
    }
