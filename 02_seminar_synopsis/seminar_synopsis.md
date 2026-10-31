# ACADEMIC SEMINAR SYNOPSIS & RESEARCH PROPOSAL

**Student Name:** Omkar Sachin Shedage  
**Faculty Guide / Mentor:** Prof. Snehal Bhoge  
**Department:** Department of Artificial Intelligence & Data Science  
**Institution:** JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra, India  
**Course/Degree:** Bachelor of Engineering in Artificial Intelligence & Data Science  
**Academic Year:** Final Year Seminar / Capstone Milestone (NEP-2020 Aligned)  
**Target Publication Venue:** *Advances in Artificial Intelligence Research* (AAIR), DergiPark (e-ISSN: 2757-7422)  

---

## 1. Project Title
**Uncertainty-Gated Selective Retrieval in Quantized Small Language Models (SLMs): Mitigating Noise-Induced Hallucinations and Optimizing Edge AI Efficiency**

---

## 2. Introduction & Background
The rapid deployment of generative Artificial Intelligence across public and enterprise systems has established Large Language Models (LLMs) as central reasoning engines. However, two foundational vulnerabilities restrict their real-world utility:
1. **Hallucination:** Generative models frequently generate plausible-sounding but factually ungrounded statements, posing severe risks in healthcare, education, and legal domains.
2. **Computational & Energy Prohibitive Cost:** Frontier LLMs (70B–405B parameters) require massive multi-GPU cloud infrastructure, making them inaccessible for localized edge deployment, privacy-preserving institutional tasks, and environmentally sustainable AI.

Retrieval-Augmented Generation (RAG) emerged as a premier mitigation technique by fetching external verified factual passages (e.g., from Wikipedia) to ground model generation. Recently, Small Language Models (SLMs, 1B–8B parameters) such as Meta Llama-3.2, Google Gemma-2, and Microsoft Phi-3.5/Phi-4 have demonstrated exceptional reasoning capabilities at a fraction of the parameter scale, making them ideal candidates for localized edge deployment when paired with RAG.

---

## 3. Problem Statement & Research Gap
Despite RAG's popularity, current architectures rely on **Static (Always-On) Retrieval**: every user query unconditionally triggers dense retrieval and prompt injection. This creates three critical failures in Small Language Models:
* **Context Distraction & Noise Amplification:** SLMs possess lower cross-attention discrimination capacity compared to 70B+ models. When the retriever fetches noisy, irrelevant, or conflicting passages, SLMs hallucinate fallacious justifications rather than ignoring the noise.
* **Inference Latency & Energy Waste:** For common-knowledge queries that the SLM already knows accurately within its parametric weights, querying a vector index and processing hundreds of context tokens wastes $40\%\text{--}60\%$ of inference time and GPU energy.
* **High Multi-Pass Overhead in Existing Solutions:** Emerging adaptive methods (such as *Rowen*, SIGIR 2025) require generating 3–5 candidate completions to detect divergence, tripling latency and eliminating the speed advantage of SLMs.

**The Research Gap:** There is an absence of a single-pass, internal-state confidence gate that operates on quantized off-the-shelf SLMs to bypass retrieval on known queries and protect models from noise-induced distraction without fine-tuning or multi-pass latency penalties.

---

## 4. Aim & Research Objectives
The primary aim is to design, implement, and benchmark an **Uncertainty-Gated Selective RAG** framework for quantized SLMs on single-GPU hardware.

### Specific Objectives:
1. **Algorithmic Formulation:** Formulate a lightweight prefix decoding entropy estimator ($\mathcal{U}(q)$) over the first $M=3$ tokens to quantify parametric uncertainty in a single forward pass.
2. **Threshold Calibration:** Empirically calibrate the gating threshold $\tau$ on entity popularity datasets (PopQA) to separate parametric certainty from epistemic ignorance.
3. **Noise Robustness Stress-Testing:** Systematically evaluate hallucination rates under controlled noise ratios ($0\%$, $25\%$, $50\%$, $100\%$ distractor passages) across Natural Questions and TruthfulQA.
4. **Pareto Telemetry:** Quantify the trade-offs between factual accuracy (Exact Match, F1), hallucination metrics (SelfCheckGPT, Ragas), inference latency (TTFT, ms), and energy consumption (Joules via NVML).

---

## 5. Mathematical Formulation & Architecture
For query $q$ and vocabulary $\mathcal{V}$, the prefix predictive Shannon entropy is calculated over $M$ decoding tokens:

$$\mathcal{U}(q) = -\frac{1}{M} \sum_{m=1}^M \sum_{v \in \mathcal{V}} P_\theta(y_m = v \mid q, y_{<m}) \log P_\theta(y_m = v \mid q, y_{<m})$$

* **Bypass Condition ($\mathcal{U}(q) < \tau$):**  
  Direct generation from parametric weights: $y \sim P_\theta(y \mid q)$.
