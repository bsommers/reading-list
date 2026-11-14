"""Curated AI-security research pack: multi-turn escalation, trajectory monitoring, and endpoint agent security.

Paper metadata (titles, authors, dates, abstracts) was taken from the arXiv abstract pages on
2026-11-13. Web-source notes record what was actually read; see each note's ``notes`` field.
"""

from __future__ import annotations

from typing import Any

AI_SECURITY_KEYWORDS: tuple[str, ...] = (
    "security",
    "jailbreak",
    "jailbreaks",
    "crescendo",
    "multi-turn",
    "escalation",
    "trajectory",
    "trajectories",
    "session",
    "sessions",
    "agent",
    "agents",
    "endpoint",
    "mcp",
    "injection",
    "guardrail",
    "guardrails",
)

AI_SECURITY_DOCUMENTS: list[dict[str, Any]] = [{'authors': ['Mark Russinovich', 'Ahmed Salem', 'Ronen Eldan'],
  'content': '## Problem Statement & Context\n'
             'Large Language Models (LLMs) have risen significantly in popularity and are '
             'increasingly being adopted across multiple applications. These LLMs are heavily '
             'aligned to resist engaging in illegal or unethical topics as a means to avoid '
             'contributing to responsible AI harms. However, a recent line of attacks, known as '
             'jailbreaks, seek to overcome this alignment. Intuitively, jailbreak attacks aim to '
             'narrow the gap between what the model can do and what it is willing to do.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'In this paper, we introduce a novel jailbreak attack called Crescendo. Unlike '
             'existing jailbreak methods, Crescendo is a simple multi-turn jailbreak that '
             'interacts with the model in a seemingly benign manner. It begins with a general '
             'prompt or question about the task at hand and then gradually escalates the dialogue '
             "by referencing the model's replies progressively leading to a successful jailbreak. "
             'We evaluate Crescendo on various public systems, including ChatGPT, Gemini Pro, '
             'Gemini-Ultra, LlaMA-2 70b and LlaMA-3 70b Chat, and Anthropic Chat.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'Our results demonstrate the strong efficacy of Crescendo, with it achieving high '
             'attack success rates across all evaluated models and tasks. Furthermore, we present '
             'Crescendomation, a tool that automates the Crescendo attack and demonstrate its '
             'efficacy against state-of-the-art models through our evaluations. Crescendomation '
             'surpasses other state-of-the-art jailbreaking techniques on the AdvBench subset '
             'dataset, achieving 29-61% higher performance on GPT-4 and 49-71% on Gemini-Pro. '
             "Finally, we also demonstrate Crescendo's ability to jailbreak multimodal models.",
  'doc_id': 'arxiv-2404.01833',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2404.01833',
                  'pdf_url': 'https://arxiv.org/pdf/2404.01833',
                  'primary_category': 'cs.CR'},
  'institutions': [],
  'notes': 'Primary attack paper: the benign-looking, gradually escalating multi-turn jailbreak '
           '(Crescendo) and its automated variant Crescendomation. Defenses in this pack are '
           'largely motivated by it. Metadata verified from the arXiv abstract page on 2026-11-13.',
  'priority': 'high',
  'published_date': '2024-04-02',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['crescendo', 'multi-turn', 'jailbreak', 'red-teaming', 'ai-security'],
  'title': 'Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack',
  'url': 'https://arxiv.org/abs/2404.01833'},
 {'authors': ['Xunguang Wang',
              'Zhenlan Ji',
              'Wenxuan Wang',
              'Zongjie Li',
              'Daoyuan Wu',
              'Shuai Wang'],
  'content': '## Problem Statement & Context\n'
             'Large Language Models (LLMs) have achieved remarkable progress, but their deployment '
             'has exposed critical vulnerabilities, particularly to jailbreak attacks that '
             'circumvent safety alignments. Guardrails--external defense mechanisms that monitor '
             'and control LLM interactions--have emerged as a promising solution.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'However, the current landscape of LLM guardrails is fragmented, lacking a unified '
             'taxonomy and comprehensive evaluation framework. In this Systematization of '
             'Knowledge (SoK) paper, we present the first holistic analysis of jailbreak '
             'guardrails for LLMs.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'We propose a novel, multi-dimensional taxonomy that categorizes guardrails along six '
             'key dimensions, and introduce a Security-Efficiency-Utility evaluation framework to '
             'assess their practical effectiveness. Through extensive analysis and experiments, we '
             'identify the strengths and limitations of existing guardrail approaches, provide '
             'insights into optimizing their defense mechanisms, and explore their universality '
             'across attack types. Our work offers a structured foundation for future research and '
             'development, aiming to guide the principled advancement and deployment of robust LLM '
             'guardrails. The code is available at '
             'https://github.com/xunguangwang/SoK4JailbreakGuardrails.',
  'doc_id': 'arxiv-2506.10597',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2506.10597', 'pdf_url': 'https://arxiv.org/pdf/2506.10597'},
  'institutions': [],
  'notes': 'SoK on jailbreak guardrails: six-dimension taxonomy and a Security-Efficiency-Utility '
           'evaluation framework. Background reference for comparing guardrail approaches. '
           'Metadata verified from the arXiv abstract page on 2026-11-13.',
  'priority': 'medium',
  'published_date': '2025-06-12',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['guardrails', 'jailbreak', 'sok', 'taxonomy', 'ai-security'],
  'title': 'SoK: Evaluating Jailbreak Guardrails for Large Language Models',
  'url': 'https://arxiv.org/abs/2506.10597'},
 {'authors': ['Haoyu Wang', 'Christopher M. Poskitt', 'Jiali Wei', 'Jun Sun'],
  'content': '## Problem Statement & Context\n'
             'Large Language Model (LLM) agents increasingly operate across domains such as '
             'robotics, virtual assistants, and web automation. However, their stochastic '
             'decision-making introduces safety risks that are difficult to anticipate during '
             'execution. Existing runtime monitoring frameworks, such as AgentSpec, primarily rely '
             'on reactive safety rules that detect violations only when unsafe behavior is '
             'imminent or has already occurred, limiting their ability to handle long-horizon '
             'dependencies.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We present ProbGuard, a proactive runtime monitoring framework for LLM agents that '
             'anticipates safety violations through probabilistic risk prediction. ProbGuard '
             'abstracts agent executions into symbolic states and learns a Discrete-Time Markov '
             'Chain (DTMC) from execution traces to model behavioral dynamics. At runtime, the '
             'monitor estimates the probability that execution will remain safe from the current '
             'state, and triggers an intervention when this probability falls below a user-defined '
             'threshold.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'To improve robustness, ProbGuard incorporates semantic validity constraints in the '
             'abstraction and admits a PAC-style analysis that characterizes the sample complexity '
             'required to certify the learned model under standard assumptions. We evaluate '
             'ProbGuard in two safety-critical domains: autonomous driving and embodied household '
             'agents. Across evaluated scenarios, ProbGuard consistently predicts traffic law '
             'violations and collisions in advance, with warnings up to 15.84 seconds at a '
             'threshold yielding no false alarms, and up to 38.66 seconds at stricter thresholds. '
             "In embodied agent tasks, ProbGuard's re-prompting intervention mode reduces unsafe "
             'behavior by 65.37% relative to the unmonitored baseline while retaining 80.4% of the '
             'baseline task completion; a stricter halting configuration reduces unsafe behavior '
             'by 93.60% at a larger cost in completion.',
  'doc_id': 'arxiv-2508.00500',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2508.00500', 'pdf_url': 'https://arxiv.org/pdf/2508.00500'},
  'institutions': [],
  'notes': 'Evaluated on autonomous driving and embodied household agents, not on chat or '
           'security-conversation traces. Relevant here as a trajectory-prediction technique (DTMC '
           'over abstracted execution states). Metadata verified from the arXiv abstract page on '
           '2026-11-13.',
  'priority': 'medium',
  'published_date': '2025-08-01',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['agent-runtime', 'runtime-monitoring', 'markov-chain', 'proactive', 'ai-security'],
  'title': 'ProbGuard: Proactive Runtime Monitoring for LLM Agent Safety via Probabilistic '
           'Prediction',
  'url': 'https://arxiv.org/abs/2508.00500'},
 {'authors': ['Hyunjun Kim'],
  'content': '## Problem Statement & Context\n'
             'Guardrail models are essential for ensuring the safety of Large Language Model (LLM) '
             'deployments, but processing full multi-turn conversation histories incurs '
             'significant computational cost. We propose Defensive M2S, a training paradigm that '
             'fine-tunes guardrail models on Multi-turn to Single-turn (M2S) compressed '
             'conversations rather than complete dialogue histories. We provide a formal '
             'complexity analysis showing that M2S reduces training cost from $O(n^2)$ to $O(n)$ '
             'for $n$-turn conversations.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'Empirically, on our training dataset (779 samples, avg. 10.6 turns), M2S requires '
             'only 169K tokens compared to 15.7M tokens for the multi-turn baseline -- a '
             '93$\\times$ reduction. We evaluate Defensive M2S across three guardrail model '
             'families (LlamaGuard, Nemotron, Qwen3Guard) and three compression templates '
             '(hyphenize, numberize, pythonize) on SafeDialBench, a comprehensive multi-turn '
             'jailbreak benchmark.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'Our best configuration, Qwen3Guard with hyphenize compression, achieves 93.8% attack '
             'detection recall while reducing inference tokens by 94.6% (from 3,231 to 173 tokens '
             'per conversation). This represents a 38.9 percentage point improvement over the '
             'baseline while dramatically reducing both training and inference costs. Our findings '
             'demonstrate that M2S compression can serve as an effective efficiency technique for '
             'guardrail deployment, enabling scalable safety screening of long multi-turn '
             'conversations.',
  'doc_id': 'arxiv-2601.00454',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2601.00454', 'pdf_url': 'https://arxiv.org/pdf/2601.00454'},
  'institutions': [],
  'notes': 'Compresses multi-turn history to single-turn for guardrail training and inference '
           '(efficiency angle). Single-author; results on SafeDialBench. Metadata verified from '
           'the arXiv abstract page on 2026-11-13.',
  'priority': 'medium',
  'published_date': '2026-01-01',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['multi-turn', 'guardrails', 'efficiency', 'jailbreak-detection', 'ai-security'],
  'title': 'Defensive M2S: Training Guardrail Models on Compressed Multi-turn Conversations',
  'url': 'https://arxiv.org/abs/2601.00454'},
 {'authors': ['Narek Maloyan', 'Dmitry Namiot'],
  'content': '## Problem Statement & Context\n'
             'The proliferation of agentic AI coding assistants, including Claude Code, GitHub '
             'Copilot, Cursor, and emerging skill-based architectures, has fundamentally '
             'transformed software development workflows. These systems leverage Large Language '
             'Models (LLMs) integrated with external tools, file systems, and shell access through '
             'protocols like the Model Context Protocol (MCP). However, this expanded capability '
             'surface introduces critical security vulnerabilities.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'In this \\textbf{Systematization of Knowledge (SoK)} paper, we present a '
             'comprehensive analysis of prompt injection attacks targeting agentic coding '
             'assistants. We propose a novel three-dimensional taxonomy categorizing attacks '
             'across \\textit{delivery vectors}, \\textit{attack modalities}, and '
             '\\textit{propagation behaviors}. Our meta-analysis synthesizes findings from 78 '
             'recent studies (2021--2026), consolidating evidence that attack success rates '
             'against state-of-the-art defenses exceed 85\\% when adaptive attack strategies are '
             'employed.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'We systematically catalog 42 distinct attack techniques spanning input manipulation, '
             'tool poisoning, protocol exploitation, multimodal injection, and cross-origin '
             'context poisoning. Through critical analysis of 18 defense mechanisms reported in '
             'prior work, we identify that most achieve less than 50\\% mitigation against '
             'sophisticated adaptive attacks. We contribute: (1) a unified taxonomy bridging '
             'disparate attack classifications, (2) the first systematic analysis of skill-based '
             'architecture vulnerabilities with concrete exploit chains, and (3) a '
             'defense-in-depth framework grounded in the limitations we identify. Our findings '
             'indicate that the security community must treat prompt injection as a first-class '
             'vulnerability class requiring architectural-level mitigations rather than ad-hoc '
             'filtering approaches.',
  'doc_id': 'arxiv-2601.17548',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2601.17548', 'pdf_url': 'https://arxiv.org/pdf/2601.17548'},
  'institutions': [],
  'notes': 'SoK meta-analysis (78 studies, 42 attack techniques, 18 defenses). Figures are the '
           "authors' consolidation of prior work, not new measurements. Metadata verified from the "
           'arXiv abstract page on 2026-11-13.',
  'priority': 'high',
  'published_date': '2026-01-24',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['prompt-injection', 'coding-agents', 'mcp', 'endpoint', 'sok', 'ai-security'],
  'title': 'Prompt Injection Attacks on Agentic Coding Assistants: A Systematic Analysis of '
           'Vulnerabilities in Skills, Tools, and Protocol Ecosystems',
  'url': 'https://arxiv.org/abs/2601.17548'},
 {'authors': ['J Alex Corll'],
  'content': '## Problem Statement & Context\n'
             'Multi-turn prompt injection attacks distribute malicious intent across multiple '
             'conversation turns, exploiting the assumption that each turn is evaluated '
             'independently. While single-turn detection has been extensively studied, no '
             'published formula exists for aggregating per-turn pattern scores into a '
             'conversation-level risk score at the proxy layer -- without invoking an LLM.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We identify a fundamental flaw in the intuitive weighted-average approach: it '
             'converges to the per-turn score regardless of turn count, meaning a 20-turn '
             'persistent attack scores identically to a single suspicious turn. Drawing on '
             'analogies from change-point detection (CUSUM), Bayesian belief updating, and '
             'security risk-based alerting, we propose peak + accumulation scoring -- a formula '
             'combining peak single-turn risk, persistence ratio, and category diversity.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'Evaluated on 10,654 multi-turn conversations -- 588 attacks sourced from '
             'WildJailbreak adversarial prompts and 10,066 benign conversations from WildChat -- '
             'the formula achieves 90.8% recall at 1.20% false positive rate with an F1 of 85.9%. '
             'A sensitivity analysis over the persistence parameter reveals a phase transition at '
             'rho ~ 0.4, where recall jumps 12 percentage points with negligible FPR increase. We '
             'release the scoring algorithm, pattern library, and evaluation harness as open '
             'source.',
  'doc_id': 'arxiv-2602.11247',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2602.11247', 'pdf_url': 'https://arxiv.org/pdf/2602.11247'},
  'institutions': [],
  'notes': 'Single-author. Practical, LLM-free conversation-level scoring formula for a proxy; '
           'shows why a weighted average fails to catch persistent attacks. Dataset: WildJailbreak '
           'attacks vs WildChat benign. Metadata verified from the arXiv abstract page on '
           '2026-11-13.',
  'priority': 'high',
  'published_date': '2026-02-11',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['multi-turn', 'trajectory-monitoring', 'risk-scoring', 'proxy-layer', 'ai-security'],
  'title': 'Peak + Accumulation: A Proxy-Level Scoring Formula for Multi-Turn LLM Attack Detection',
  'url': 'https://arxiv.org/abs/2602.11247'},
 {'authors': ['Justin Albrethsen', 'Yash Datta', 'Kunal Kumar', 'Sharath Rajasekar'],
  'content': '## Problem Statement & Context\n'
             'While Large Language Model (LLM) capabilities have scaled, safety guardrails remain '
             'largely stateless, treating multi-turn dialogues as a series of disconnected events. '
             'This lack of temporal awareness facilitates a "Safety Gap" where adversarial '
             'tactics, like Crescendo and ActorAttack, slowly bleed malicious intent across turn '
             'boundaries to bypass stateless filters.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We introduce DeepContext, a stateful monitoring framework designed to map the '
             'temporal trajectory of user intent. DeepContext discards the isolated evaluation '
             'model in favor of a Recurrent Neural Network (RNN) architecture that ingests a '
             'sequence of fine-tuned turn-level embeddings.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'By propagating a hidden state across the conversation, DeepContext captures the '
             'incremental accumulation of risk that stateless models overlook. Our evaluation '
             'demonstrates that DeepContext significantly outperforms existing baselines in '
             'multi-turn jailbreak detection, achieving a state-of-the-art F1 score of 0.84, which '
             'represents a substantial improvement over both hyperscaler cloud-provider guardrails '
             'and leading open-weight models such as Llama-Prompt-Guard-2 (0.67) and '
             'Granite-Guardian (0.67). Furthermore, DeepContext maintains a sub-20ms inference '
             'overhead on a T4 GPU, ensuring viability for real-time applications. These results '
             'suggest that modeling the sequential evolution of intent is a more effective and '
             'computationally efficient alternative to deploying massive, stateless models.',
  'doc_id': 'arxiv-2602.16935',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2602.16935', 'pdf_url': 'https://arxiv.org/pdf/2602.16935'},
  'institutions': [],
  'notes': 'Stateful (RNN over turn embeddings) detector for Crescendo/ActorAttack-style intent '
           'drift; reports F1 0.84 vs 0.67 for Llama-Prompt-Guard-2 and Granite-Guardian with '
           'sub-20ms overhead on a T4. Metadata verified from the arXiv abstract page on '
           '2026-11-13.',
  'priority': 'high',
  'published_date': '2026-02-18',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['multi-turn', 'trajectory-monitoring', 'intent-drift', 'stateful', 'rnn', 'ai-security'],
  'title': 'DeepContext: Stateful Real-Time Detection of Multi-Turn Adversarial Intent Drift in '
           'LLMs',
  'url': 'https://arxiv.org/abs/2602.16935'},
 {'authors': ['Kexin Chu'],
  'content': '## Problem Statement & Context\n'
             'Agentic AI systems introduce a security surface that is qualitatively different from '
             'that of stateless LLMs. They persist memory, invoke external tools, coordinate with '
             'peer agents, and operate across sessions, allowing attacks to emerge not only at the '
             'prompt interface but also through architectural state, delegated authority, and '
             'long-horizon interactions. Existing security taxonomies, however, primarily organize '
             'threats by attack type, such as prompt injection or jailbreaking, and therefore '
             'obscure where in the agentic stack a threat arises and over what timescale it '
             'manifests.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We propose the Layered Attack Surface Model (\\lasm), a structural taxonomy for '
             'agentic AI security. \\lasm decomposes the agentic stack into seven layers -- '
             'Foundation, Cognitive, Memory, Tool Execution, Multi-Agent Coordination, Ecosystem, '
             'and Governance -- and augments them with a four-class temporality axis covering '
             'instantaneous, session-persistent, cross-session cumulative, and sub-session-stack '
             'threats. We use this 7$\\times$4 framework to analyze 116 papers from 2021--2026.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'The resulting map reveals that the upper layers of the agentic stack remain sharply '
             'under-explored, especially for long-horizon and stack-propagating threats; multiple '
             'documented attack regions have no corresponding defenses; and current benchmarks '
             'provide no coverage for cross-session or sub-session-stack failure modes. We further '
             'derive a cross-layer defense taxonomy, defense recipes for canonical attack classes, '
             'and a dependency DAG that separates near-term engineering gaps from fundamental '
             'research challenges. We release the per-paper coding, robustness scripts, and a '
             'reference Agent Bill of Materials schema to support reproducible analysis.',
  'doc_id': 'arxiv-2604.23338',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2604.23338', 'pdf_url': 'https://arxiv.org/pdf/2604.23338'},
  'institutions': [],
  'notes': 'Layered Attack Surface Model: 7 layers x 4 temporalities (instantaneous, '
           'session-persistent, cross-session cumulative, sub-session-stack) over 116 papers. '
           'Reports that benchmarks give no coverage of cross-session or sub-session-stack '
           'failures. Metadata verified from the arXiv abstract page on 2026-11-13.',
  'priority': 'medium',
  'published_date': '2026-04-25',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['agent-security', 'survey', 'taxonomy', 'cross-session', 'memory', 'ai-security'],
  'title': 'A Systematic Survey of Security Threats and Defenses in LLM-Based AI Agents: A Layered '
           'Attack Surface Framework',
  'url': 'https://arxiv.org/abs/2604.23338'},
 {'authors': ['Sheldon Yu', 'Yingcheng Sun', 'Hanqing Guo', 'Qianqian Tong'],
  'content': '## Problem Statement & Context\n'
             'Large Language Model (LLM)-powered agents demonstrate strong capabilities in '
             'autonomous task execution, tool use, and multi-step reasoning. However, their '
             'increasing autonomy also introduces a new attack surface: adversarial interactions '
             'can manipulate agent behavior through direct prompt injection, indirect content '
             'attacks, and multi-turn escalation strategies. Existing defense strategies focus on '
             'prompt-level filtering and rule-based guardrails, which are often insufficient when '
             'risk emerges gradually across interaction sequences.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'In this work, we propose a complementary defense mechanism: a low-latency fraud '
             'detection layer for detecting adversarial interaction patterns in LLM-powered '
             'agents. Instead of determining whether a single prompt is malicious, our approach '
             'models risk over interaction trajectories using structured runtime features derived '
             'from prompt characteristics, session dynamics, tool usage, execution context, and '
             'fraud-inspired signals. The detection layer can be implemented using lightweight '
             'models leading to low-latency real-time deployments.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'To evaluate the framework, we construct a synthetic corpus of 12,000 multi-turn '
             'agent interactions generated from parameterized templates that simulate realistic '
             'agentic workflows. Using 42 structured features and an XGBoost classifier, our '
             'detector achieves over 9 times faster than LLM-based detectors. Through the '
             'experiment and ablation studies, our work suggests that interaction-level behavioral '
             'detection should become a core component of deployment-time defense for LLM-powered '
             'agents.',
  'doc_id': 'arxiv-2605.01143',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2605.01143', 'pdf_url': 'https://arxiv.org/pdf/2605.01143'},
  'institutions': [],
  'notes': 'Evaluated on a synthetic corpus of 12,000 template-generated interactions, not organic '
           "traces. The arXiv listing shows a newer-version title 'A Fraud-Detection-Inspired "
           "Framework for LLM Agents Security'; title here is from the abstract page as fetched. "
           'Metadata verified from the arXiv abstract page on 2026-11-13.',
  'priority': 'high',
  'published_date': '2026-05-01',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['trajectory-monitoring',
           'fraud-detection',
           'agent-security',
           'multi-turn',
           'xgboost',
           'ai-security'],
  'title': 'A Low-Latency Fraud Detection Layer for Detecting Adversarial Interaction Patterns in '
           'LLM-Powered Agents',
  'url': 'https://arxiv.org/abs/2605.01143'},
 {'authors': ['Chenglin Yang'],
  'content': '## Problem Statement & Context\n'
             'Modern AI agents execute real-world side effects through tool calls such as file '
             'operations, shell commands, HTTP requests, and database queries. A single unsafe '
             'action, including accidental deletion, credential exposure, or data exfiltration, '
             'can cause irreversible harm. Existing defenses are incomplete: post-hoc benchmarks '
             'measure behavior after execution, static guardrails miss obfuscation and multi-step '
             'context, and infrastructure sandboxes constrain where code runs without '
             'understanding what an action means.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We present AgentTrust, a runtime safety layer that intercepts agent tool calls '
             'before execution and returns a structured verdict: allow, warn, block, or review. '
             'AgentTrust combines a shell deobfuscation normalizer, SafeFix suggestions for safer '
             'alternatives, RiskChain detection for multi-step attack chains, and a cache-aware '
             'LLM-as-Judge for ambiguous inputs. We release a 300-scenario benchmark across six '
             'risk categories and an additional 630 independently constructed real-world '
             'adversarial scenarios.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'On the internal benchmark, the production-only ruleset achieves 95.0% verdict '
             'accuracy and 73.7% risk-level accuracy at low-millisecond end-to-end latency. On the '
             '630-scenario benchmark, evaluated under a patched ruleset and not claimed as '
             'zero-shot, AgentTrust achieves 96.7% verdict accuracy, including about 93% on '
             'shell-obfuscated payloads. AgentTrust is released under the AGPL-3.0 license and '
             'provides a Model Context Protocol server for MCP-compatible agents.',
  'doc_id': 'arxiv-2605.04785',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2605.04785', 'pdf_url': 'https://arxiv.org/pdf/2605.04785'},
  'institutions': [],
  'notes': 'Single-author, AGPL-3.0, ships an MCP server. Its RiskChain module targets multi-step '
           'attack chains. The 630-scenario result is stated by the author to be under a patched '
           'ruleset and not zero-shot. Metadata verified from the arXiv abstract page on '
           '2026-11-13.',
  'priority': 'medium',
  'published_date': '2026-05-06',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['agent-runtime', 'tool-call-interception', 'risk-chain', 'mcp', 'ai-security'],
  'title': 'AgentTrust: Runtime Safety Evaluation and Interception for AI Agent Tool Use',
  'url': 'https://arxiv.org/abs/2605.04785'},
 {'authors': ['Zhiqing Ma', 'Zhonghao Xu', 'Dong Yu', 'Chen Kang', 'Changliang Li', 'Pengyuan Liu'],
  'content': '## Problem Statement & Context\n'
             'Multi-turn jailbreak attacks pose a growing threat to LLMs by exploiting '
             'conversational dynamics such as gradual escalation and cross-turn coordination. '
             'Existing defenses either rely on costly retraining -- often degrading model utility '
             '-- or apply single-turn analysis independently at each turn, failing to capture how '
             'risk accumulates along interaction trajectories.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We observe that safety behavior in multi-turn interaction is trajectory-dependent: '
             "dialogue history continuously reshapes the model's conditioning context, making it "
             'insufficient to evaluate each turn in isolation. Motivated by this insight, we '
             'present THRD, the first training-free framework that explicitly models temporal risk '
             'accumulation for multi-turn jailbreak defense.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'THRD integrates four modules: a Turn-level Risk Assessor (TRA) for instantaneous '
             'risk estimation, a Historical Context Analyzer (HCA) for cross-turn intent '
             'escalation detection, a Response Evaluator (RE) for identifying facilitative '
             'outputs, and a Decision Module that combines these signals through a time-evolving '
             'scoring mechanism with attenuation-based modulation and trend-aware adjustment. '
             'Experiments against state-of-the-art multi-turn attacks -- including '
             'tree-search-based and multi-agent collaborative methods -- across two target models '
             'show that THRD reduces ASR to 0.2--4.0% while preserving model utility within 1.5% '
             'degradation on MMLU and GSM8K. Ablation studies confirm non-redundant module '
             'contributions and stable cross-architecture generalization. Analysis of first '
             'rejection triggers reveals that over 70% of multi-turn attacks require Turn~2 or '
             'later to detect, validating the necessity of explicit temporal aggregation.',
  'doc_id': 'arxiv-2606.01738',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2606.01738', 'pdf_url': 'https://arxiv.org/pdf/2606.01738'},
  'institutions': [],
  'notes': 'Training-free defense with four modules (turn risk, historical context, response '
           'evaluator, decision). Reports ASR 0.2-4.0% and that over 70% of multi-turn attacks '
           'need Turn 2 or later to detect. Metadata verified from the arXiv abstract page on '
           '2026-11-13.',
  'priority': 'high',
  'published_date': '2026-06-01',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['multi-turn',
           'trajectory-monitoring',
           'jailbreak-defense',
           'training-free',
           'ai-security'],
  'title': 'THRD: A Training-Free Multi-Turn Defense Framework for Jailbreak Attacks on Large '
           'Language Models',
  'url': 'https://arxiv.org/abs/2606.01738'},
 {'authors': ['Muberra Ozmen', 'Subhabrata Majumdar'],
  'content': '## Problem Statement & Context\n'
             'Multi-turn jailbreak attacks on large language models (LLMs) reveal a mismatch in '
             'current guardrails: they operate on individual turns, while attacks unfold as '
             'trajectories across conversations. We propose a shift from content to dynamics, '
             'modeling conversations as paths in representation space and asking whether '
             'adversarial intent is encoded early in their geometry.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'We introduce PsychoPass, a framework that extracts geometric features from '
             'conversation trajectories in embedding space to predict a potential attack before '
             'harmful content is produced. These features achieve near-perfect performance in '
             'na\\"ive classifiers, which is largely explained by the inclusion of number of turns '
             'as a feature.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'After removing this confound, a smaller but consistent geometric signal remains, '
             'with classification performance that does not depend meaningfully on encoder choice. '
             'Crucially, this signal appears early in the conversation: attack outcomes remain '
             'above chance from short prefixes alone, more reliably than baseline guardrails. A '
             'supporting theoretical analysis explains these findings via a decomposition of '
             'length and shape, a detection bound based on prefix length, and encoder invariance. '
             'Together, these results show that adversarial conversations leave an early, '
             'representation-robust geometric fingerprint suitable for online monitoring.',
  'doc_id': 'arxiv-2606.03136',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2606.03136', 'pdf_url': 'https://arxiv.org/pdf/2606.03136'},
  'institutions': [],
  'notes': 'Caveat from the abstract itself: near-perfect classifier scores are largely explained '
           'by number of turns as a confound; after removing it a smaller but consistent geometric '
           'signal remains. Metadata verified from the arXiv abstract page on 2026-11-13.',
  'priority': 'high',
  'published_date': '2026-06-02',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['multi-turn',
           'trajectory-monitoring',
           'embedding-geometry',
           'early-detection',
           'ai-security'],
  'title': 'PsychoPass: Geometric Profiling of Multi-Turn Adversarial LLM Conversations',
  'url': 'https://arxiv.org/abs/2606.03136'},
 {'authors': ['Elias Hossain',
              'Md Mehedi Hasan Nipu',
              'Tasfia Nuzhat Ornee',
              'Rajib Rana',
              'Niloofar Yousefi'],
  'content': '## Problem Statement & Context\n'
             'Tool-using LLM agents increasingly execute high-impact actions, making runtime '
             'safety monitoring essential. We present NEXUS (Neural EXecution Utility and Safety), '
             'a structured-plan safety monitor that applies a formal intervention policy to select '
             'among four actions: allow, block, request confirmation, or request revision. NEXUS '
             'combines deterministic safety rules, argument-level inspection, and a calibrated '
             'logistic-regression risk score for graded escalation.\n'
             '\n'
             '## Proposed Mechanism & Architecture\n'
             'On a 128-instance synthetic benchmark, NEXUS achieves an F1 score of 0.949 and a '
             '4-class intervention accuracy of 0.6406, outperforming rule-only intervention '
             'selection by 27.3 percentage points. It also improves over rule-only on R-Judge (F1 '
             '= 0.861 vs. 0.849), matches rule-only on AgentHarm due to threat-model limits, and '
             'achieves 0% ASR at 99% control allow on IPI.\n'
             '\n'
             '## Evaluation & Key Findings\n'
             'On the rule-blind NEXUS-Stress benchmark, NEXUS reaches an F1 score of 0.881, '
             'highlighting the difficulty of fine-grained intervention routing. With 0.205 ms '
             'median latency, NEXUS adds under 0.1% overhead to typical agent loops. Code, '
             'benchmarks, and the calibrated risk scorer are publicly released.',
  'doc_id': 'arxiv-2607.19356',
  'doc_type': 'academic_paper',
  'identifiers': {'arxiv': '2607.19356', 'pdf_url': 'https://arxiv.org/pdf/2607.19356'},
  'institutions': [],
  'notes': 'Abstract page shows submission 25 May 2026 although the arXiv ID is 2607.*; date '
           'recorded as shown on the page. Evaluated on a 128-instance synthetic benchmark plus '
           'R-Judge, AgentHarm and IPI. Session-state numbers cited in earlier search summaries '
           'are NOT in the abstract and are not recorded here. Metadata verified from the arXiv '
           'abstract page on 2026-11-13.',
  'priority': 'high',
  'published_date': '2026-05-25',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['agent-runtime', 'tool-use', 'intervention-policy', 'benchmarks', 'ai-security'],
  'title': 'NEXUS: Structured Runtime Safety for Tool-Using LLM Agents',
  'url': 'https://arxiv.org/abs/2607.19356'},
 {'authors': [],
  'content': '## Claim\n'
             'Zenity argues device-based AI (coding agents and personal AI tools on endpoints) is '
             'a distinct risk class. Its stated position is that EDR and DLP monitor processes and '
             'file activity but cannot observe what a coding agent decides, what it writes, where '
             'it sends data, or which external services and MCP servers it connects to.\n'
             '\n'
             '## Threat vectors listed\n'
             'Code and data exfiltration, destructive actions, prompt injection, lateral movement, '
             'and supply-chain risk via repositories, extensions and MCP servers.\n'
             '\n'
             '## Caveat\n'
             'Vendor marketing content; the visibility gap is asserted, not measured.',
  'doc_id': 'note-2026-zenity-device-based-ai-security',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://zenity.io/academy/device-based-ai-security'},
  'institutions': [],
  'notes': 'Source-type: vendor blog (Zenity).. Opening section read; remainder not reviewed.',
  'priority': 'medium',
  'published_date': '2026-07-02',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['endpoint', 'edr', 'coding-agents', 'mcp', 'vendor-blog', 'ai-security'],
  'title': 'Device-Based AI Security: Protecting Endpoint AI Agents (Zenity)',
  'url': 'https://zenity.io/academy/device-based-ai-security'},
 {'authors': [],
  'content': '## Claim (as attributed to Tenet Security)\n'
             'Attacker-controlled instructions are POSTed into Sentry error events using only a '
             'public write-only DSN. AI coding agents (Claude Code, Cursor, Codex) retrieved the '
             "events over MCP, did not distinguish them from real errors in Tenet's testing, and "
             "ran attacker-controlled commands with the developer's own privileges.\n"
             '\n'
             '## Reported figures\n'
             'Tenet reports an 85% exploitation success rate across tested agents and at least '
             '2,388 organizations with injectable DSNs. In tested configurations the attack '
             'bypassed EDR, WAF, IAM and VPN because only authorized operations were performed '
             "with the developer's credentials.\n"
             '\n'
             '## Caveat\n'
             "These are Tenet's proof-of-concept results, not confirmed exploitation at scale (the "
             'CSA note says so). Sentry reportedly acknowledged the disclosure but declined '
             'root-cause remediation.',
  'doc_id': 'note-2026-csa-agentjacking-mcp-sentry',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/'},
  'institutions': [],
  'notes': 'Source-type: industry research note (CSA Labs) summarizing vendor research by Tenet '
           'Security.. Key Takeaways and background read; full attack chain not reviewed.',
  'priority': 'high',
  'published_date': '2026-06-12',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['agentjacking',
           'mcp',
           'prompt-injection',
           'edr-bypass',
           'coding-agents',
           'endpoint',
           'ai-security'],
  'title': 'Agentjacking: MCP Injection Hijacks AI Coding Agents (Cloud Security Alliance research '
           'note)',
  'url': 'https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-mcp-sentry-injection-20260612/'},
 {'authors': [],
  'content': '## Points reported by a search excerpt (unverified)\n'
             '- Claude Code reads project configuration automatically, so a malicious MCP server '
             'defined in those files can execute commands before the trust dialog appears.\n'
             "- A Cursor issue where approval was tied to a plugin's name rather than a content "
             'hash of what was approved.\n'
             '\n'
             '## To do\n'
             'Read the article and confirm the CVE identifiers and affected versions before '
             'relying on this note.',
  'doc_id': 'note-2026-darkreading-ai-coding-tools-endpoint',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://www.darkreading.com/application-security/ai-coding-tools-endpoint-security'},
  'institutions': [],
  'notes': 'Source-type: news article (Dark Reading).. NOT READ: the page returned HTTP 403 (bot '
           'wall) on 2026-11-13. The points below come from a web-search excerpt and should be '
           'verified against the article.',
  'priority': 'medium',
  'published_date': '',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['endpoint', 'mcp', 'coding-agents', 'news', 'unverified', 'ai-security'],
  'title': 'How AI Coding Tools Crushed the Endpoint Security Fortress (Dark Reading)',
  'url': 'https://www.darkreading.com/application-security/ai-coding-tools-endpoint-security'},
 {'authors': [],
  'content': '## Framing\n'
             'Pillar says good coding-agent security does four things: find every agent on a '
             "developer machine, audit each one's configuration, block a dangerous action before "
             'it runs, and keep doing so if the developer or agent tries to disable the control.\n'
             '\n'
             '## Claims\n'
             'The guide compares thirteen tools on eight questions. It recommends Pillar, citing '
             'configuration parsing for Claude Code, Cursor, Gemini CLI, Codex CLI and OpenCode, '
             'pre-action controls on three of them, and an MCP catalog of 23,000+ analyzed '
             'servers. It names Palo Alto Networks (Koi) and Noma as closest alternatives.\n'
             '\n'
             '## Caveat\n'
             'Self-recommending vendor comparison; treat the ranking and product claims as '
             'unverified.',
  'doc_id': 'note-2026-pillar-ai-coding-agent-security-tools',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://www.pillar.security/blog/best-ai-coding-agent-security-tools-for-the-enterprise-2026'},
  'institutions': [],
  'notes': 'Source-type: vendor blog (Pillar Security), a comparison that includes and recommends '
           "the publisher's own product.. Introduction read; the 13-tool comparison table was not "
           'reviewed.',
  'priority': 'medium',
  'published_date': '2026-10-02',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['endpoint', 'coding-agents', 'mcp', 'vendor-blog', 'product-comparison', 'ai-security'],
  'title': 'Best AI Coding Agent Security Tools for the Enterprise (2026) (Pillar Security)',
  'url': 'https://www.pillar.security/blog/best-ai-coding-agent-security-tools-for-the-enterprise-2026'},
 {'authors': [],
  'content': '## Claim\n'
             'Workforce AI security focused on the browser for two years; coding agents, skills '
             'and MCP servers now run on laptops with real access to code, credentials and '
             'internal systems, and security teams lack visibility into what they do.\n'
             '\n'
             '## Illustrative scenario\n'
             'The post walks through a hypothetical: a sanctioned agent plus an approved Jira MCP '
             'server processes a ticket containing buried instructions to fetch and run an '
             'external script, exfiltrating a .env file. Every step looks legitimate in '
             'isolation.\n'
             '\n'
             '## Caveat\n'
             'The scenario is illustrative, not an incident report. Vendor content.',
  'doc_id': 'note-2026-lasso-securing-ai-on-endpoints',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://www.lasso.security/blog/securing-ai-on-endpoints-how-to-govern-ai-tools-coding-agents-and-mcp-connections'},
  'institutions': [],
  'notes': 'Source-type: vendor blog (Lasso Security).. Introduction read; remainder not reviewed.',
  'priority': 'medium',
  'published_date': '2026-09-28',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['endpoint', 'coding-agents', 'mcp', 'prompt-injection', 'vendor-blog', 'ai-security'],
  'title': 'Securing AI on Endpoints: How to Govern AI Tools, Coding Agents, and MCP Connections '
           '(Lasso Security)',
  'url': 'https://www.lasso.security/blog/securing-ai-on-endpoints-how-to-govern-ai-tools-coding-agents-and-mcp-connections'},
 {'authors': [],
  'content': '## Claim\n'
             'Agents such as Claude Code, Codex and Cursor read local files, launch processes, use '
             'stored credentials and load MCP servers, skills, plugins and hooks. Backslash calls '
             "this the 'agentic fabric' and says EDR sees processes, MDM sees installed apps and "
             'proxies see traffic, but none connect a prompt, a component and a permission to the '
             'local action that followed.\n'
             '\n'
             '## Evaluation criteria it proposes\n'
             'Discover every agent and component on the device; map what each can reach; block '
             'unsafe local actions before they complete; preserve endpoint-level evidence for '
             'investigation.\n'
             '\n'
             '## Cited statistic\n'
             "Cites Latio's 2026 AI Security Market Report: 45% of surveyed practitioners named "
             'endpoint agents as their primary AI security concern, and teams with a dedicated AI '
             'security budget rose from 8% to 37% in a year (not independently checked).\n'
             '\n'
             '## Caveat\n'
             'Vendor-authored ranking.',
  'doc_id': 'note-2026-backslash-agentic-endpoint-security-top7',
  'doc_type': 'note',
  'identifiers': {'source_url': 'https://www.backslash.security/blog/top-7-agentic-endpoint-security-companies'},
  'institutions': [],
  'notes': 'Source-type: vendor blog (Backslash Security), a vendor ranking.. TL;DR and '
           'introduction read; the vendor-by-vendor sections were not reviewed.',
  'priority': 'medium',
  'published_date': '2026-10-01',
  'reading_status': 'to-read',
  'relations': [],
  'tags': ['endpoint',
           'edr',
           'coding-agents',
           'mcp',
           'vendor-blog',
           'product-comparison',
           'ai-security'],
  'title': 'Top 7 Agentic Endpoint Security Companies CISOs Should Evaluate in 2026 (Backslash '
           'Security)',
  'url': 'https://www.backslash.security/blog/top-7-agentic-endpoint-security-companies'}]
