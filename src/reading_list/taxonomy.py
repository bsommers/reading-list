"""Conceptual taxonomy hierarchy, technology areas, and concept catalog."""

from __future__ import annotations

import re

from reading_list.models import ConceptDefinition, TaxonomyNode

TAXONOMY_NODES: tuple[TaxonomyNode, ...] = (
    TaxonomyNode(
        path="Hardware & Semiconductor Systems",
        label="Hardware & Semiconductor Systems",
        parent_path=None,
        technology_area="Semiconductor Engineering",
        keywords=(
            "hardware",
            "chip",
            "semiconductor",
            "28nm",
            "silicon",
            "asic",
            "fpga",
            "area",
            "energy",
            "datapath",
            "rtl",
            "soc",
        ),
        description="Integrated circuits, semiconductor manufacturing nodes, and hardware architectures.",
        ontologic_class_uri="ontologic:HardwareSemiconductorSystems",
    ),
    TaxonomyNode(
        path="Hardware & Semiconductor Systems > AI Accelerators",
        label="AI Accelerators",
        parent_path="Hardware & Semiconductor Systems",
        technology_area="AI Hardware Accelerators",
        keywords=(
            "accelerator",
            "accelerators",
            "datapath",
            "on-chip",
            "neural engine",
            "systolic",
            "npu",
            "tpu",
            "inference",
        ),
        description="Specialized hardware datapaths and neural engines for executing AI workloads.",
        ontologic_class_uri="ontologic:AIAccelerators",
    ),
    TaxonomyNode(
        path="Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
        label="Built-in Performance Monitors",
        parent_path="Hardware & Semiconductor Systems > AI Accelerators",
        technology_area="On-Chip Telemetry & Runtime Monitoring",
        keywords=(
            "performance monitors",
            "performance counters",
            "apcs",
            "monitors",
            "pulse",
            "activation statistics",
            "sparsity",
            "entropy",
            "kurtosis",
            "spectral shift",
            "telemetry",
        ),
        description="Lightweight on-chip telemetry counters and runtime monitors integrated into accelerator datapaths.",
        ontologic_class_uri="ontologic:BuiltInPerformanceMonitors",
    ),
    TaxonomyNode(
        path="Hardware & Semiconductor Systems > Memory & Interconnects",
        label="Memory & Interconnects",
        parent_path="Hardware & Semiconductor Systems",
        technology_area="Memory Subsystems & Chiplets",
        keywords=(
            "dram",
            "sram",
            "ddr3",
            "ddr4",
            "trr",
            "target row refresh",
            "hbm",
            "non-volatile",
            "nvm",
            "rowhammer",
            "chiplet",
            "interconnect",
            "ucie",
            "cxl",
            "memory",
        ),
        description="On-package memory, DRAM/SRAM subsystems, and die-to-die interconnects.",
        ontologic_class_uri="ontologic:MemoryAndInterconnects",
    ),
    TaxonomyNode(
        path="Hardware & Semiconductor Systems > EDA & Hardware Verification",
        label="EDA & Hardware Verification",
        parent_path="Hardware & Semiconductor Systems",
        technology_area="Electronic Design Automation",
        keywords=(
            "synthesized",
            "synthesis",
            "eda",
            "verification",
            "place and route",
            "timing",
            "formal verification",
            "operational semantics",
            "simulation",
        ),
        description="Electronic design automation, logic synthesis, formal semantics, and verification.",
        ontologic_class_uri="ontologic:EDAAndVerification",
    ),
    TaxonomyNode(
        path="Security & Resilience",
        label="Security & Resilience",
        parent_path=None,
        technology_area="Hardware & AI Security",
        keywords=(
            "security",
            "vulnerable",
            "vulnerability",
            "defenses",
            "resilience",
            "safety critical",
            "attacks",
            "attack",
            "threat",
            "adversarial",
            "privilege escalation",
        ),
        description="System security, adversarial threat modeling, and fault resilience.",
        ontologic_class_uri="ontologic:SecurityAndResilience",
    ),
    TaxonomyNode(
        path="Security & Resilience > Hardware Fault Attacks > Bit-Flip Attacks",
        label="Bit-Flip Attacks",
        parent_path="Security & Resilience",
        technology_area="Adversarial Fault Injection",
        keywords=(
            "bit-flip",
            "bit-flip attacks",
            "bfas",
            "perturbations",
            "targeted flips",
            "memory level",
            "fault injection",
            "rowhammer",
            "laser fault",
        ),
        description="Memory-level bit-flip perturbations (including Rowhammer) that corrupt weights or pointer metadata.",
        ontologic_class_uri="ontologic:BitFlipAttacks",
    ),
    TaxonomyNode(
        path="Security & Resilience > Memory Safety & Software Capabilities",
        label="Memory Safety & Software Capabilities",
        parent_path="Security & Resilience",
        technology_area="Language & Runtime Memory Safety",
        keywords=(
            "fil-c",
            "invisicaps",
            "software capabilities",
            "memory safety",
            "spatial",
            "temporal",
            "bounds-checking",
            "out-of-bounds",
            "pointer",
        ),
        description="Compiler and runtime memory-safety mechanisms, capability pointers, and bounds metadata.",
        ontologic_class_uri="ontologic:MemorySafetySoftwareCapabilities",
    ),
    TaxonomyNode(
        path="Security & Resilience > Runtime Fault Localization & Recovery",
        label="Runtime Fault Localization & Recovery",
        parent_path="Security & Resilience",
        technology_area="Self-Healing & Fault-Tolerant AI",
        keywords=(
            "localizes",
            "mitigates",
            "localization",
            "recovery",
            "repair",
            "activation shift index",
            "asi",
            "z-score",
            "error correcting codes",
            "ecc",
            "fault tolerance",
        ),
        description="Online anomaly localization and statistical weight repair without full model retraining.",
        ontologic_class_uri="ontologic:RuntimeFaultLocalizationRecovery",
    ),
    TaxonomyNode(
        path="Artificial Intelligence & Machine Learning",
        label="Artificial Intelligence & Machine Learning",
        parent_path=None,
        technology_area="AI & Machine Learning",
        keywords=(
            "machine learning",
            "artificial intelligence",
            "neural",
            "classifier",
            "classifiers",
            "ensemble",
            "retraining",
            "inference",
        ),
        description="Machine learning models, training/inference pipelines, and statistical algorithms.",
        ontologic_class_uri="ontologic:ArtificialIntelligenceMachineLearning",
    ),
    TaxonomyNode(
        path="Artificial Intelligence & Machine Learning > Deep Neural Networks",
        label="Deep Neural Networks",
        parent_path="Artificial Intelligence & Machine Learning",
        technology_area="Deep Learning Architectures",
        keywords=(
            "deep neural networks",
            "dnns",
            "cnns",
            "vision transformers",
            "vits",
            "large language models",
            "llms",
            "weights",
            "layer",
            "transformer",
        ),
        description="Deep neural network architectures including CNNs, Vision Transformers, and Large Language Models.",
        ontologic_class_uri="ontologic:DeepNeuralNetworks",
    ),
)

