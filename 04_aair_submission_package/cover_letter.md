# AAIR JOURNAL SUBMISSION COVER LETTER

**Date:** October 30, 2026  
**To:** Dr. Osman Özkaraca, Editor-in-Chief  
Editorial Board of *Advances in Artificial Intelligence Research* (AAIR)  
DergiPark Platform (e-ISSN: 2757-7422)  

**Subject:** Submission of Original Research Article for Peer Review  

Dear Dr. Özkaraca and Editorial Board Members,

Please consider our original research manuscript entitled:

> **"Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment"**

for publication as a regular Research Article in *Advances in Artificial Intelligence Research* (AAIR).

### Motivation and Core Contributions
While Retrieval-Augmented Generation (RAG) is established as an effective paradigm for grounding generative AI, conventional static architectures unconditionally retrieve external passages for all queries. In this work, we demonstrate that this always-on paradigm introduces severe vulnerabilities when applied to Small Language Models (SLMs, 1B–8B parameters), including:
1. **Context Distraction & Hallucination Amplification:** Due to constrained parameter capacity, SLMs are easily misled when dense retrievers return irrelevant or conflicting passages, causing hallucinated rationalizations on facts the model already knows.
2. **Inference Inefficiency:** Static retrieval wastes up to $50\%$ of token processing and energy on common-knowledge queries.

To resolve these challenges, we propose an **Uncertainty-Gated Selective RAG** architecture that evaluates a single-pass Shannon entropy probe ($\mathcal{U}(q)$) over the initial $M=3$ prefix decoding tokens. Our method operates completely post-hoc on off-the-shelf and 4-bit quantized models without requiring weight retraining or multi-pass latency penalties. Evaluated across 18,000+ queries from PopQA, Natural Questions, and TruthfulQA, our approach cuts hallucination error rates by up to $22\%$ under noisy context, reduces end-to-end inference latency by $38\%$, and lowers GPU energy consumption by $31\%$.

### Compliance and Originality Statements
* **Originality:** This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere.
* **Integrity & Similarity:** A complete similarity report (iThenticate/Turnitin) is attached, confirming a similarity index below the mandatory $20\%$ threshold ($8.4\%$ observed).
* **Anonymity:** The main manuscript file has been completely anonymized for double-blind peer review in accordance with AAIR guidelines.
* **Ethics & Data:** All experiments utilize publicly available, open-license benchmarks and models. No human or animal subjects were involved, requiring no IRB clearance.
* **Copyright:** All authors have approved the manuscript and agree to the open-access terms (CC BY-NC 4.0) and copyright transfer policies of AAIR upon acceptance.

### Suggested Independent Reviewers
As required by AAIR author guidelines, we nominate three independent subject-matter experts qualified to review this manuscript who have no conflicts of interest with the authors:

1. **Dr. Wenliang Chen**  
   *Affiliation:* Institute of Artificial Intelligence, Soochow University  
   *Email:* wlchen@suda.edu.cn  
   *Expertise:* Natural Language Processing, Hallucination Detection in Generative Models, Information Extraction.

2. **Prof. Dr. Yiming Peng**  
   *Affiliation:* Department of Computer Science, University of Sheffield  
   *Email:* y.peng@sheffield.ac.uk  
   *Expertise:* Retrieval-Augmented Generation, Dense Retrieval, Language Model Evaluation.

3. **Dr. Megha Kumar**  
   *Affiliation:* School of Computing and Data Science, Nanyang Technological University  
   *Email:* megha.kumar@ntu.edu.sg  
   *Expertise:* Small Language Models, Model Quantization, Edge AI Efficiency.

**Opposed Reviewers (if any):** None to declare.

Thank you for your editorial consideration of our work. We look forward to receiving the reviewers' comments.

Sincerely,

**Corresponding Author:**  
Omkar Sachin Shedage  
Department of Artificial Intelligence and Data Science  
JSPM Narhe Technical Campus, Savitribai Phule Pune University  
Pune, Maharashtra 411041, India  
Email: omkarshedage1977@gmail.com  
GitHub: https://github.com/Omkar-ai-wed  

