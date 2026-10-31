# VIVA & ORAL DEFENSE Q&A PREPARATION GUIDE

**Target:** Final Year Seminar / Capstone Examination & Peer Review Defense  
**Project:** *Uncertainty-Gated Selective Retrieval in Quantized Small Language Models (SLMs)*  

---

### Category 1: Conceptual & Foundational Challenges

#### Q1: "Why focus on Small Language Models (SLMs) when frontier models like GPT-4 or Claude 3.5 already have low hallucination rates?"
* **Core Answer:**
  "While frontier models are capable, they are fundamentally centralized cloud APIs requiring hundreds of gigawatts of energy, high token costs (up to $\$50/\text{M}$ tokens), and severe data privacy violations for sensitive enterprise or healthcare data. In real-world applications—such as defense, on-device mobile assistants, and edge healthcare—we must run models locally on edge devices with 8B or fewer parameters. Our research addresses the specific vulnerability of these edge models under retrieval, ensuring that democratization of AI does not compromise factual safety."
* **Literature Reference:** Lin et al. (MLSys 2024, AWQ) and Dettmers et al. (NeurIPS 2023, QLoRA).

---

#### Q2: "How does your uncertainty gating differ from existing works like Self-RAG (ICLR 2024) or Rowen (SIGIR 2025)?"
* **Core Answer:**
  "Existing adaptive retrieval works suffer from two major trade-offs:
  1. *Self-RAG (Asai et al., 2024)* requires pre-training the model from scratch with custom reflection tokens (`[Retrieve]`, `[IsSup]`). This is impossible for off-the-shelf, quantized models or low-budget academic settings.
  2. *Rowen (Ding et al., 2025)* operates at test-time but generates 3 to 5 full candidate answers and measures lexical/semantic consistency across multilingual perturbations. This triples the inference latency ($>300\%$ overhead).
  Our approach is a **single-pass, post-hoc internal state probe**. We inspect the Shannon entropy of the model's first $M=3$ decoded tokens in less than 15 milliseconds. It requires zero weight updates, zero fine-tuning, and introduces virtually zero latency overhead."

---

#### Q3: "What is Shannon entropy, and why do you measure it only on the first $M=3$ tokens instead of the entire response?"
* **Core Answer:**
  "Shannon entropy measures the uncertainty of the probability distribution over the vocabulary:
  $$\mathcal{U} = -\sum_{v \in \mathcal{V}} P(v) \log P(v)$$
  If the model has high confidence in a factual claim (e.g., 'Paris'), the probability of the top token is close to $1.0$, resulting in near-zero entropy. If the model is uncertain, the distribution is flat, yielding high entropy.
  We restrict measurement to the first $M=3$ tokens (the response onset prefix) because measuring the full sequence would require generating the entire answer before deciding whether to retrieve, which negates the latency and energy benefits. Early prefix entropy captures the model's initial epistemic certainty regarding the subject-predicate relation of the query."

---

### Category 2: Methodological & Technical Challenges

#### Q4: "What if the query is linguistically ambiguous or has multiple valid phrasings? Wouldn't that create artificially high entropy even if the model knows the fact?"
* **Core Answer:**
  "That is a valid challenge known as *linguistic entropy vs. semantic entropy*. To prevent syntactic variance from triggering false retrieval, we employ a standardized prompt template ('Question: ... Answer with a concise factual answer: ...') which anchors the model's generation syntax. Furthermore, we calibrate our threshold $\tau$ not on arbitrary conversational text, but specifically on factual question-answering benchmarks (PopQA), ensuring that $\tau$ reflects factual certainty rather than grammatical hesitation."

---

#### Q5: "How does 4-bit quantization (AWQ / GPTQ) affect your entropy measurements?"
* **Core Answer:**
  "Quantization compresses 16-bit floating-point weights into 4-bit integers. While perplexity on general language modeling remains relatively stable, low-bit quantization causes subtle rounding dispersion in cross-attention projections. In our ablation experiments, we observed that INT4 quantization slightly elevates baseline entropy across all tokens by $\sim 0.15\text{--}0.25$ nats. However, the *relative margin* between known and unknown entities remains statistically significant ($p < 0.01$). Thus, the gating mechanism remains robust, requiring only a minor offset recalibration of $\tau$."

---

#### Q6: "Why do you claim that Static RAG causes hallucinations? Isn't giving the model more information always better?"
* **Core Answer:**
  "In theory, more information helps. In empirical reality, dense retrievers are imperfect and routinely return irrelevant or conflicting passages in top-$k$ results. Shi et al. (ICML 2023) and Yoran et al. (ICLR 2024) proved that unlike humans, language models suffer from *context distraction*. Because SLMs have fewer attention heads and lower parameter capacity, they over-attend to tokens in the prompt context. If an irrelevant distractor mentions an incorrect entity, the SLM assumes it must be relevant and fabricates a hallucinated rationale to connect the query with the distractor. By bypassing retrieval when the model is already confident, our gate prevents the model from ever seeing distracting noise."

---

### Category 3: Evaluation & Publication Challenges

#### Q7: "How can you be sure your benchmark results aren't just memorization or dataset contamination?"
* **Core Answer:**
  "We take three specific methodological precautions against contamination:
  1. We evaluate on *PopQA*, which specifically stratifies entities by monthly Wikipedia pageviews. Long-tail entities (e.g., historical dates of obscure parishes with $<100$ views) have negligible representation in pre-training data, ensuring they test true epistemic boundaries.
  2. For our Wikipedia retrieval index, we strictly use historical frozen snapshots dated prior to test set curation.
  3. We test on *TruthfulQA*, which was explicitly engineered to contain human misconceptions where naive memorization leads to incorrect answers."

---

#### Q8: "Why did you choose the journal AAIR (Advances in Artificial Intelligence Research) on DergiPark?"
* **Core Answer:**
  "AAIR explicitly seeks papers that demonstrate how novel AI techniques advance performance in specific application domains, rather than purely incremental surveys. Our work fits their double-blind, peer-reviewed scope perfectly: it introduces an algorithmic gating innovation, provides extensive hardware telemetry (latency, memory, Joules), and evaluates practical edge deployment. Furthermore, AAIR offers Platinum Open Access with zero fees and rapid review cycles, making it an ideal venue for high-impact early-career research."

---

### Quick Examiner Checklist: Formula & Metrics Recap
* **Prefix Entropy:** $\mathcal{U}(q) = -\frac{1}{M} \sum_{m=1}^M \sum_{v \in \mathcal{V}} P(v) \log P(v)$
* **Target Horizon:** $M = 3$ tokens (decoding latency $< 15\text{ms}$)
* **Optimal Threshold Range:** $\tau \in [1.8, 2.2]$ nats (model-dependent)
* **Observed Entropy Margin:** $\Delta \mathcal{U} \approx 1.67$ nats between popular and long-tail entities
* **Observed Latency Reduction:** $\sim 38\%$ reduction in end-to-end query time
* **Observed Noise Shielding:** Drops hallucination rate by up to $22\%$ under $50\%$ distractor noise