CONCEPT_CATALOG: tuple[ConceptDefinition, ...] = (
    ConceptDefinition(
        concept_id="concept:bare-ai",
        label="BARE-AI Framework",
        taxonomy_path="Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
        technology_area="On-Chip Telemetry & Runtime Monitoring",
        surface_forms=("bare-ai", "bit-flip attack resilience in ai hardware"),
        related_concepts=("concept:apc", "concept:pulse", "concept:asi", "concept:bit-flip-attack"),
        description="Runtime framework that detects, localizes, and mitigates bit-flip attacks during AI inference.",
    ),
    ConceptDefinition(
        concept_id="concept:bit-flip-attack",
        label="Bit-Flip Attack (BFA)",
        taxonomy_path="Security & Resilience > Hardware Fault Attacks > Bit-Flip Attacks",
        technology_area="Adversarial Fault Injection",
        surface_forms=(
            "bit-flip",
            "bit-flip attack",
            "bit-flip attacks",
            "bfa",
            "bfas",
            "targeted flips",
            "memory level perturbations",
            "rowhammer",
        ),
        related_concepts=("concept:bare-ai", "concept:dnn", "concept:rowhammer"),
        description="Adversarial or fault-induced memory perturbations that flip bits in neural network weights or runtime metadata.",
    ),
    ConceptDefinition(
        concept_id="concept:rowhammer",
        label="Rowhammer DRAM Disturbance Attack",
        taxonomy_path="Security & Resilience > Hardware Fault Attacks > Bit-Flip Attacks",
        technology_area="Adversarial Fault Injection",
        surface_forms=("rowhammer", "target row refresh", "trr", "ddr3", "ddr4"),
        related_concepts=("concept:bit-flip-attack", "concept:fil-c", "concept:ecc"),
        description="Physical DRAM disturbance errors induced by rapid row activations that flip bits in adjacent rows.",
    ),
    ConceptDefinition(
        concept_id="concept:fil-c",
        label="Fil-C Software Capabilities (InvisiCaps)",
        taxonomy_path="Security & Resilience > Memory Safety & Software Capabilities",
        technology_area="Language & Runtime Memory Safety",
        surface_forms=("fil-c", "invisicaps", "software capabilities", "upper-bound word"),
        related_concepts=("concept:rowhammer", "concept:bit-flip-attack"),
        description="Memory-safe C/C++ implementation using DRAM-backed software capabilities (InvisiCaps) checked on pointer dereferences.",
    ),
    ConceptDefinition(
        concept_id="concept:apc",
        label="AI Performance Counters (APCs)",
        taxonomy_path="Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
        technology_area="On-Chip Telemetry & Runtime Monitoring",
        surface_forms=(
            "ai performance counters",
            "apcs",
            "performance monitors",
            "on-chip monitors",
            "hardware monitors",
        ),
        related_concepts=("concept:bare-ai", "concept:pulse", "concept:activation-statistics"),
        description="Lightweight hardware monitors in the accelerator datapath capturing per-layer activation statistics.",
    ),
    ConceptDefinition(
        concept_id="concept:pulse",
        label="PULSE Detector",
        taxonomy_path="Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
        technology_area="On-Chip Telemetry & Runtime Monitoring",
        surface_forms=(
            "pulse",
            "predictive unit for layer security evaluation",
            "ensemble of classifiers",
            "small neural engine",
        ),
        related_concepts=("concept:bare-ai", "concept:apc"),
        description="Compact on-chip neural detector trained as an ensemble of classifiers to evaluate APC layer telemetry.",
    ),
    ConceptDefinition(
        concept_id="concept:asi",
        label="Activation Shift Index (ASI)",
        taxonomy_path="Security & Resilience > Runtime Fault Localization & Recovery",
        technology_area="Self-Healing & Fault-Tolerant AI",
        surface_forms=(
            "activation shift index",
            "asi",
            "fault localization",
            "z-score based repair",
        ),
        related_concepts=("concept:bare-ai", "concept:activation-statistics"),
        description="Metric for layer-level fault localization paired with z-score weight repair.",
    ),
    ConceptDefinition(
        concept_id="concept:activation-statistics",
        label="Layer Activation Statistics",
        taxonomy_path="Hardware & Semiconductor Systems > AI Accelerators > Built-in Performance Monitors",
        technology_area="On-Chip Telemetry & Runtime Monitoring",
        surface_forms=("activation statistics", "sparsity", "entropy", "kurtosis", "spectral shift"),
        related_concepts=("concept:apc", "concept:asi"),
        description="Statistical moments and spectral properties of per-layer neural activations captured at runtime.",
    ),
    ConceptDefinition(
        concept_id="concept:dnn",
        label="Deep Neural Networks (DNNs, ViTs, LLMs)",
        taxonomy_path="Artificial Intelligence & Machine Learning > Deep Neural Networks",
        technology_area="Deep Learning Architectures",
        surface_forms=(
            "deep neural networks",
            "dnns",
            "cnns",
            "vision transformers",
            "vits",
            "large language models",
            "llms",
        ),
        related_concepts=("concept:bit-flip-attack", "concept:ai-accelerator"),
        description="Neural network families evaluated for resilience against bit-flip perturbations.",
    ),
    ConceptDefinition(
        concept_id="concept:ai-accelerator",
        label="AI Hardware Accelerator",
        taxonomy_path="Hardware & Semiconductor Systems > AI Accelerators",
        technology_area="AI Hardware Accelerators",
        surface_forms=("ai accelerators", "ai hardware", "accelerator datapath", "28nm"),
        related_concepts=("concept:apc", "concept:bare-ai", "concept:dnn"),
        description="Integrated circuit accelerators synthesized for neural network inference.",
    ),
    ConceptDefinition(
        concept_id="concept:ecc",
        label="Error Correcting Codes (ECC)",
        taxonomy_path="Security & Resilience > Runtime Fault Localization & Recovery",
        technology_area="Self-Healing & Fault-Tolerant AI",
        surface_forms=("error correcting codes", "ecc"),
        related_concepts=("concept:bit-flip-attack", "concept:bare-ai", "concept:rowhammer"),
        description="Hardware memory redundancy codes whose overhead scales with the number of tolerated bit flips.",
    ),
)

