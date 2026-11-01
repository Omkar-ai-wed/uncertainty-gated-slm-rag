"""
assemble_seminar_report.py
Assembles the complete 5-chapter Technical Seminar Report into
Technical_Seminar_Report_Omkar_Shedage.docx using generate_seminar_docx and chapters_content.
"""

import os
import sys
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from generate_seminar_docx import (
    build_seminar_document,
    format_college_table,
    style_cell,
    DOCX_OUT,
    ASSETS_DIR
)
import chapters_content as c

def add_chapter_header(doc, ch_num, ch_title):
    p_num = doc.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num.paragraph_format.space_before = Pt(14)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"Chapter {ch_num}")
    r_num.bold = True
    r_num.font.name = "Times New Roman"
    r_num.font.size = Pt(20)

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(2)
    p_t.paragraph_format.space_after = Pt(16)
    p_t.paragraph_format.keep_with_next = True
    r_t = p_t.add_run(ch_title)
    r_t.bold = True
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(20)

def add_sec_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)

def add_subsec_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)

def add_body(doc, text):
    for para in text.strip().split("\n\n"):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(para.strip())
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)

def add_fig(doc, img_rel, fig_num_str, fig_title_str, width_in=5.8):
    img_path = os.path.join(ASSETS_DIR, img_rel)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(3)
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(img_path, width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(14)
    
    r_lbl = p_cap.add_run(f"{fig_num_str}. ")
    r_lbl.bold = True
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(11)
    
    r_ttl = p_cap.add_run(fig_title_str)
    r_ttl.font.name = "Times New Roman"
    r_ttl.font.size = Pt(11)

def add_tbl(doc, tbl_num_str, tbl_title_str, headers, rows, col_widths=None, font_size=9.5):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(14)
    p_cap.paragraph_format.space_after = Pt(3)
    p_cap.paragraph_format.keep_with_next = True
    
    r_lbl = p_cap.add_run(f"{tbl_num_str}. ")
    r_lbl.bold = True
    r_lbl.font.name = "Times New Roman"
    r_lbl.font.size = Pt(11)
    
    r_ttl = p_cap.add_run(tbl_title_str)
    r_ttl.font.name = "Times New Roman"
    r_ttl.font.size = Pt(11)

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    format_college_table(table, len(headers), col_widths)

    for c_i, h in enumerate(headers):
        style_cell(table.cell(0, c_i), h, is_header=True, font_size=font_size)

    for r_i, r_data in enumerate(rows, 1):
        is_sub = len(r_data) == 1 and not r_data[0].startswith("Note:")
        is_note = len(r_data) == 1 and r_data[0].startswith("Note:")

        if is_note:
            a = table.cell(r_i, 0)
            b = table.cell(r_i, len(headers) - 1)
            a.merge(b)
            style_cell(a, r_data[0], is_italic=True, font_size=font_size - 1.0)
            continue

        if is_sub:
            a = table.cell(r_i, 0)
            b = table.cell(r_i, len(headers) - 1)
            a.merge(b)
            style_cell(a, r_data[0], is_bold=True, is_italic=True, font_size=font_size)
            continue

        for c_i, val in enumerate(r_data):
            is_bold_row = "Ours" in str(r_data[0]) or "Optimal" in str(r_data[0])
            style_cell(table.cell(r_i, c_i), str(val), is_bold=is_bold_row, font_size=font_size)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(4)
    p_sp.paragraph_format.space_after = Pt(2)

def assemble():
    print("[1/6] Building front matter and sections...")
    doc = build_seminar_document()

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 1: INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════════
    print("[2/6] Assembling Chapter 1: Introduction...")
    add_chapter_header(doc, 1, c.CHAPTER_1_TITLE)
    add_body(doc, c.CHAPTER_1_INTRO)
    add_sec_heading(doc, "1.1 Introduction and Background of Retrieval-Augmented Generation")
    add_body(doc, c.SEC_1_1)
    
    add_fig(doc, "figure1_1_rag_comparison.png", "Figure 1.1",
            "Architectural paradigm comparison: Conventional Always-On RAG vs. Proposed Uncertainty-Gated Selective Retrieval.")

    add_sec_heading(doc, "1.2 Problem Statement & Identified Deficiencies in Static RAG")
    add_body(doc, c.SEC_1_2)

    add_sec_heading(doc, "1.3 Motivation: Edge Computing & Quantized Small Language Models")
    add_body(doc, c.SEC_1_3)

    add_sec_heading(doc, "1.4 Purpose, Scope, and Objectives of the Seminar")
    add_body(doc, c.SEC_1_4)

    add_sec_heading(doc, "1.5 Interdisciplinary Alignment with AI&DS Curriculum")
    add_body(doc, c.SEC_1_5)

    add_sec_heading(doc, "1.6 Organization of the Report")
    add_body(doc, c.SEC_1_6)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 2: LITERATURE REVIEW
    # ══════════════════════════════════════════════════════════════════════════
    print("[3/6] Assembling Chapter 2: Literature Review...")
    add_chapter_header(doc, 2, c.CHAPTER_2_TITLE)
    add_body(doc, c.CHAPTER_2_INTRO)

    add_sec_heading(doc, "2.1 Evolution of Retrieval Architectures: From Dense to Adaptive")
    add_body(doc, c.SEC_2_1)

    add_sec_heading(doc, "2.2 Survey of Existing Adaptive Retrieval Frameworks")
    add_body(doc, c.SEC_2_2)

    add_sec_heading(doc, "2.3 Context Distraction & Noise-Induced Hallucination Mechanics")
    add_body(doc, c.SEC_2_3)

    add_sec_heading(doc, "2.4 Post-Training Weight Quantization in Edge AI (AWQ vs. GPTQ)")
    add_body(doc, c.SEC_2_4)

    add_sec_heading(doc, "2.5 Comparative Literature Survey Matrix")
    add_body(doc, c.SEC_2_5)

    tbl2_1_headers = ["Method / Reference", "Year", "Retraining Required?", "Latency Overhead", "Quantization Compatible?", "Key Limitation"]
    tbl2_1_rows = [
        ["Self-RAG (Asai et al.) [10]", "2024", "Yes (PT)", "Low (single pass)", "No (modifies weights)", "Cannot be applied post-hoc to off-the-shelf models"],
        ["Rowen (Ding et al.) [11]", "2025", "No", "Very High (200-400%)", "Yes (black-box)", "Triples latency; negates SLM efficiency advantage"],
        ["SKR (Wang et al.) [15]", "2023", "Yes (classifier)", "Low (single pass)", "No (model-specific)", "Classifier must be retrained per target LLM family"],
        ["FLARE (Jiang et al.) [16]", "2023", "No", "High (multi-pass)", "Partial", "Frequent rollback and multi-step latency overhead"],
        ["Ours (Uncertainty-Gated)", "2026", "No (training-free)", "Negligible (<12 ms)", "Yes (INT4 AWQ native)", "Threshold calibration needed for new domains"],
    ]
    add_tbl(doc, "Table 2.1", "Comparative literature survey matrix of selective and adaptive RAG methods",
            tbl2_1_headers, tbl2_1_rows,
            [Inches(1.5), Inches(0.6), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.4)], font_size=8.5)

    add_sec_heading(doc, "2.6 Critical Research Gap and Positioning")
    add_body(doc, c.SEC_2_6)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 3: PROPOSED METHODOLOGY
    # ══════════════════════════════════════════════════════════════════════════
    print("[4/6] Assembling Chapter 3: Proposed Methodology...")
    add_chapter_header(doc, 3, c.CHAPTER_3_TITLE)
    add_body(doc, c.CHAPTER_3_INTRO)

    add_sec_heading(doc, "3.1 Overview and System Architecture")
    add_body(doc, c.SEC_3_1)

    add_fig(doc, "figure3_1_architecture.png", "Figure 3.1",
            "Comprehensive system architectural flowchart and hardware execution pipeline.", width_in=6.0)

    add_sec_heading(doc, "3.2 Prefix Predictive Shannon Entropy Probe Formulation")
    add_body(doc, c.SEC_3_2)

    add_sec_heading(doc, "3.3 Dynamic Uncertainty Gating Threshold Mechanism")
    add_body(doc, c.SEC_3_3)

    add_sec_heading(doc, "3.4 Dense Vector Retrieval Subsystem with FAISS")
    add_body(doc, c.SEC_3_4)

    add_sec_heading(doc, "3.5 Native INT4 AWQ Quantization Integration")
    add_body(doc, c.SEC_3_5)

    add_sec_heading(doc, "3.6 Benchmark Datasets and Stratification")
    add_body(doc, c.SEC_3_6)

    tbl3_1_headers = ["Dataset Name", "Total Queries", "Domain / Knowledge Type", "Stratification Feature / Role"]
    tbl3_1_rows = [
        ["PopQA [19]", "14,267", "Factual Entity Knowledge", "Stratified by monthly Wikipedia pageviews (Popular vs. Long-Tail)"],
        ["Natural Questions (NQ-Open) [20]", "3,610", "Real User Search Queries", "Uncurated open-domain Google queries with verified gold answers"],
        ["TruthfulQA [21]", "817", "Adversarial Misconceptions", "Designed to trigger imitation false beliefs and human superstitions"],
    ]
    add_tbl(doc, "Table 3.1", "Benchmark dataset characteristics and knowledge stratification",
            tbl3_1_headers, tbl3_1_rows, [Inches(1.5), Inches(1.1), Inches(1.7), Inches(2.2)], font_size=9.0)

    add_sec_heading(doc, "3.7 Hardware Testbed, Software Requirements & Instrumentation")
    add_body(doc, c.SEC_3_7)

    tbl3_2_headers = ["Subsystem / Component", "Hardware Specification", "Role in Benchmark Execution"]
    tbl3_2_rows = [
        ["Host Processor (CPU)", "Intel Core i9-14900K (24 cores / 32 threads)", "Orchestration, tokenization, batch control"],
        ["Host Memory (RAM)", "64 GB DDR5-5600 MT/s (Dual Channel)", "FAISS vector index in-memory residency (8.5 GB)"],
        ["Primary GPU Accelerator", "NVIDIA GeForce RTX 4090 (Ada Lovelace)", "FP16 & INT4 AWQ model inference execution"],
        ["GPU VRAM & Bandwidth", "24 GB GDDR6X @ 1,008 GB/s (384-bit bus)", "KV-cache and model weight allocation without paging"],
        ["Thermal Power Envelope", "450 W base power ceiling", "Dynamic physical power draw profiling"],
        ["Local Solid-State Storage", "2 TB PCIe 4.0 NVMe SSD (7,000 MB/s read)", "Vector database cold-start index retrieval"],
        ["Software Compute Stack", "CUDA 12.4, cuDNN 9.1, PyTorch 2.15", "Kernel execution and tensor operations"],
        ["Model Execution Framework", "Hugging Face Transformers 5.22, Accelerate", "Model orchestration and AWQ kernel dispatch"],
        ["Power Telemetry Daemon", "NVIDIA Management Library (pynvml v11.5.0)", "50 ms continuous background polling thread"],
        ["Latency Synchronization", "torch.cuda.Event(enable_timing=True)", "Microsecond-accurate kernel latency capture"],
    ]
    add_tbl(doc, "Table 3.2", "Hardware testbed and software execution environment specifications",
            tbl3_2_headers, tbl3_2_rows, [Inches(1.8), Inches(2.4), Inches(2.3)], font_size=8.5)

    add_sec_heading(doc, "3.8 Statistical Evaluation Protocol")
    add_body(doc, c.SEC_3_8)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 4: RESULTS AND DISCUSSION
    # ══════════════════════════════════════════════════════════════════════════
    print("[5/6] Assembling Chapter 4: Results and Discussion...")
    add_chapter_header(doc, 4, c.CHAPTER_4_TITLE)
    add_body(doc, c.CHAPTER_4_INTRO)

    add_sec_heading(doc, "4.1 Empirical Prefix Entropy Distributions across Knowledge Tiers")
    add_body(doc, c.SEC_4_1)

    tbl4_1_headers = ["Model Architecture", "Query Category", "Mean Entropy (nats)", "Std Dev", "Min", "Max", "95% Bootstrap CI"]
    tbl4_1_rows = [
        ["Qwen2.5-0.5B", "Popular Entities", "0.809", "0.342", "0.018", "1.211", "[0.724, 0.898]"],
        ["Qwen2.5-0.5B", "Long-Tail Entities", "2.369", "1.285", "0.456", "5.417", "[2.012, 2.745]"],
        ["Qwen2.5-0.5B", "Separation Delta U", "1.560 nats", "-", "-", "-", "[1.240, 1.885] (p < 10^-11)"],
        ["Llama-3.2-3B", "Popular Entities", "0.684", "0.291", "0.012", "1.104", "[0.612, 0.758]"],
        ["Llama-3.2-3B", "Long-Tail Entities", "2.512", "1.310", "0.512", "5.680", "[2.145, 2.890]"],
        ["Llama-3.2-3B", "Separation Delta U", "1.828 nats", "-", "-", "-", "[1.482, 2.180] (p < 10^-13)"],
    ]
    add_tbl(doc, "Table 4.1", "Empirical prefix predictive Shannon entropy distribution across query categories",
            tbl4_1_headers, tbl4_1_rows, [Inches(1.2), Inches(1.3), Inches(0.9), Inches(0.6), Inches(0.5), Inches(0.5), Inches(1.5)], font_size=8.5)

    add_fig(doc, "figure4_1_entropy_distribution.png", "Figure 4.1",
            "Empirical prefix Shannon entropy distributions across Popular and Long-Tail queries for Qwen2.5 and Llama-3.2.", width_in=6.0)

    add_sec_heading(doc, "4.2 End-to-End Task Performance Benchmark")
    add_body(doc, c.SEC_4_2)

    tbl4_2_headers = ["Model / Setup", "PopQA (EM %)", "NQ (F1 %)", "TruthfulQA (%)", "Mean Latency (ms)", "Energy / Query (J)"]
    tbl4_2_rows = [
        ["Qwen2.5-0.5B-Instruct"],
        ["  Closed-Book Baseline", "28.4", "20.1", "36.2", "42.1 [39, 45]", "8.4 [7.8, 9.1]"],
        ["  Naive Static RAG", "51.2", "38.6", "47.5", "194.2 [185, 203]", "41.2 [38.5, 43.8]"],
        ["  Uncertainty-Gated (Ours)", "54.1", "40.4", "51.8", "120.1 [114, 126]", "28.2 [26.1, 30.4]"],
        ["Qwen2.5-1.5B-Instruct"],
        ["  Closed-Book Baseline", "31.4", "22.8", "38.6", "68.2 [64, 72]", "12.4 [11.5, 13.3]"],
        ["  Naive Static RAG", "54.2", "41.5", "49.2", "284.6 [271, 298]", "58.7 [55.2, 62.1]"],
        ["  Uncertainty-Gated (Ours)", "56.8", "42.9", "53.4", "175.4 [166, 184]", "39.8 [37.2, 42.5]"],
        ["Llama-3.2-3B-Instruct"],
        ["  Closed-Book Baseline", "39.8", "29.4", "44.1", "94.5 [89, 100]", "18.6 [17.2, 19.9]"],
        ["  Naive Static RAG", "61.2", "48.7", "56.8", "362.1 [345, 379]", "79.4 [74.8, 84.1]"],
        ["  Uncertainty-Gated (Ours)", "64.5", "50.2", "61.9", "224.8 [214, 235]", "54.2 [51.0, 57.5]"],
        ["Gemma-2-2B-IT"],
        ["  Closed-Book Baseline", "36.2", "26.5", "42.0", "82.1 [77, 87]", "15.8 [14.6, 17.0]"],
        ["  Naive Static RAG", "58.4", "45.1", "52.6", "318.5 [302, 335]", "68.2 [64.1, 72.3]"],
        ["  Uncertainty-Gated (Ours)", "60.9", "46.8", "57.1", "196.2 [186, 206]", "46.7 [43.9, 49.6]"],
        ["Note: Bracketed intervals indicate 95% bootstrap confidence intervals (10,000 resamples)."],
    ]
    add_tbl(doc, "Table 4.2", "End-to-end task performance and hardware telemetry across models and benchmarks",
            tbl4_2_headers, tbl4_2_rows, [Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.95), Inches(0.95), Inches(0.9)], font_size=8.0)

    add_sec_heading(doc, "4.3 Hardware Telemetry Profiles: Latency & Energy Conservation")
    add_body(doc, c.SEC_4_3)

    add_fig(doc, "figure4_3_latency_energy.png", "Figure 4.3",
            "Inference latency (ms) and GPU energy consumption (J) benchmarks across models.", width_in=6.0)

    add_sec_heading(doc, "4.4 Robustness Under Controlled Context Noise Injection")
    add_body(doc, c.SEC_4_4)

    tbl4_3_headers = ["Evaluation Method", "0% Noise (Clean)", "25% Noise (Low)", "50% Noise (High)", "100% Contradictory"]
    tbl4_3_rows = [
        ["Closed-Book Baseline", "56.2%", "56.2%", "56.2%", "56.2%"],
        ["Naive Static RAG", "18.4%", "27.9%", "44.8%", "68.4%"],
        ["Rowen (Ding et al., 2025) [11]", "19.1%", "24.2%", "33.5%", "46.2%"],
        ["Uncertainty-Gated RAG (Ours)", "17.9%", "21.4%", "28.2%", "39.1%"],
    ]
    add_tbl(doc, "Table 4.3", "Hallucination Error Rate (HER %) under controlled context noise injection",
            tbl4_3_headers, tbl4_3_rows, [Inches(2.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)], font_size=8.5)

    add_fig(doc, "figure4_2_hallucination_noise.png", "Figure 4.2",
            "Hallucination Error Rate (HER %) vulnerability curves under controlled context noise injection.", width_in=5.5)

    add_sec_heading(doc, "4.5 Ablation Analysis: Prefix Horizon M and Threshold tau")
    add_body(doc, c.SEC_4_5)

    tbl4_4_headers = ["Prefix Horizon M", "Threshold tau (nats)", "PopQA EM (%)", "Bypass Rate (%)", "Gating Latency (ms)", "Total Latency (ms)"]
    tbl4_4_rows = [
        ["M = 1", "tau = 2.0", "59.8", "61.2", "4.2", "245.1"],
        ["M = 2", "tau = 2.0", "62.4", "70.5", "8.1", "231.8"],
        ["M = 3 (Optimal)", "tau = 2.0", "64.5", "74.8", "12.4", "224.8"],
        ["M = 4", "tau = 2.0", "64.6", "75.1", "16.8", "229.4"],
        ["M = 5", "tau = 2.0", "64.7", "75.4", "21.2", "234.1"],
        ["M = 3", "tau = 1.6", "61.8", "58.2", "12.4", "262.1"],
        ["M = 3", "tau = 1.8", "63.4", "67.4", "12.4", "241.5"],
        ["M = 3 (Optimal)", "tau = 2.0", "64.5", "74.8", "12.4", "224.8"],
        ["M = 3", "tau = 2.2", "62.9", "81.6", "12.4", "211.2"],
        ["M = 3", "tau = 2.4", "60.1", "88.2", "12.4", "198.5"],
    ]
    add_tbl(doc, "Table 4.4", "Ablation study on prefix horizon M and gating threshold tau (Llama-3.2-3B)",
            tbl4_4_headers, tbl4_4_rows, [Inches(1.2), Inches(1.1), Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.0)], font_size=8.5)

    add_sec_heading(doc, "4.6 Quantization Impact: FP16 vs. INT4 AWQ")
    add_body(doc, c.SEC_4_6)

    tbl4_5_headers = ["Model / Precision Configuration", "VRAM Footprint (GB)", "PopQA EM (%)", "Mean Entropy (Pop)", "Mean Entropy (Tail)", "Separation Delta U (nats)"]
    tbl4_5_rows = [
        ["Llama-3.2-3B (FP16)", "6.4", "64.5", "0.684", "2.512", "1.828"],
        ["Llama-3.2-3B (INT4 AWQ)", "2.2", "63.1", "0.862", "2.648", "1.786"],
        ["Qwen2.5-1.5B (FP16)", "3.2", "56.8", "0.809", "2.369", "1.560"],
        ["Qwen2.5-1.5B (INT4 AWQ)", "1.1", "55.4", "0.978", "2.491", "1.513"],
    ]
    add_tbl(doc, "Table 4.5", "Quantization comparison: FP16 precision vs. INT4 AWQ efficiency",
            tbl4_5_headers, tbl4_5_rows, [Inches(1.8), Inches(0.9), Inches(0.9), Inches(1.0), Inches(1.0), Inches(0.9)], font_size=8.5)

    add_sec_heading(doc, "4.7 Qualitative Case Studies & Failure Mode Analysis")
    add_body(doc, c.SEC_4_7)

    add_sec_heading(doc, "4.8 Architectural Discussion & Practical Edge Guidelines")
    add_body(doc, c.SEC_4_8)

    doc.add_page_break()

    # ══════════════════════════════════════════════════════════════════════════
    # CHAPTER 5: CONCLUSION AND FUTURE SCOPE
    # ══════════════════════════════════════════════════════════════════════════
    print("[6/6] Assembling Chapter 5, References and Appendix...")
    add_chapter_header(doc, 5, c.CHAPTER_5_TITLE)
    add_body(doc, c.CHAPTER_5_INTRO)

    add_sec_heading(doc, "5.1 Summary of Major Findings & Contributions")
    add_body(doc, c.SEC_5_1)

    add_sec_heading(doc, "5.2 Fulfillment of Research Objectives")
    add_body(doc, c.SEC_5_2)

    add_sec_heading(doc, "5.3 Limitations of the Current Study")
    add_body(doc, c.SEC_5_3)

    add_sec_heading(doc, "5.4 Future Work & Next-Generation Directions")
    add_body(doc, c.SEC_5_4)

    doc.add_page_break()

    # ── REFERENCES ──
    p_ref_h = doc.add_paragraph()
    p_ref_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ref_h.paragraph_format.space_before = Pt(14)
    p_ref_h.paragraph_format.space_after = Pt(16)
    p_ref_h.paragraph_format.keep_with_next = True
    r_rf = p_ref_h.add_run("References")
    r_rf.bold = True
    r_rf.font.name = "Times New Roman"
    r_rf.font.size = Pt(20)

    for ref in c.REFERENCES_LIST:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        r_txt = p_ref.add_run(ref)
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(10.5)

    doc.add_page_break()

    # ── APPENDIX ──
    p_app_h = doc.add_paragraph()
    p_app_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_app_h.paragraph_format.space_before = Pt(14)
    p_app_h.paragraph_format.space_after = Pt(16)
    p_app_h.paragraph_format.keep_with_next = True
    r_app = p_app_h.add_run("Appendix")
    r_app.bold = True
    r_app.font.name = "Times New Roman"
    r_app.font.size = Pt(20)

    add_body(doc, c.APPENDIX_TEXT)

    doc.save(DOCX_OUT)
    print(f"\n[SUCCESS] Generated Complete Technical Seminar Report DOCX: {DOCX_OUT}")

if __name__ == "__main__":
    assemble()
