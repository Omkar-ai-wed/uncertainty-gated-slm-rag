# SEMINAR PRESENTATION SLIDE DECK OUTLINE

**Presentation Duration:** 12–15 Minutes (10 Slides + 2 Buffer Slides)  
**Target Audience:** Department Evaluation Committee, Faculty Advisors, and Peer Scholars  
**Presentation Topic:** *Uncertainty-Gated Selective Retrieval in Quantized Small Language Models (SLMs)*

---

### Slide 1: Title & Introduction
* **Header:** Uncertainty-Gated Selective Retrieval in Quantized Small Language Models (SLMs)
* **Subtitle:** Mitigating Noise-Induced Hallucinations and Optimizing Edge AI Efficiency
* **Presenter Information:** Omkar Sachin Shedage (Under the guidance of Prof. Snehal Bhoge), Department of AI & Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University
* **Target Venue:** Submitted to *Advances in Artificial Intelligence Research* (DergiPark)
* **Visual:** Minimal split graphic showing an Edge Device (Smartphone/Embedded GPU) vs. Cloud Server Farm with a balance scale showing Accuracy vs. Latency.
* **Speaker Notes:** "Good morning respected committee members. Today I am presenting our research addressing a fundamental limitation in generative AI: how to make lightweight, quantized language models factually reliable without the massive latency and energy footprint of cloud-scale models."

---

### Slide 2: The Core Dilemma in the AI Era
* **Header:** Hallucination vs. Compute Prohibitive Costs
* **Key Points:**
  * Frontier LLMs (70B–405B) achieve high accuracy but cost up to $\$50/\text{M}$ tokens and require multi-GPU cloud clusters.
  * Small Language Models (SLMs, 1B–8B) enable private, on-device computing, but suffer from knowledge boundary limitations.
  * Standard RAG was introduced to bridge this gap by injecting retrieved Wikipedia passages into the prompt.
* **Visual:** Graph showing parameter scale vs. operational cost.
* **Speaker Notes:** "While RAG is widely used, standard implementations assume bigger is better and that retrieval should be unconditional. We show why this assumption breaks down catastrophically on small models."

---

### Slide 3: The Failure Mode: Why Static RAG Fails in SLMs
* **Header:** Context Distraction and Noise Amplification
* **Key Points:**
  * **Static RAG is Unconditional:** Every question triggers dense retrieval, even if the model already knows the answer.
  * **Limited Cross-Attention Filtering:** Unlike 70B models, 1B–8B models are easily distracted when retrieved context contains irrelevant or conflicting passages.
  * **Empirical Reality (Yoran et al., ICLR 2024):** Adding two noisy passages drops open-source model accuracy by up to $34\%$.
* **Visual:** Diagram showing a correct parametric answer getting overridden by an irrelevant retrieved snippet, resulting in a hallucination.
* **Speaker Notes:** "When an SLM is forced to read noisy or conflicting documents, it lacks the parameter capacity to reject them. It hallucinates justifications to reconcile the text, effectively turning clean parametric knowledge into confabulated output."

---

### Slide 4: The Efficiency Paradox
* **Header:** Inference Latency and Energy Waste
* **Key Points:**
  * Over $50\%$ of enterprise/user queries concern high-popularity entities that SLMs already know accurately.
  * Static RAG forces: Query Encoding $\to$ FAISS Search $\to$ Context Token Concatenation $\to$ Generation.
  * Result: Latency increases from $80\text{ms}$ to $350\text{ms}+$; GPU energy draw increases by $150\%$.
* **Visual:** Bar chart comparing latency of Direct SLM vs. Static RAG.
* **Speaker Notes:** "Why perform a vector database lookup for 'What is the capital of France?' when the model knows it with $99.9\%$ certainty? It wastes battery on mobile devices and slows down interactive chatbots."

---

### Slide 5: The Proposed Solution: Uncertainty-Gated Selective RAG
* **Header:** Epistemic Confidence Gating via Prefix Predictive Entropy
* **Key Points:**
  * Prior adaptive methods (Rowen, SIGIR 2025) generate 3–5 responses to test consistency, tripling latency.
  * **Our Innovation:** A single-pass prefix entropy probe over the first $M=3$ decoded tokens.
  * High parametric confidence ($\mathcal{U}(q) < \tau$) $\implies$ Bypass retrieval.
  * Epistemic uncertainty ($\mathcal{U}(q) \ge \tau$) $\implies$ Trigger dense retrieval and semantic filtering.