_ACRONYM_PATTERN = re.compile(r"\b[A-Z][A-Z0-9-]{1,12}s?\b")
_HYPHEN_TECH_PATTERN = re.compile(r"\b[a-zA-Z0-9]+-[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\b")


def match_concepts(text: str) -> list[ConceptDefinition]:
    """Return all canonical concepts whose surface forms appear in `text`."""
    lowered = text.lower()
    matched: list[ConceptDefinition] = []
    for concept in CONCEPT_CATALOG:
        if any(form in lowered for form in concept.surface_forms):
            matched.append(concept)
    return matched


def extract_candidate_concepts(text: str) -> list[str]:
    """Extract technical acronyms and compound terms not already covered or useful for quick tagging."""
    candidates: set[str] = set()
    for match in _ACRONYM_PATTERN.finditer(text):
        token = match.group(0)
        if token not in {"II", "III", "IV", "URL", "PDF", "HTTP", "HTTPS"}:
            candidates.add(token)
    for match in _HYPHEN_TECH_PATTERN.finditer(text):
        token = match.group(0).lower()
        if len(token) >= 4:
            candidates.add(token)
    return sorted(candidates)


def classify_taxonomy(
    text: str,
    matched_concepts: list[ConceptDefinition],
) -> tuple[list[str], list[str]]:
    """Assign hierarchical taxonomy paths and technology areas to a text segment."""
    lowered = text.lower()
    paths: set[str] = {c.taxonomy_path for c in matched_concepts}
    tech_areas: set[str] = {c.technology_area for c in matched_concepts}

    for node in TAXONOMY_NODES:
        if any(kw in lowered for kw in node.keywords):
            paths.add(node.path)
            tech_areas.add(node.technology_area)

    # Ensure ancestor paths in the hierarchy are also represented for tree navigation
    node_by_path = {n.path: n for n in TAXONOMY_NODES}
    expanded_paths = set(paths)
    for path in list(paths):
        curr = node_by_path.get(path)
        while curr and curr.parent_path:
            expanded_paths.add(curr.parent_path)
            if curr.parent_path in node_by_path:
                tech_areas.add(node_by_path[curr.parent_path].technology_area)
            curr = node_by_path.get(curr.parent_path)

    return sorted(expanded_paths), sorted(tech_areas)
