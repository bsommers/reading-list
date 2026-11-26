"""Curated research pack: secure execution enclaves, non-speculative enclave execution,
linear address spaces & linear capabilities, and zero-trust blast chambers in hardened custom OSes.
"""

from __future__ import annotations

from typing import Any

ENCLAVES_OS_KEYWORDS: tuple[str, ...] = (
    "enclave",
    "enclaves",
    "linear",
    "address",
    "space",
    "non-speculative",
    "speculative",
    "blast",
    "chamber",
    "chambers",
    "zero-trust",
    "hardened",
    "operating",
    "system",
    "sasos",
    "single-address-space",
    "capstone",
    "sanctum",
    "mi6",
    "prospect",
    "cherios",
    "redleaf",
    "theseus",
)

ENCLAVES_OS_DOCUMENTS: list[dict[str, Any]] = [
    {
        "doc_id": "usenix-2016-sanctum",
        "title": "Sanctum: Minimal Hardware Extensions for Strong Software Isolation",
        "doc_type": "academic_paper",
        "url": "https://eprint.iacr.org/2015/564",
        "published_date": "2016-08-10",
        "authors": [
            "Victor Costan",
            "Ilia Lebedev",
            "Srinivas Devadas",
        ],
        "institutions": [
            "Massachusetts Institute of Technology",
        ],
        "identifiers": {
            "iacr_eprint": "2015/564",
            "venue": "USENIX Security 2016",
            "usenix_url": "https://www.usenix.org/conference/usenixsecurity16/technical-sessions/presentation/costan",
        },
        "reading_status": "read",
        "priority": "high",
        "tags": [
            "sanctum",
            "secure-enclaves",
            "riscv",
            "cache-partitioning",
            "dram-regions",
            "security-monitor",
            "formal-isolation",
        ],
        "notes": "Foundational open-hardware (RISC-V Rocket) secure execution enclave architecture eliminating page-fault and LLC cache-timing side channels via DRAM region bitmasks and per-enclave page tables.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "arxiv-2208.03699",
            }
        ],
        "content": (
            "## Threat Model & Limitations of Commercial Enclaves\n"
            "Commercial Trusted Execution Environments (TEEs) such as Intel SGX protect enclave memory against direct reads and writes from a compromised operating system or hypervisor, but leave enclaves exposed to software side-channel attacks through shared Last-Level Cache (LLC) sets and OS-observable page-fault address traces. Sanctum introduces minimal, non-invasive hardware extensions to a RISC-V processor core (outside the main execution pipeline) coupled with a tiny, formally verifiable M-mode security monitor (<5,000 LoC).\n\n"
            "## Contiguous DRAM Regions, Cache Index Shifting & Per-Enclave Page Tables\n"
            "Sanctum partitions physical DRAM into equal-sized contiguous DRAM regions whose bit-slice maps directly to LLC cache sets. By assigning exclusive DRAM region bitmasks to each enclave and maintaining separate hardware page-table walker base pointers (`EPTBR` vs. OS `PTBR`) inside the enclave itself, Sanctum guarantees that an untrusted OS cannot observe enclave page faults or induce cross-domain LLC cache evictions.\n\n"
            "## Foundation for Non-Speculative Enclave Proofs\n"
            "On an in-order core, Sanctum achieves provable constant-time and trace-oblivious isolation against a malicious kernel; it directly serves as the baseline architectural contract later extended to out-of-order speculative pipelines by MI6 (`arxiv-1812.09822`)."
        ),
    },
    {
        "doc_id": "arxiv-1812.09822",
        "title": "MI6: Secure Enclaves in a Speculative Out-of-Order Processor",
        "doc_type": "academic_paper",
        "url": "https://arxiv.org/abs/1812.09822",
        "published_date": "2018-12-24",
        "authors": [
            "Thomas Bourgeat",
            "Ilia Lebedev",
            "Andrew Wright",
            "Sizhuo Zhang",
            "Arvind",
            "Srinivas Devadas",
        ],
        "institutions": [
            "Massachusetts Institute of Technology",
        ],
        "identifiers": {
            "arxiv": "1812.09822",
            "pdf_url": "https://arxiv.org/pdf/1812.09822",
            "primary_category": "cs.AR",
            "venue": "MICRO 2019",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "mi6",
            "secure-enclaves",
            "non-speculative",
            "speculative-execution",
            "out-of-order",
            "purge-instruction",
            "riscv",
        ],
        "notes": "Proves that speculative execution breaks traditional enclave isolation and introduces hardware non-speculative cross-domain memory gates plus the microarchitectural `purge` instruction on an out-of-order RISC-V processor.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "usenix-2016-sanctum",
            },
            {
                "relation_type": "CITES",
                "target_doc_id": "arxiv-2208.03699",
            },
        ],
        "content": (
            "## Why Speculative Execution Breaks Enclave Isolation\n"
            "On modern out-of-order speculative processors, transient instructions fetched along mispredicted branches can speculatively issue loads to unauthorized physical addresses or modulate shared microarchitectural structures (L1 data/instruction caches, TLBs, MSHRs, branch predictors, and arithmetic functional units) before the Reorder Buffer (ROB) squash occurs. Even when DRAM and Last-Level Caches are partitioned as in Sanctum, speculative execution leaks enclave secrets across protection boundaries.\n\n"
            "## Enforcing Non-Speculative Boundaries & the `purge` Instruction\n"
            "MI6 co-designs an out-of-order speculative RISC-V processor (`RiscyOO`) and secure enclave monitor to restore rigorous formal isolation. First, MI6 enforces **non-speculative capability/range checks at protection boundaries**: speculative loads and stores are hardware-blocked from crossing out of the active enclave's allocated DRAM region bitmap, preventing transient cross-domain reads. Second, MI6 introduces a hardware `purge` instruction executed on every enclave entry/exit and context switch that deterministically flushes all core-local microarchitectural state (L1 caches, TLBs, branch history tables, BTB, RSB, and in-flight MSHRs).\n\n"
            "## Formal Indistinguishability & Performance Trade-off\n"
            "MI6 satisfies a machine-checked trace-indistinguishability security definition — guaranteeing that no speculative execution inside or outside the enclave can transmit information across enclave boundaries — with an average runtime overhead of 16.6% compared to turning off speculation entirely."
        ),
    },
    {
        "doc_id": "arxiv-2302.12108",
        "title": "ProSpeCT: Provably Secure Speculation for the Constant-Time Policy",
        "doc_type": "academic_paper",
        "url": "https://arxiv.org/abs/2302.12108",
        "published_date": "2023-02-23",
        "authors": [
            "Lesly-Ann Daniel",
            "Márton Bognár",
            "Job Noorman",
            "Sébastien Bardin",
            "Tamara Rezk",
            "Frank Piessens",
        ],
        "institutions": [
            "KU Leuven",
            "Université Paris-Saclay (CEA List)",
            "Inria",
        ],
        "identifiers": {
            "arxiv": "2302.12108",
            "pdf_url": "https://arxiv.org/pdf/2302.12108",
            "primary_category": "cs.CR",
            "venue": "USENIX Security 2023",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "prospect",
            "non-speculative",
            "speculative-execution",
            "constant-time",
            "secure-enclaves",
            "riscv",
            "taint-tracking",
        ],
        "notes": "Hardware-software co-design on an out-of-order RISC-V processor that enforces strictly non-speculative execution for secret-tainted enclave data while allowing public data to execute speculatively at full speed.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "arxiv-1812.09822",
            }
        ],
        "content": (
            "## Selective Non-Speculative Execution Inside Enclaves\n"
            "Completely disabling speculative execution inside a secure enclave eliminates Spectre-class transient execution attacks at the cost of severe throughput degradation, whereas coarse fence insertion (`lfence`) is error-prone and incomplete. ProSpeCT introduces a formal hardware-software contract where enclave memory pages or linear address ranges are classified as either *secret* or *public*, and the processor pipeline tracks dynamic secret taint across registers.\n\n"
            "## Blocking Speculative Secret Propagation in the Pipeline\n"
            "Whenever an instruction in the out-of-order execution window consumes a secret-tainted operand or performs a secret-dependent memory access, branch, or variable-time arithmetic operation, ProSpeCT's hardware control logic delays any microarchitecturally observable side effect until the instruction becomes **non-speculative** (i.e., all older branches, exceptions, and address translations in the Reorder Buffer are resolved). Public control-flow and non-secret calculations continue to speculate at full out-of-order speed.\n\n"
            "## Provable Constant-Time Enclave Guarantees on RISC-V\n"
            "Implemented on a speculative out-of-order RISC-V core (BOOM/Proteus), ProSpeCT proves that any enclave binary satisfying standard sequential constant-time discipline remains 100% immune to speculative leakage with near-zero performance penalty on cryptographic and enclave workloads."
        ),
    },
    {
        "doc_id": "arxiv-2302.13863",
        "title": "Capstone: A Capability-Based Foundation for Trustless Secure Memory Access",
        "doc_type": "academic_paper",
        "url": "https://arxiv.org/abs/2302.13863",
        "published_date": "2023-02-27",
        "authors": [
            "Jason Zhijingcheng Yu",
            "Conrad Watt",
            "Aditya Badole",
            "Trevor E. Carlson",
            "Prateek Saxena",
        ],
        "institutions": [
            "National University of Singapore",
            "University of Cambridge",
        ],
        "identifiers": {
            "arxiv": "2302.13863",
            "pdf_url": "https://arxiv.org/pdf/2302.13863",
            "primary_category": "cs.CR",
            "venue": "USENIX Security 2023",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "capstone",
            "linear-capabilities",
            "linear-address-space",
            "secure-enclaves",
            "zero-trust",
            "cheri",
            "riscv",
        ],
        "notes": "Introduces hardware-enforced linear capabilities (move-only, non-aliasing pointers) and revocation trees over a flat linear address space, enabling zero-trust enclaves and blast chambers without a trusted OS kernel or hypervisor.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "usenix-2016-sanctum",
            },
            {
                "relation_type": "CITES",
                "target_doc_id": "arxiv-1812.09822",
            },
        ],
        "content": (
            "## From Copyable Capabilities to Hardware Linear Capabilities\n"
            "Traditional hardware capability architectures (such as CHERI) enforce spatial bounds within a linear address space, but allow capabilities to be duplicated arbitrarily. Because any duplicated capability creates an alias, enforcing exclusive memory ownership for secure enclaves or revoking access across mutually distrusting domains requires trusting a privileged OS kernel or sweeping all of physical memory. Capstone introduces **linear capabilities**—hardware-tagged pointers governed by linear logic that can be *moved* between registers or memory locations, *split* into disjoint sub-intervals, or *transferred* across domain transitions, but **never copied**.\n\n"
            "## Alias-Free Exclusive Enclaves in a Flat Linear Address Space\n"
            "Because a linear capability is guaranteed by the processor ISA not to alias with any other capability in the entire flat linear address space, holding a linear capability proves exclusive read/write access to that memory slice. Paired with hardware revocation trees (`mrev`) and sealed domain-invocation capabilities (`dom`), Capstone allows any compartment to spawn a zero-trust secure execution enclave or temporary blast chamber, delegate a linear memory buffer to it, and deterministically revoke access upon return—without relying on page tables or trusting the host operating system.\n\n"
            "## Unified Substrate for Enclaves, Safe Allocators & OS Compartments\n"
            "Prototyped on RISC-V, Capstone demonstrates six composable isolation models in a single linear address space without a trusted kernel: mutually distrusting enclaves, nested sandboxes, preemptive thread scheduling, safe shared-memory zero-copy IPC, and hardware-enforced Rust-style borrow checking."
        ),
    },
    {
        "doc_id": "cambridge-2021-cherios-sasos",
        "title": "CheriOS: Designing an Untrusted Single-Address-Space Capability Operating System",
        "doc_type": "academic_paper",
        "url": "https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-961.pdf",
        "published_date": "2021-09-01",
        "authors": [
            "Lawrence G. Esswood",
            "Robert N. M. Watson",
            "Simon W. Moore",
            "Peter G. Neumann",
        ],
        "institutions": [
            "University of Cambridge",
            "SRI International",
        ],
        "identifiers": {
            "tech_report": "UCAM-CL-TR-961",
            "url": "https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-961.html",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "cherios",
            "single-address-space",
            "sasos",
            "linear-address-space",
            "cheri",
            "capabilities",
            "zero-trust",
            "blast-chambers",
        ],
        "notes": "Complete Single-Address-Space Operating System (SASOS) where all OS services, drivers, and user tasks share one flat linear address space and isolate every subsystem in capability-bounded zero-trust blast chambers.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "usenix-2016-sanctum",
            },
            {
                "relation_type": "CITES",
                "target_doc_id": "fil-c-2025-invisicaps",
            },
        ],
        "content": (
            "## Decoupling Address Translation from Protection in a Linear Address Space\n"
            "Conventional operating systems conflate virtual address translation with memory protection by placing each process in a separate page-table hierarchy, incurring steep TLB shootdown, context-switch, and serialization costs when decomposing an OS into fine-grained zero-trust compartments. CheriOS implements a pure **Single-Address-Space Operating System (SASOS)** where all tasks, device drivers, file systems, network stacks, and nanokernel routines execute inside a single global linear virtual address space.\n\n"
            "## Zero-Trust Compartments & Temporal Quarantine Blast Chambers\n"
            "In CheriOS, numeric integers cannot be dereferenced as pointers; every memory instruction requires an unforgeable hardware capability encoding exact base, length, permissions, and object-type seal. Every OS service and untrusted parser runs inside an isolated compartment ('blast chamber') holding only the minimal capabilities passed to it. Temporal memory safety is enforced via a hardware-accelerated quarantine bitmap that sweeps revoked heap regions before capability reuse.\n\n"
            "## Zero-Copy Cross-Domain Invocations Without Trusted Kernel Mediation\n"
            "Because all compartments share the same linear address space, cross-domain RPC passes bounded capabilities in registers rather than copying buffers through a monolithic kernel, achieving order-of-magnitude faster compartmentalized I/O even when the OS services themselves are mutually untrusted."
        ),
    },
    {
        "doc_id": "usenix-osdi20-redleaf",
        "title": "RedLeaf: Isolation and Communication in a Safe Operating System",
        "doc_type": "academic_paper",
        "url": "https://www.usenix.org/conference/osdi20/presentation/narayanan-vikram",
        "published_date": "2020-11-04",
        "authors": [
            "Vikram Narayanan",
            "Tianjiao Huang",
            "David Detweiler",
            "Dan Appel",
            "Zhaofeng Li",
            "Gerd Zellweger",
            "Anton Burtsev",
        ],
        "institutions": [
            "University of California, Irvine",
            "VMware Research",
        ],
        "identifiers": {
            "venue": "USENIX OSDI 2020",
            "isbn": "978-1-939133-19-9",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "redleaf",
            "blast-chambers",
            "zero-trust",
            "linear-address-space",
            "single-address-space",
            "rust-os",
            "fault-isolation",
        ],
        "notes": "Custom operating system in Rust running in a single flat linear address space without hardware page-table switches, isolating device drivers and kernel extensions inside recoverable zero-trust blast chambers.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "cambridge-2021-cherios-sasos",
            }
        ],
        "content": (
            "## Zero-Trust Blast Chambers in a Single Linear Address Space\n"
            "RedLeaf is a custom operating system designed from scratch in Rust that abandons hardware page-table isolation in favor of a **single flat linear address space** shared across the microkernel, device drivers, and user domains. To ensure that a panic, vulnerability, or Byzantine fault in an untrusted subsystem cannot corrupt the rest of the system, RedLeaf encapsulates each component inside a lightweight **fault-isolation domain (blast chamber)**.\n\n"
            "## Linear Ownership Transfer (`RRef<T>`) & Shared-Heap Isolation\n"
            "Memory safety alone does not provide fault isolation if crashing domains leave shared data structures in inconsistent states or hold dangling pointers. RedLeaf enforces a strict invariant: domains never share mutable references directly. Cross-domain communication over the flat linear address space occurs exclusively via `RRef<T>`—linearly owned heap objects allocated on an exchange heap whose ownership is moved atomically across domain boundaries with zero data copying.\n\n"
            "## Sub-Microsecond Blast Containment & Transparent Recovery\n"
            "Every cross-domain invocation traverses an automatically generated compiler proxy that returns an explicit `RpcResult<T>`. When a blast chamber faults or violates an invariant, the RedLeaf nanokernel unwinds and reclaims only that domain's heap and linear `RRef` objects in microseconds, restarting high-throughput NVMe and 10GbE IXGBE driver domains transparently without dropping adjacent OS sessions."
        ),
    },
    {
        "doc_id": "usenix-osdi20-theseus",
        "title": "Theseus: An Experiment in Operating System Structure and State Management",
        "doc_type": "academic_paper",
        "url": "https://www.usenix.org/conference/osdi20/presentation/boos",
        "published_date": "2020-11-04",
        "authors": [
            "Kevin Boos",
            "Namitha Liyanage",
            "Ramla Ijaz",
            "Lin Zhong",
        ],
        "institutions": [
            "Rice University",
            "Yale University",
        ],
        "identifiers": {
            "venue": "USENIX OSDI 2020",
            "isbn": "978-1-939133-19-9",
        },
        "reading_status": "to-read",
        "priority": "high",
        "tags": [
            "theseus",
            "single-address-space",
            "linear-address-space",
            "blast-chambers",
            "zero-trust",
            "intralingual-os",
            "state-spill-freedom",
        ],
        "notes": "Custom single-address-space, single-privilege-level operating system built from dozens of cell-level blast chambers with bijective linear virtual-to-physical mappings (`MappedPages`) and zero state spill.",
        "relations": [
            {
                "relation_type": "CITES",
                "target_doc_id": "usenix-osdi20-redleaf",
            },
            {
                "relation_type": "CITES",
                "target_doc_id": "cambridge-2021-cherios-sasos",
            },
        ],
        "content": (
            "## Single-Address-Space Intralingual OS Architecture\n"
            "Theseus is a custom hardened operating system executing entirely within a **single flat linear virtual address space** and a single hardware privilege level (Ring 0), decomposed into dozens of fine-grained, dynamically linked software cells. Instead of relying on expensive hardware rings or nested page tables, Theseus pushes isolation and resource lifecycle management into the compiler's linear/affine type system.\n\n"
            "## Bijective Linear Address Mappings (`MappedPages`) & State-Spill Freedom\n"
            "At the foundation of Theseus's linear address space is `MappedPages`, a linear type guaranteeing a strict one-to-one bijection between virtual address ranges and physical frames—making double-mapping, aliasing, use-after-unmap, and bounds violations impossible at compile time. Furthermore, Theseus enforces **state-spill freedom**: no cell stores hidden bookkeeping state on behalf of another cell, turning every cell into a self-contained zero-trust blast chamber.\n\n"
            "## Live Blast-Chamber Unwinding & Hot-Swapping\n"
            "When an exception or fault occurs inside any kernel or application cell, Theseus deterministically unwinds that cell's stack and linearly owned `MappedPages` resources, replaces or restarts the cell in place, and resumes execution without corrupting neighboring cells in the shared linear address space."
        ),
    },
]