* **Visual:** The system architectural flowchart (Query $\to$ Entropy Probe $\to$ Branching Path $\to$ Answer).
* **Speaker Notes:** "By inspecting the Shannon entropy of the model's own output distribution on the first three tokens, we know in less than 15 milliseconds whether the model knows the fact or needs external help."

---

### Slide 6: Mathematical Formulation
* **Header:** Formulation of Prefix Predictive Entropy
* **Equation:**
  $$\mathcal{U}(q) = -\frac{1}{M} \sum_{m=1}^M \sum_{v \in \mathcal{V}} P(y_m = v \mid q, y_{<m}) \log P(y_m = v \mid q, y_{<m})$$
* **Gating Policy:**
  $$\text{Decision}(q) = \begin{cases} \text{Direct SLM Inference} & \text{if } \mathcal{U}(q) < \tau \\ \text{Dense Vector Retrieval + SLM} & \text{if } \mathcal{U}(q) \ge \tau \end{cases}$$
* **Threshold Calibration:** $\tau$ is calibrated on PopQA to optimize the F1-separation margin between known and long-tail entities.
* **Speaker Notes:** "This formulation requires zero model weight modifications and zero fine-tuning. It works post-hoc on any modern quantized causal language model."

---

### Slide 7: Experimental Setup & Datasets
* **Header:** Rigorous Multi-Benchmark Evaluation
* **Models Evaluated:** Llama-3.2 (1B, 3B), Gemma-2 (2B), Qwen-2.5 (1.5B) in FP16 and INT4 AWQ.
* **Knowledge Corpus:** English Wikipedia (21M passages indexed via FAISS and BGE-small).
* **Benchmarks:**
  * *PopQA (14,267 queries):* Tests popularity stratification.
  * *TruthfulQA (817 queries):* Tests resistance to false human misconceptions.
  * *Natural Questions (3,610 queries):* Real Google search queries.
* **Hardware:** Single NVIDIA RTX 4090 / Colab GPU with `pynvml` energy tracking.
* **Speaker Notes:** "We evaluate our method across thousands of questions spanning common facts to obscure historical data, tracking both accuracy and physical hardware energy consumption."

---

### Slide 8: Preliminary Results: Clean Separation of Epistemic Uncertainty
* **Header:** Empirical Validation of the Entropy Margin
* **Key Empirical Findings:**
  * Popular entities exhibit low prefix entropy: $\sim 1.15$ nats.
  * Long-tail obscure queries exhibit high prefix entropy: $\sim 2.82$ nats.
  * **Entropy Delta:** A statistically significant gap of $1.67$ nats ($p < 0.001$).
  * Gating successfully bypasses retrieval on $52.3\%$ of standard queries.
* **Visual:** Overlapping distribution plot showing clean separation between popular and long-tail query entropy.
* **Speaker Notes:** "Our pilot results confirm that the model's internal entropy provides a distinct, unambiguous boundary. It easily identifies when it is safe to skip the database lookup."

---

### Slide 9: Noise Stress-Testing & Pareto Frontiers
* **Header:** Resilience to Distractors & Resource Optimization
* **Findings:**
  * When $50\%$ noisy distractors are injected, Static RAG accuracy drops by $26.4\%$; Gated RAG drops by only $4.1\%$ because confident queries never see the noise.
  * Average latency drops by $38.2\%$ across the benchmark.
  * Energy consumption decreases by $31.5\%$ Joules per query.
* **Visual:** Pareto curve comparing Accuracy (y-axis) vs. Latency/Energy (x-axis) across Closed-Book, Static RAG, Rowen, and Gated RAG.
* **Speaker Notes:** "Our method achieves the optimal Pareto frontier: near-oracle accuracy with half the energy consumption of static RAG."

---

### Slide 10: Conclusion & Next Steps
* **Header:** Summary of Contributions
* **Key Takeaways:**
  1. Solved the context distraction problem in Small Language Models without expensive retraining.
  2. Replaced high-latency multi-pass adaptive methods with a sub-15ms prefix entropy probe.
  3. Achieved substantial latency and energy reductions suitable for edge AI.
* **Next Milestone:** Submitting the finalized 14-page manuscript to *Advances in Artificial Intelligence Research* (AAIR).
* **Speaker Notes:** "In conclusion, uncertainty-gated RAG demonstrates that small, localized AI can be made both reliable and fast. Thank you, and I look forward to your questions."

---

### Slide 11 (Buffer): Quantization Interaction (FP16 vs. INT4 AWQ)
* Details how 4-bit activation-aware weight quantization impacts attention head entropy.

### Slide 12 (Buffer): Limitations & Boundary Conditions
* Outlines failure cases: queries with high linguistic ambiguity despite known factual answers (e.g., highly complex phrasing).

