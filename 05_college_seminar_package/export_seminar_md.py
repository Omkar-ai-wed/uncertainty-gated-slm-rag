"""
export_seminar_md.py
Exports the complete Technical Seminar Report into Technical_Seminar_Report_Omkar_Shedage.md
"""

import os
import chapters_content as c

MD_OUT = r"d:\play\RAG\05_college_seminar_package\Technical_Seminar_Report_Omkar_Shedage.md"

md_lines = []

md_lines.append("""# A SEMINAR REPORT ON
## “UNCERTAINTY-GATED SELECTIVE RETRIEVAL IN QUANTIZED SMALL LANGUAGE MODELS: MITIGATING NOISE-INDUCED HALLUCINATION AND LATENCY IN EDGE DEPLOYMENT”

**SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF DEGREE OF**  
### BACHELOR OF ENGINEERING (Artificial Intelligence & Data Science Engineering)

![JSPM College Logo](assets/jspm_college_logo.jpg)

**SUBMITTED BY:**  
**Omkar Sachin Shedage** (Roll No: TE-56)  

**UNDER THE GUIDANCE OF:**  
**Prof. Snehal Bhoge**  

**DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND DATA SCIENCE ENGINEERING**  
**JSPM’s Narhe Technical Campus, Narhe, Pune – 411041**  
**Rajarshi Shahu School of Engineering & Research**  
**SAVITRIBAI PHULE PUNE UNIVERSITY, PUNE**  
**Academic Year: 2025–26**  

---

## JSPM Narhe Technical Campus
### Rajarshi Shahu School of Engineering & Research
### DEPARTMENT OF AI&DS ENGINEERING

# CERTIFICATE

This is to certify that the preliminary technical seminar report entitled:

> **“UNCERTAINTY-GATED SELECTIVE RETRIEVAL IN QUANTIZED SMALL LANGUAGE MODELS: MITIGATING NOISE-INDUCED HALLUCINATION AND LATENCY IN EDGE DEPLOYMENT”**

Submitted by **Omkar Sachin Shedage** (Roll No: TE-56) is a bonafide work carried out by him under the supervision of **Prof. Snehal Bhoge** and it is submitted towards partial fulfillment of the requirements of **Savitribai Phule Pune University, Pune**, for the award of the degree of Bachelor of Engineering in Artificial Intelligence & Data Science Engineering.

| | | |
| :---: | :---: | :---: |
| <br><br>**Prof. Snehal Bhoge**<br>Seminar Guide | <br><br>**Prof. Hitesh Rahangdale**<br>Seminar Coordinator | <br><br>**Dr. Manisha Hajare**<br>HOD, AI&DS Engineering |

**Place:** Pune  
**Date:** ____________  

---

## DECLARATION

I hereby declare that the seminar report entitled **“Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment”** is a bonafide record of independent academic research carried out by me under the guidance of **Prof. Snehal Bhoge**, Department of Artificial Intelligence and Data Science Engineering, JSPM’s Narhe Technical Campus, Narhe, Pune.

This work is based on original research conducted during the academic year 2025–26, which has also been authored and accepted for international peer-reviewed journal publication in *Advances in Artificial Intelligence Research* (AAIR, DergiPark, e-ISSN: 2757-7422). I further declare that this seminar report or any part thereof has not been submitted previously to this or any other university or institution for the award of any degree, diploma, or fellowship.

**Omkar Sachin Shedage**  
Roll No: TE-56  
Department of AI&DS Engineering, JSPM NTC, Pune  
**Date:** ____________  

---

## Acknowledgements

With immense pleasure and gratitude, I present this technical seminar report entitled **“Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment”** as a mandatory part of the curriculum of Third Year (T.E.) Artificial Intelligence and Data Science Engineering at JSPM’s Narhe Technical Campus, Pune, affiliated with Savitribai Phule Pune University.

First and foremost, I express my profound gratitude and heartfelt respect to my Seminar Guide, **Prof. Snehal Bhoge**, for her continuous encouragement, intellectual guidance, critical technical suggestions, and patient mentoring throughout the conceptualization, benchmarking, and documentation of this work.

I express my sincere thanks to **Dr. Manisha Hajare**, Head of the Department of Artificial Intelligence and Data Science Engineering, and Seminar Coordinator **Prof. Hitesh Rahangdale** for their organizational support and providing state-of-the-art computational laboratory facilities.

I am deeply indebted to **Dr. M. M. Sardeshmukh**, Director of JSPM’s Narhe Technical Campus, for creating an inspiring academic and research-oriented institutional environment.

Lastly, I extend my heartfelt thanks to all the faculty members of the AI&DS Department, laboratory technical staff, my peers, and my family members whose unending moral support and encouragement enabled me to complete this research endeavor successfully.

**Omkar Sachin Shedage**  
Roll No: TE-56  
T.E. (Artificial Intelligence & Data Science)  

---

## Abstract

Retrieval-Augmented Generation (RAG) is established as an indispensable paradigm for grounding Large Language Models in external knowledge and mitigating factual inaccuracies. However, state-of-the-art RAG deployments operate under a rigid, unconditional retrieval paradigm: external passages are retrieved for every user query regardless of whether the query falls well within the model’s internal parametric knowledge. When deployed on compact Small Language Models (SLMs, 1B–8B parameters) operating on resource-constrained edge hardware, this "always-on" mechanism creates two severe operational bottlenecks: substantial latency and computational energy overhead, and severe vulnerability to noise-induced hallucination caused by irrelevant or conflicting retrieved contexts distracting parameter-limited decoders.

To resolve this foundational trade-off, this seminar report presents **Uncertainty-Gated Selective Retrieval**, a training-free, single-forward-pass gating architecture designed specifically for quantized edge-deployed SLMs. Rather than executing speculative multi-pass sampling or training complex external routing classifiers, our framework computes an instantaneous predictive Shannon entropy probe over the model’s initial prefix decoding horizon ($M = 3$ tokens). When the predictive entropy falls below a calibrated decision threshold ($\tau = 2.0\text{ nats}$), the query is recognized as parametrically confident and bypasses external retrieval entirely. Only when high epistemic uncertainty is diagnosed does the system trigger dense vector retrieval over a FAISS vector index.

Extensive empirical evaluations conducted across 18,694 benchmark queries spanning PopQA, Natural Questions (NQ-Open), and adversarial TruthfulQA demonstrate that the proposed architecture establishes a new Pareto efficiency frontier. Our method suppresses Hallucination Error Rate (HER) from 68.4% under naive static RAG down to 39.1% under 100% contradictory context noise (a 29.3 percentage point improvement). Concurrently, bypassing unnecessary retrieval on popular queries yields a 38.4% reduction in mean end-to-end latency (from 284.6 ms to 175.4 ms) and saves 32.2% of GPU energy consumption per query. Furthermore, validation under 4-bit Activation-aware Weight Quantization (AWQ) proves that uncertainty separation remains highly robust ($\Delta \mathcal{U} = 1.786\text{ nats}, p < 10^{-11}$) while compressing the model footprint to 2.2 GB VRAM, proving feasibility for standalone, private edge deployment.

---

## Contents

| Chapter | Contents | Page No. |
| :--- | :--- | :---: |
| | Certificate | i |
| | Declaration | ii |
| | Acknowledgements | iii |
| | Abstract | iv |
| | List of Tables | vii |
| | List of Figures | viii |
| | List of Acronyms and Abbreviations | ix |
| **Chapter 1** | **Introduction** | **1** |
| | 1.1 Introduction and Background of RAG | 1 |
| | 1.2 Problem Statement & Identified Deficiencies | 3 |
| | 1.3 Motivation: Edge Computing & Quantized SLMs | 4 |
| | 1.4 Purpose, Scope, and Objectives of the Seminar | 6 |
| | 1.5 Interdisciplinary Alignment with AI&DS Curriculum | 7 |
| | 1.6 Organization of the Report | 8 |
| **Chapter 2** | **Literature Review and Comparative Evaluation** | **9** |
| | 2.1 Evolution of Retrieval Architectures: From Dense to Adaptive | 9 |
| | 2.2 Survey of Existing Adaptive Retrieval Frameworks | 11 |
| | 2.3 Context Distraction & Noise-Induced Hallucination Mechanics | 13 |
| | 2.4 Post-Training Weight Quantization in Edge AI (AWQ vs. GPTQ) | 15 |
| | 2.5 Comparative Literature Survey Matrix | 17 |
| | 2.6 Critical Research Gap and Positioning | 18 |
| **Chapter 3** | **Proposed Methodology and System Architecture** | **19** |
| | 3.1 Architectural Overview & Core Workflow | 19 |
| | 3.2 Prefix Predictive Shannon Entropy Probe Formulation | 21 |
| | 3.3 Dynamic Uncertainty Gating Threshold Mechanism | 23 |
| | 3.4 Dense Vector Retrieval Subsystem with FAISS | 25 |
| | 3.5 Native INT4 AWQ Quantization Integration | 26 |
| | 3.6 Benchmark Datasets and Stratification | 28 |
| | 3.7 Hardware Testbed, Software Requirements & Instrumentation | 29 |
| | 3.8 Statistical Evaluation Protocol | 31 |
| **Chapter 4** | **Results, Empirical Evaluation, and Discussion** | **32** |
| | 4.1 Empirical Prefix Entropy Distributions across Knowledge Tiers | 32 |
| | 4.2 End-to-End Task Performance Benchmark | 34 |
| | 4.3 Hardware Telemetry Profiles: Latency & Energy Conservation | 36 |
| | 4.4 Robustness Under Controlled Context Noise Injection | 38 |
| | 4.5 Ablation Analysis: Prefix Horizon M and Threshold $\tau$ | 40 |
| | 4.6 Quantization Impact: FP16 vs. INT4 AWQ | 42 |
| | 4.7 Qualitative Case Studies & Failure Mode Analysis | 43 |
| | 4.8 Architectural Discussion & Practical Edge Guidelines | 45 |
| **Chapter 5** | **Conclusion and Future Scope** | **47** |
| | 5.1 Summary of Major Findings & Contributions | 47 |
| | 5.2 Fulfillment of Research Objectives | 48 |
| | 5.3 Limitations of the Current Study | 49 |
| | 5.4 Future Work & Next-Generation Directions | 50 |
| | **References** | **51** |
| | **Appendix: Research Publication & Acceptance Certificate** | **54** |

---

## List of Tables

| Table No. | Title | Page No. |
| :--- | :--- | :---: |
| Table 2.1 | Comparative literature survey matrix of selective and adaptive RAG methods | 17 |
| Table 3.1 | Benchmark dataset characteristics and knowledge stratification | 28 |
| Table 3.2 | Hardware testbed and software execution environment specifications | 30 |
| Table 4.1 | Empirical prefix predictive Shannon entropy distribution across query categories | 33 |
| Table 4.2 | End-to-end task performance and hardware telemetry across models and benchmarks | 35 |
| Table 4.3 | Hallucination Error Rate (HER %) under controlled context noise injection | 38 |
| Table 4.4 | Ablation study on prefix horizon M and gating threshold $\tau$ (Llama-3.2-3B) | 40 |
| Table 4.5 | Quantization comparison: FP16 precision vs. INT4 AWQ efficiency | 42 |

---

## List of Figures

| Figure No. | Title | Page No. |
| :--- | :--- | :---: |
| Figure 1.1 | Architectural paradigm comparison: Conventional Always-On RAG vs. Proposed Uncertainty-Gated Selective Retrieval | 2 |
| Figure 3.1 | Comprehensive system architectural flowchart and hardware execution pipeline | 20 |
| Figure 4.1 | Empirical prefix Shannon entropy distributions across Popular and Long-Tail queries for Qwen2.5 and Llama-3.2 | 33 |
| Figure 4.2 | Hallucination Error Rate (HER %) vulnerability curves under controlled context noise injection | 39 |
| Figure 4.3 | Inference latency (ms) and GPU energy consumption (J) benchmarks across models | 37 |

---

## List of Acronyms and Abbreviations

| Acronym / Abbreviation | Expanded Description |
| :--- | :--- |
| **RAG** | Retrieval-Augmented Generation |
| **SLM** | Small Language Model (1B – 8B parameters) |
| **LLM** | Large Language Model |
| **AWQ** | Activation-aware Weight Quantization |
| **FAISS** | Facebook AI Similarity Search |
| **HER** | Hallucination Error Rate (%) |
| **EM** | Exact Match Accuracy (%) |
| **TTFT** | Time-To-First-Token (milliseconds) |
| **CI** | Confidence Interval (Bootstrap 95%) |
| **NQ** | Natural Questions Open-Domain Benchmark |
| **PopQA** | Popularity-Stratified Entity Question Answering Benchmark |
| **CUDA** | Compute Unified Device Architecture (NVIDIA) |
| **VRAM** | Video Random Access Memory |
| **TDP** | Thermal Design Power (Watts) |
| **GPU** | Graphics Processing Unit |
| **CPU** | Central Processing Unit |
| **NVML** | NVIDIA Management Library |
| **NLP** | Natural Language Processing |
| **NLI** | Natural Language Inference |
| **FP16** | 16-bit Half-Precision Floating Point |
| **INT4** | 4-bit Integer Precision Quantization |
| **HOD** | Head of the Department |
| **SPPU** | Savitribai Phule Pune University |
| **JSPM** | Jayawant Shikshan Prasarak Mandal |
| **NTC** | Narhe Technical Campus |

---

# Chapter 1
# Introduction

""" + c.CHAPTER_1_INTRO + """

### 1.1 Introduction and Background of Retrieval-Augmented Generation
""" + c.SEC_1_1 + """

![Figure 1.1: Architectural paradigm comparison](assets/figure1_1_rag_comparison.png)  
**Figure 1.1.** Architectural paradigm comparison: Conventional Always-On RAG vs. Proposed Uncertainty-Gated Selective Retrieval.

### 1.2 Problem Statement & Identified Deficiencies in Static RAG
""" + c.SEC_1_2 + """

### 1.3 Motivation: Edge Computing & Quantized Small Language Models
""" + c.SEC_1_3 + """

### 1.4 Purpose, Scope, and Objectives of the Seminar
""" + c.SEC_1_4 + """

### 1.5 Interdisciplinary Alignment with AI&DS Curriculum
""" + c.SEC_1_5 + """

### 1.6 Organization of the Report
""" + c.SEC_1_6 + """

---

# Chapter 2
# Literature Review and Comparative Evaluation

""" + c.CHAPTER_2_INTRO + """

### 2.1 Evolution of Retrieval Architectures: From Dense to Adaptive
""" + c.SEC_2_1 + """

### 2.2 Survey of Existing Adaptive Retrieval Frameworks
""" + c.SEC_2_2 + """

### 2.3 Context Distraction & Noise-Induced Hallucination Mechanics
""" + c.SEC_2_3 + """

### 2.4 Post-Training Weight Quantization in Edge AI (AWQ vs. GPTQ)
""" + c.SEC_2_4 + """

### 2.5 Comparative Literature Survey Matrix
""" + c.SEC_2_5 + """

**Table 2.1.** Comparative literature survey matrix of selective and adaptive RAG methods

| Method / Reference | Year | Retraining Required? | Latency Overhead | Quantization Compatible? | Key Limitation |
| :--- | :---: | :--- | :--- | :--- | :--- |
| Self-RAG (Asai et al.) [10] | 2024 | Yes (PT) | Low (single pass) | No (modifies weights) | Cannot be applied post-hoc to off-the-shelf models |
| Rowen (Ding et al.) [11] | 2025 | No | Very High (200-400%) | Yes (black-box) | Triples latency; negates SLM efficiency advantage |
| SKR (Wang et al.) [15] | 2023 | Yes (classifier) | Low (single pass) | No (model-specific) | Classifier must be retrained per target LLM family |
| FLARE (Jiang et al.) [16] | 2023 | No | High (multi-pass) | Partial | Frequent rollback and multi-step latency overhead |
| **Ours (Uncertainty-Gated)** | **2026** | **No (training-free)** | **Negligible (<12 ms)** | **Yes (INT4 AWQ native)** | **Threshold calibration needed for new domains** |

### 2.6 Critical Research Gap and Positioning
""" + c.SEC_2_6 + """

---

# Chapter 3
# Proposed Methodology and System Architecture

""" + c.CHAPTER_3_INTRO + """

### 3.1 Overview and System Architecture
""" + c.SEC_3_1 + """

![Figure 3.1: System Architecture](assets/figure3_1_architecture.png)  
**Figure 3.1.** Comprehensive system architectural flowchart and hardware execution pipeline.

### 3.2 Prefix Predictive Shannon Entropy Probe Formulation
""" + c.SEC_3_2 + """

### 3.3 Dynamic Uncertainty Gating Threshold Mechanism
""" + c.SEC_3_3 + """

### 3.4 Dense Vector Retrieval Subsystem with FAISS
""" + c.SEC_3_4 + """

### 3.5 Native INT4 AWQ Quantization Integration
""" + c.SEC_3_5 + """

### 3.6 Benchmark Datasets and Stratification
""" + c.SEC_3_6 + """

**Table 3.1.** Benchmark dataset characteristics and knowledge stratification

| Dataset Name | Total Queries | Domain / Knowledge Type | Stratification Feature / Role |
| :--- | :---: | :--- | :--- |
| PopQA [19] | 14,267 | Factual Entity Knowledge | Stratified by monthly Wikipedia pageviews (Popular vs. Long-Tail) |
| Natural Questions (NQ-Open) [20] | 3,610 | Real User Search Queries | Uncurated open-domain Google queries with verified gold answers |
| TruthfulQA [21] | 817 | Adversarial Misconceptions | Designed to trigger imitation false beliefs and human superstitions |

### 3.7 Hardware Testbed, Software Requirements & Instrumentation
""" + c.SEC_3_7 + """

**Table 3.2.** Hardware testbed and software execution environment specifications

| Subsystem / Component | Hardware Specification | Role in Benchmark Execution |
| :--- | :--- | :--- |
| Host Processor (CPU) | Intel Core i9-14900K (24 cores / 32 threads) | Orchestration, tokenization, batch control |
| Host Memory (RAM) | 64 GB DDR5-5600 MT/s (Dual Channel) | FAISS vector index in-memory residency (8.5 GB) |
| Primary GPU Accelerator | NVIDIA GeForce RTX 4090 (Ada Lovelace) | FP16 & INT4 AWQ model inference execution |
| GPU VRAM & Bandwidth | 24 GB GDDR6X @ 1,008 GB/s (384-bit bus) | KV-cache and model weight allocation without paging |
| Thermal Power Envelope | 450 W base power ceiling | Dynamic physical power draw profiling |
| Local Solid-State Storage | 2 TB PCIe 4.0 NVMe SSD (7,000 MB/s read) | Vector database cold-start index retrieval |
| Software Compute Stack | CUDA 12.4, cuDNN 9.1, PyTorch 2.15 | Kernel execution and tensor operations |
| Model Execution Framework | Hugging Face Transformers 5.22, Accelerate | Model orchestration and AWQ kernel dispatch |
| Power Telemetry Daemon | NVIDIA Management Library (pynvml v11.5.0) | 50 ms continuous background polling thread |
| Latency Synchronization | torch.cuda.Event(enable_timing=True) | Microsecond-accurate kernel latency capture |

### 3.8 Statistical Evaluation Protocol
""" + c.SEC_3_8 + """

---

# Chapter 4
# Results, Empirical Evaluation, and Discussion

""" + c.CHAPTER_4_INTRO + """

### 4.1 Empirical Prefix Entropy Distributions across Knowledge Tiers
""" + c.SEC_4_1 + """

**Table 4.1.** Empirical prefix predictive Shannon entropy distribution across query categories

| Model Architecture | Query Category | Mean Entropy (nats) | Std Dev | Min | Max | 95% Bootstrap CI |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Qwen2.5-0.5B | Popular Entities | 0.809 | 0.342 | 0.018 | 1.211 | [0.724, 0.898] |
| Qwen2.5-0.5B | Long-Tail Entities | 2.369 | 1.285 | 0.456 | 5.417 | [2.012, 2.745] |
| Qwen2.5-0.5B | **Separation $\Delta \mathcal{U}$** | **1.560 nats** | - | - | - | **[1.240, 1.885] (p < 10^-11)** |
| Llama-3.2-3B | Popular Entities | 0.684 | 0.291 | 0.012 | 1.104 | [0.612, 0.758] |
| Llama-3.2-3B | Long-Tail Entities | 2.512 | 1.310 | 0.512 | 5.680 | [2.145, 2.890] |
| Llama-3.2-3B | **Separation $\Delta \mathcal{U}$** | **1.828 nats** | - | - | - | **[1.482, 2.180] (p < 10^-13)** |

![Figure 4.1: Empirical Entropy Distributions](assets/figure4_1_entropy_distribution.png)  
**Figure 4.1.** Empirical prefix Shannon entropy distributions across Popular and Long-Tail queries for Qwen2.5 and Llama-3.2.

### 4.2 End-to-End Task Performance Benchmark
""" + c.SEC_4_2 + """

**Table 4.2.** End-to-end task performance and hardware telemetry across models and benchmarks

| Model / Setup | PopQA (EM %) | NQ (F1 %) | TruthfulQA (%) | Mean Latency (ms) | Energy / Query (J) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Qwen2.5-0.5B-Instruct** | | | | | |
| &nbsp;&nbsp;Closed-Book Baseline | 28.4 | 20.1 | 36.2 | 42.1 [39, 45] | 8.4 [7.8, 9.1] |
| &nbsp;&nbsp;Naive Static RAG | 51.2 | 38.6 | 47.5 | 194.2 [185, 203] | 41.2 [38.5, 43.8] |
| &nbsp;&nbsp;**Uncertainty-Gated (Ours)** | **54.1** | **40.4** | **51.8** | **120.1 [114, 126]** | **28.2 [26.1, 30.4]** |
| **Qwen2.5-1.5B-Instruct** | | | | | |
| &nbsp;&nbsp;Closed-Book Baseline | 31.4 | 22.8 | 38.6 | 68.2 [64, 72] | 12.4 [11.5, 13.3] |
| &nbsp;&nbsp;Naive Static RAG | 54.2 | 41.5 | 49.2 | 284.6 [271, 298] | 58.7 [55.2, 62.1] |
| &nbsp;&nbsp;**Uncertainty-Gated (Ours)** | **56.8** | **42.9** | **53.4** | **175.4 [166, 184]** | **39.8 [37.2, 42.5]** |
| **Llama-3.2-3B-Instruct** | | | | | |
| &nbsp;&nbsp;Closed-Book Baseline | 39.8 | 29.4 | 44.1 | 94.5 [89, 100] | 18.6 [17.2, 19.9] |
| &nbsp;&nbsp;Naive Static RAG | 61.2 | 48.7 | 56.8 | 362.1 [345, 379] | 79.4 [74.8, 84.1] |
| &nbsp;&nbsp;**Uncertainty-Gated (Ours)** | **64.5** | **50.2** | **61.9** | **224.8 [214, 235]** | **54.2 [51.0, 57.5]** |
| **Gemma-2-2B-IT** | | | | | |
| &nbsp;&nbsp;Closed-Book Baseline | 36.2 | 26.5 | 42.0 | 82.1 [77, 87] | 15.8 [14.6, 17.0] |
| &nbsp;&nbsp;Naive Static RAG | 58.4 | 45.1 | 52.6 | 318.5 [302, 335] | 68.2 [64.1, 72.3] |
| &nbsp;&nbsp;**Uncertainty-Gated (Ours)** | **60.9** | **46.8** | **57.1** | **196.2 [186, 206]** | **46.7 [43.9, 49.6]** |

*Note: Bracketed intervals indicate 95% bootstrap confidence intervals (10,000 resamples).*

### 4.3 Hardware Telemetry Profiles: Latency & Energy Conservation
""" + c.SEC_4_3 + """

![Figure 4.3: Latency and Energy Savings](assets/figure4_3_latency_energy.png)  
**Figure 4.3.** Inference latency (ms) and GPU energy consumption (J) benchmarks across models.

### 4.4 Robustness Under Controlled Context Noise Injection
""" + c.SEC_4_4 + """

**Table 4.3.** Hallucination Error Rate (HER %) under controlled context noise injection

| Evaluation Method | 0% Noise (Clean) | 25% Noise (Low) | 50% Noise (High) | 100% Contradictory |
| :--- | :---: | :---: | :---: | :---: |
| Closed-Book Baseline | 56.2% | 56.2% | 56.2% | 56.2% |
| Naive Static RAG | 18.4% | 27.9% | 44.8% | 68.4% |
| Rowen (Ding et al., 2025) [11] | 19.1% | 24.2% | 33.5% | 46.2% |
| **Uncertainty-Gated RAG (Ours)** | **17.9%** | **21.4%** | **28.2%** | **39.1%** |

![Figure 4.2: Hallucination Error Rate vs Noise](assets/figure4_2_hallucination_noise.png)  
**Figure 4.2.** Hallucination Error Rate (HER %) vulnerability curves under controlled context noise injection.

### 4.5 Ablation Analysis: Prefix Horizon M and Threshold $\tau$
""" + c.SEC_4_5 + """

**Table 4.4.** Ablation study on prefix horizon M and gating threshold $\tau$ (Llama-3.2-3B on PopQA)

| Prefix Horizon M | Threshold $\tau$ (nats) | PopQA EM (%) | Bypass Rate (%) | Gating Latency (ms) | Total Latency (ms) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| M = 1 | $\tau$ = 2.0 | 59.8 | 61.2 | 4.2 | 245.1 |
| M = 2 | $\tau$ = 2.0 | 62.4 | 70.5 | 8.1 | 231.8 |
| **M = 3 (Optimal)** | **$\tau$ = 2.0** | **64.5** | **74.8** | **12.4** | **224.8** |
| M = 4 | $\tau$ = 2.0 | 64.6 | 75.1 | 16.8 | 229.4 |
| M = 5 | $\tau$ = 2.0 | 64.7 | 75.4 | 21.2 | 234.1 |
| M = 3 | $\tau$ = 1.6 | 61.8 | 58.2 | 12.4 | 262.1 |
| M = 3 | $\tau$ = 1.8 | 63.4 | 67.4 | 12.4 | 241.5 |
| **M = 3 (Optimal)** | **$\tau$ = 2.0** | **64.5** | **74.8** | **12.4** | **224.8** |
| M = 3 | $\tau$ = 2.2 | 62.9 | 81.6 | 12.4 | 211.2 |
| M = 3 | $\tau$ = 2.4 | 60.1 | 88.2 | 12.4 | 198.5 |

### 4.6 Quantization Impact: FP16 vs. INT4 AWQ
""" + c.SEC_4_6 + """

**Table 4.5.** Quantization comparison: FP16 precision vs. INT4 AWQ efficiency

| Model / Precision Configuration | VRAM Footprint (GB) | PopQA EM (%) | Mean Entropy (Pop) | Mean Entropy (Tail) | Separation $\Delta \mathcal{U}$ (nats) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Llama-3.2-3B (FP16) | 6.4 | 64.5 | 0.684 | 2.512 | 1.828 |
| Llama-3.2-3B (INT4 AWQ) | 2.2 | 63.1 | 0.862 | 2.648 | 1.786 |
| Qwen2.5-1.5B (FP16) | 3.2 | 56.8 | 0.809 | 2.369 | 1.560 |
| Qwen2.5-1.5B (INT4 AWQ) | 1.1 | 55.4 | 0.978 | 2.491 | 1.513 |

### 4.7 Qualitative Case Studies & Failure Mode Analysis
""" + c.SEC_4_7 + """

### 4.8 Architectural Discussion & Practical Edge Guidelines
""" + c.SEC_4_8 + """

---

# Chapter 5
# Conclusion and Future Scope

""" + c.CHAPTER_5_INTRO + """

### 5.1 Summary of Major Findings & Contributions
""" + c.SEC_5_1 + """

### 5.2 Fulfillment of Research Objectives
""" + c.SEC_5_2 + """

### 5.3 Limitations of the Current Study
""" + c.SEC_5_3 + """

### 5.4 Future Work & Next-Generation Directions
""" + c.SEC_5_4 + """

---

# References

""" + "\n\n".join(c.REFERENCES_LIST) + """

---

# Appendix: Research Publication and Acceptance

""" + c.APPENDIX_TEXT + """
""")

with open(MD_OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"Generated Markdown Seminar Report: {MD_OUT}")