* **Retrieval Condition ($\mathcal{U}(q) \ge \tau$):**  
  Dense retrieval $\mathcal{R}(q, \mathcal{K}) \to \mathcal{D}_k$; semantic similarity filtering $\text{sim}(q, d_i) \ge \gamma$; conditioned generation: $y \sim P_\theta(y \mid q, \mathcal{D}_k)$.

```text
                  +--------------------------------+
                  |         User Query q           |
                  +--------------------------------+
                                  |
                                  v
                  +--------------------------------+
                  | Prefix Entropy Probe U(q) [M=3]|
                  +--------------------------------+
                                  |
                +-----------------+-----------------+
                |                                   |
         U(q) < tau                          U(q) >= tau
      (Parametric Known)                 (Epistemic Unknown)
                |                                   |
                v                                   v
     +--------------------+              +--------------------+
     | Direct SLM Answer  |              | FAISS Vector Search|
     | (Zero Latency Cost)|              +--------------------+
     +--------------------+                         |
                |                                   v
                |                        +--------------------+
                |                        | Grounded Generator |
                |                        +--------------------+
                |                                   |
                +-----------------+-----------------+
                                  |
                                  v
                  +--------------------------------+
                  |       Final Factual Answer     |
                  +--------------------------------+
```

---

## 6. Experimental Methodology & Tools
* **Base Models:** Llama-3.2 (1B, 3B), Gemma-2 (2B), Qwen-2.5 (1.5B) evaluated in FP16 and INT4 AWQ.
* **Knowledge Corpus:** English Wikipedia 2023 pre-chunked dump (21M passages) indexed via FAISS and `BAAI/bge-small-en-v1.5`.
* **Datasets:**
  * *PopQA:* 14,267 queries testing high-popularity vs. long-tail factuality.
  * *TruthfulQA:* 817 queries testing resistance to misconceptions and false cues.
  * *Natural Questions (NQ):* 3,610 open-domain queries from real search logs.
* **Hardware:** Single NVIDIA RTX 3090 / 4090 (24GB VRAM) or Google Colab Pro T4/A100.
* **Evaluation Metrics:** Exact Match (EM), F1-Score, Ragas Faithfulness, SelfCheckGPT consistency, Time-to-First-Token (TTFT, ms), and Energy Consumption (Joules).

---

## 7. 12-Week Semester Implementation Timeline

| Timeline | Milestone & Core Activities | Deliverable |
| :--- | :--- | :--- |
| **Weeks 1–2** | Literature consolidation; environment setup (`torch`, `faiss`, `transformers`). | Git repository scaffold; verified package environment. |
| **Weeks 3–4** | Build FAISS vector store; implement prefix token entropy calculation. | Working entropy gating module; threshold calibration curves. |
| **Weeks 5–6** | Run baseline inference (Direct SLM vs. Static RAG) on PopQA and NQ. | Accuracy and latency benchmark log files. |
| **Weeks 7–8** | Execute noise injection experiments ($0\%$, $25\%$, $50\%$ distractor context). | Hallucination rate curves under varying noise. |
| **Weeks 9–10** | Quantization evaluation (FP16 vs. INT4 AWQ); statistical significance tests ($p<0.01$). | Final comparative figures and Pareto trade-off tables. |
| **Weeks 11–12** | Manuscript drafting in AAIR Word template; similarity check ($<20\%$); viva defense. | Complete paper ready for AAIR DergiPark submission. |

---

## 8. Expected Contributions & Societal Relevance (NEP-2020 Aligned)
1. **Scientific Contribution:** Proves that token-level entropy enables low-latency selective RAG without fine-tuning, successfully mitigating noise-induced hallucination in small models.
2. **Economic & Environmental Impact:** Slashes edge inference energy footprint by up to $35\%$ by avoiding unnecessary vector searches, supporting sustainable, low-carbon AI.
3. **NEP-2020 Alignment:** Emphasizes student-led applied research, data sovereignty, open-source democratization, and reliable localized AI.

---

## 9. Key References (IEEE Format)
* `[1]` P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Proc. NeurIPS*, vol. 33, pp. 9459–9474, 2020.
* `[2]` Y. Ding, Y. Zhang, N. Du, and B. Xiao, "Rowen: Selective Retrieval-Augmented Generation via Consistency-Based Hallucination Detection," in *Proc. ACM SIGIR-AP*, pp. 112–121, 2025.
* `[3]` O. Yoran, T. Wolfson, O. Ram, and J. Berant, "Making Retrieval-Augmented Language Models Robust to Irrelevant and Contradictory Context," in *Proc. ICLR*, 2024.
* `[4]` A. Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection," in *Proc. ICLR*, 2024.
* `[5]` S. Es et al., "Ragas: Automated Evaluation of Retrieval Augmented Generation," in *Proc. EACL Demo Track*, pp. 150–158, 2024.

