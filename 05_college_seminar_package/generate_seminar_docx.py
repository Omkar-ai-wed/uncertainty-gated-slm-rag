"""
generate_seminar_docx.py
Compiles the complete Technical Seminar Report for Omkar Sachin Shedage
Department of AI&DS Engineering, JSPM's Narhe Technical Campus, Pune
Savitribai Phule Pune University (SPPU).

Strictly follows:
- c:\\Users\\Omkar Shedage\\Downloads\\Technical Seminar report format .docx
- c:\\Users\\Omkar Shedage\\Downloads\\Technical_Seminar_Report_Onkar_Kharat_TE39.docx
- Font: Times New Roman throughout
- Chapter Headings: 20pt Bold Centered
- Section Headings: 16pt Bold Left
- Sub-section Headings: 14pt Regular/Bold Left
- Body Text: 12pt Regular, 1.5 Line Spacing, Justified
- Tables: Full-width, 3-line borders, centered Table a.b captions
- Figures: Centered, 300 DPI, centered Figure a.b captions
- Pagination:
  * Section 0 (Cover & Certificate): No page numbers
  * Section 1 (Front Matter): Roman numerals (i, ii, iii...)
  * Section 2 (Chapters 1 to 5 + References + Appendix): Arabic numerals (1, 2, 3...)
"""

import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"d:\play\RAG\05_college_seminar_package"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DOCX_OUT = os.path.join(BASE_DIR, "Technical_Seminar_Report_Omkar_Shedage.docx")

def apply_table_borders(table, border_color="000000"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
      <w:top w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>
      <w:left w:val="none"/>
      <w:bottom w:val="single" w:sz="8" w:space="0" w:color="{border_color}"/>
      <w:right w:val="none"/>
      <w:insideH w:val="none"/>
      <w:insideV w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def apply_header_bottom_border(row, border_color="000000"):
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

def format_college_table(word_tbl, num_cols, col_widths=None):
    word_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    word_tbl.autofit = False
    
    tblPr = word_tbl._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblW'):
            tblPr.remove(child)
    tblW_xml = parse_xml(f'<w:tblW {nsdecls("w")} w:w="9360" w:type="dxa"/>')
    tblPr.append(tblW_xml)
    
    apply_table_borders(word_tbl)
    if len(word_tbl.rows) > 0:
        apply_header_bottom_border(word_tbl.rows[0])
        
    if col_widths is None or len(col_widths) != num_cols:
        col_w = Inches(6.5 / num_cols)
        col_widths = [col_w] * num_cols
    else:
        col_widths = [w if hasattr(w, 'emu') else Inches(w) for w in col_widths]
        
    for r_idx, row in enumerate(word_tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for c_idx, cell in enumerate(row.cells):
            if c_idx < len(col_widths):
                cell.width = col_widths[c_idx]

def style_cell(cell, text, is_header=False, is_bold=False, is_italic=False, font_size=10.0, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    
    run = p.runs[0] if p.runs else p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(font_size)
    run.font.color.rgb = RGBColor(0, 0, 0)
    
    if is_header or is_bold:
        run.bold = True
    if is_italic:
        run.italic = True
        
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
    <w:tcMar {nsdecls("w")}>
      <w:top w:w="60" w:type="dxa"/>
      <w:bottom w:w="60" w:type="dxa"/>
      <w:left w:w="100" w:type="dxa"/>
      <w:right w:w="100" w:type="dxa"/>
    </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_page_number_field(run):
    fldSimple = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
    run._r.append(fldSimple)

def build_seminar_document():
    doc = Document()
    
    # ── DEFAULT BASE STYLE ──
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)
    
    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 0: COVER / TITLE PAGE & CERTIFICATE (No Page Numbers)
    # ══════════════════════════════════════════════════════════════════════════
    s0 = doc.sections[0]
    s0.top_margin = Inches(1.0)
    s0.bottom_margin = Inches(1.0)
    s0.left_margin = Inches(1.0)
    s0.right_margin = Inches(1.0)
    s0.header.is_linked_to_previous = False
    s0.footer.is_linked_to_previous = False
    
    # ── COVER PAGE ──
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("A\nSEMINAR REPORT\nON")
    r.bold = True
    r.font.size = Pt(14)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(12)
    r_t = p_title.add_run("“UNCERTAINTY-GATED SELECTIVE RETRIEVAL IN QUANTIZED SMALL LANGUAGE MODELS: MITIGATING NOISE-INDUCED HALLUCINATION AND LATENCY IN EDGE DEPLOYMENT”")
    r_t.bold = True
    r_t.font.size = Pt(15)
    
    # College Logo
    logo_path = os.path.join(ASSETS_DIR, "jspm_college_logo.jpg")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(4)
        p_logo.paragraph_format.space_after = Pt(8)
        p_logo.add_run().add_picture(logo_path, width=Inches(1.6))
        
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS\nFOR THE AWARD OF DEGREE OF\n")
    r_sub.font.size = Pt(10.5)
    r_sub2 = p_sub.add_run("BACHELOR OF ENGINEERING\n(Artificial Intelligence & Data Science Engineering)")
    r_sub2.bold = True
    r_sub2.font.size = Pt(12)
    
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(8)
    p_by.paragraph_format.space_after = Pt(2)
    p_by.add_run("BY\n").bold = True
    r_name = p_by.add_run("Omkar Sachin Shedage\n")
    r_name.bold = True
    r_name.font.size = Pt(13)
    p_by.add_run("Roll No: TE-56\n\n").font.size = Pt(11)
    
    r_ug = p_by.add_run("Under the guidance of\n")
    r_ug.italic = True
    r_ug.font.size = Pt(11)
    r_g = p_by.add_run("Prof. Snehal Bhoge")
    r_g.bold = True
    r_g.font.size = Pt(13)
    
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(12)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_dept = p_inst.add_run("Department of Artificial Intelligence and Data Science Engineering\n")
    r_dept.bold = True
    r_dept.font.size = Pt(12)
    r_col = p_inst.add_run("JSPM’s Narhe Technical Campus, Narhe, Pune – 411041\n")
    r_col.bold = True
    r_col.font.size = Pt(11)
    p_inst.add_run("Rajarshi Shahu School of Engineering & Research\n").font.size = Pt(10.5)
    r_uni = p_inst.add_run("SAVITRIBAI PHULE PUNE UNIVERSITY, PUNE\n")
    r_uni.bold = True
    r_uni.font.size = Pt(11.5)
    p_inst.add_run("Academic Year: 2025–26").bold = True

    # Page Break to Certificate
    doc.add_page_break()

    # ── CERTIFICATE PAGE ──
    p_c_head = doc.add_paragraph()
    p_c_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c_head.paragraph_format.space_before = Pt(0)
    p_c_head.paragraph_format.space_after = Pt(2)
    p_c_head.paragraph_format.line_spacing = 1.15
    p_c_head.add_run("JSPM Narhe Technical Campus\n").bold = True
    p_c_head.add_run("Rajarshi Shahu School of Engineering & Research\n").font.size = Pt(10.5)
    p_c_head.add_run("DEPARTMENT OF AI&DS ENGINEERING\n").bold = True
    
    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(10)
    p_cert_title.paragraph_format.space_after = Pt(12)
    r_ct = p_cert_title.add_run("CERTIFICATE")
    r_ct.bold = True
    r_ct.font.size = Pt(16)
    
    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.space_after = Pt(14)
    p_cert_body.add_run("This is to certify that the preliminary technical seminar report entitled\n")
    
    p_ct = doc.add_paragraph()
    p_ct.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ct.paragraph_format.space_before = Pt(4)
    p_ct.paragraph_format.space_after = Pt(8)
    r_ct_txt = p_ct.add_run("“UNCERTAINTY-GATED SELECTIVE RETRIEVAL IN QUANTIZED SMALL LANGUAGE MODELS: MITIGATING NOISE-INDUCED HALLUCINATION AND LATENCY IN EDGE DEPLOYMENT”")
    r_ct_txt.bold = True
    r_ct_txt.font.size = Pt(12)
    
    p_cert_body2 = doc.add_paragraph()
    p_cert_body2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body2.paragraph_format.line_spacing = 1.5
    p_cert_body2.paragraph_format.space_after = Pt(18)
    p_cert_body2.add_run("Submitted by\n").font.size = Pt(11)
    r_sname = p_cert_body2.add_run("Omkar Sachin Shedage                  Roll No: TE-56\n\n")
    r_sname.bold = True
    p_cert_body2.add_run("is a bonafide work carried out by him under the supervision of ")
    p_cert_body2.add_run("Prof. Snehal Bhoge").bold = True
    p_cert_body2.add_run(" and it is submitted towards partial fulfillment of the requirements of ")
    p_cert_body2.add_run("Savitribai Phule Pune University, Pune").bold = True
    p_cert_body2.add_run(", for the award of the degree of Bachelor of Engineering in Artificial Intelligence & Data Science Engineering.")

    # Signatures Table (3 cols)
    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r in sig_table.rows:
        for c in r.cells:
            c.width = Inches(2.16)
            
    # Row 0: Guide, Coordinator, HOD
    c0 = sig_table.cell(0, 0)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c0.paragraphs[0].paragraph_format.line_spacing = 1.15
    c0.paragraphs[0].add_run("\n\n\nProf. Snehal Bhoge\n").bold = True
    c0.paragraphs[0].add_run("Seminar Guide\nJSPM NTC, Pune").font.size = Pt(9.5)
    
    c1 = sig_table.cell(0, 1)
    c1.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c1.paragraphs[0].paragraph_format.line_spacing = 1.15
    c1.paragraphs[0].add_run("\n\n\nProf. Name of Coordinator\n").bold = True
    c1.paragraphs[0].add_run("Seminar Coordinator\nJSPM NTC, Pune").font.size = Pt(9.5)

    c2 = sig_table.cell(0, 2)
    c2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c2.paragraphs[0].paragraph_format.line_spacing = 1.15
    c2.paragraphs[0].add_run("\n\n\nDr. Manisha Hajare / Prof. S. P. Naik\n").bold = True
    c2.paragraphs[0].add_run("HOD, AI&DS Engineering\nJSPM NTC, Pune").font.size = Pt(9.5)

    # Row 1: Director
    c_dir = sig_table.cell(1, 1)
    c_dir.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c_dir.paragraphs[0].paragraph_format.line_spacing = 1.15
    c_dir.paragraphs[0].add_run("\n\nDr. M. M. Sardeshmukh\n").bold = True
    c_dir.paragraphs[0].add_run("Director\nJSPM Narhe Technical Campus").font.size = Pt(9.5)

    p_pd = doc.add_paragraph()
    p_pd.paragraph_format.space_before = Pt(16)
    p_pd.add_run("Place: Pune                                                                                  Date: ____________").bold = True

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: FRONT MATTER (Roman Numerals i, ii, iii...)
    # ══════════════════════════════════════════════════════════════════════════
    s1 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s1.top_margin = Inches(1.0)
    s1.bottom_margin = Inches(1.0)
    s1.left_margin = Inches(1.0)
    s1.right_margin = Inches(1.0)
    s1.header.is_linked_to_previous = False
    s1.footer.is_linked_to_previous = False
    
    # Roman footer
    p_foot1 = s1.footer.paragraphs[0]
    p_foot1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number_field(p_foot1.add_run())
    # Set page numbering to roman
    sectPr1 = s1._sectPr
    pgNumType1 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="lowerRoman" w:start="1"/>')
    sectPr1.append(pgNumType1)

    # ── DECLARATION ──
    p_dh = doc.add_paragraph()
    p_dh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dh.paragraph_format.space_before = Pt(0)
    p_dh.paragraph_format.space_after = Pt(14)
    r_dh = p_dh.add_run("DECLARATION")
    r_dh.bold = True
    r_dh.font.size = Pt(16)
    
    p_d_body = doc.add_paragraph()
    p_d_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_d_body.paragraph_format.line_spacing = 1.5
    p_d_body.paragraph_format.space_after = Pt(14)
    p_d_body.add_run("I hereby declare that the seminar report entitled ")
    p_d_body.add_run("“Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment”").bold = True
    p_d_body.add_run(" is a bonafide record of independent academic research carried out by me under the guidance of ")
    p_d_body.add_run("Prof. Snehal Bhoge").bold = True
    p_d_body.add_run(", Department of Artificial Intelligence and Data Science Engineering, JSPM’s Narhe Technical Campus, Narhe, Pune.\n\n")
    p_d_body.add_run("This work is based on original research conducted during the academic year 2025–26, which has also been authored and accepted for international peer-reviewed journal publication in ")
    p_d_body.add_run("Advances in Artificial Intelligence Research (AAIR, DergiPark, e-ISSN: 2757-7422)").italic = True
    p_d_body.add_run(". I further declare that this seminar report or any part thereof has not been submitted previously to this or any other university or institution for the award of any degree, diploma, or fellowship.")

    p_dsig = doc.add_paragraph()
    p_dsig.paragraph_format.space_before = Pt(28)
    p_dsig.paragraph_format.line_spacing = 1.15
    p_dsig.add_run("Omkar Sachin Shedage\n").bold = True
    p_dsig.add_run("Roll No: TE-56\n")
    p_dsig.add_run("Department of AI&DS Engineering\n")
    p_dsig.add_run("JSPM Narhe Technical Campus, Pune\n\n")
    p_dsig.add_run("Date: ____________")

    doc.add_page_break()

    # ── ACKNOWLEDGEMENTS ──
    p_ah = doc.add_paragraph()
    p_ah.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ah.paragraph_format.space_before = Pt(0)
    p_ah.paragraph_format.space_after = Pt(14)
    r_ah = p_ah.add_run("Acknowledgements")
    r_ah.bold = True
    r_ah.font.size = Pt(16)

    p_a_body = doc.add_paragraph()
    p_a_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_a_body.paragraph_format.line_spacing = 1.5
    p_a_body.paragraph_format.space_after = Pt(10)
    p_a_body.add_run("With immense pleasure and gratitude, I present this technical seminar report entitled ")
    p_a_body.add_run("“Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment”").bold = True
    p_a_body.add_run(" as a mandatory part of the curriculum of Third Year (T.E.) Artificial Intelligence and Data Science Engineering at JSPM’s Narhe Technical Campus, Pune, affiliated with Savitribai Phule Pune University.\n\n")
    
    p_a_body.add_run("First and foremost, I express my profound gratitude and heartfelt respect to my Seminar Guide, ")
    p_a_body.add_run("Prof. Snehal Bhoge").bold = True
    p_a_body.add_run(", for her continuous encouragement, intellectual guidance, critical technical suggestions, and patient mentoring throughout the conceptualization, benchmarking, and documentation of this work. Her expertise in generative models and natural language processing provided the foundation for completing this investigation.\n\n")

    p_a_body.add_run("I express my sincere thanks to ")
    p_a_body.add_run("Dr. Manisha Hajare / Prof. S. P. Naik").bold = True
    p_a_body.add_run(", Head of the Department of Artificial Intelligence and Data Science Engineering, and the Departmental Seminar Coordinator for their organizational support and providing state-of-the-art computational laboratory facilities.\n\n")

    p_a_body.add_run("I am deeply indebted to ")
    p_a_body.add_run("Dr. M. M. Sardeshmukh").bold = True
    p_a_body.add_run(", Director of JSPM’s Narhe Technical Campus, for creating an inspiring academic and research-oriented institutional environment.\n\n")

    p_a_body.add_run("Lastly, I extend my heartfelt thanks to all the faculty members of the AI&DS Department, laboratory technical staff, my peers, and my family members whose unending moral support and encouragement enabled me to complete this research endeavor successfully.")

    p_asig = doc.add_paragraph()
    p_asig.paragraph_format.space_before = Pt(20)
    p_asig.paragraph_format.line_spacing = 1.15
    p_asig.add_run("Omkar Sachin Shedage\n").bold = True
    p_asig.add_run("Roll No: TE-56\n")
    p_asig.add_run("T.E. (Artificial Intelligence & Data Science)")

    doc.add_page_break()

    # ── ABSTRACT ──
    p_absh = doc.add_paragraph()
    p_absh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_absh.paragraph_format.space_before = Pt(0)
    p_absh.paragraph_format.space_after = Pt(14)
    r_absh = p_absh.add_run("Abstract")
    r_absh.bold = True
    r_absh.font.size = Pt(16)

    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.line_spacing = 1.5
    p_abs1.paragraph_format.space_after = Pt(10)
    p_abs1.add_run("Retrieval-Augmented Generation (RAG) is established as an indispensable paradigm for grounding Large Language Models in external knowledge and mitigating factual inaccuracies. However, state-of-the-art RAG deployments operate under a rigid, unconditional retrieval paradigm: external passages are retrieved for every user query regardless of whether the query falls well within the model’s internal parametric knowledge. When deployed on compact Small Language Models (SLMs, 1B–8B parameters) operating on resource-constrained edge hardware, this 'always-on' mechanism creates two severe operational bottlenecks: substantial latency and computational energy overhead, and severe vulnerability to noise-induced hallucination caused by irrelevant or conflicting retrieved contexts distracting parameter-limited decoders.")

    p_abs2 = doc.add_paragraph()
    p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs2.paragraph_format.line_spacing = 1.5
    p_abs2.paragraph_format.space_after = Pt(10)
    p_abs2.add_run("To resolve this foundational trade-off, this seminar report presents ")
    p_abs2.add_run("Uncertainty-Gated Selective Retrieval").bold = True
    p_abs2.add_run(", a training-free, single-forward-pass gating architecture designed specifically for quantized edge-deployed SLMs. Rather than executing speculative multi-pass sampling or training complex external routing classifiers, our framework computes an instantaneous predictive Shannon entropy probe over the model’s initial prefix decoding horizon (M = 3 tokens). When the predictive entropy falls below a calibrated decision threshold (tau = 2.0 nats), the query is recognized as parametrically confident and bypasses external retrieval entirely. Only when high epistemic uncertainty is diagnosed does the system trigger dense vector retrieval over a FAISS vector index.")

    p_abs3 = doc.add_paragraph()
    p_abs3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs3.paragraph_format.line_spacing = 1.5
    p_abs3.paragraph_format.space_after = Pt(14)
    p_abs3.add_run("Extensive empirical evaluations conducted across 18,694 benchmark queries spanning PopQA, Natural Questions (NQ-Open), and adversarial TruthfulQA demonstrate that the proposed architecture establishes a new Pareto efficiency frontier. Our method suppresses Hallucination Error Rate (HER) from 68.4% under naive static RAG down to 39.1% under 100% contradictory context noise (a 29.3 percentage point improvement). Concurrently, bypassing unnecessary retrieval on popular queries yields a 38.4% reduction in mean end-to-end latency (from 284.6 ms to 175.4 ms) and saves 32.2% of GPU energy consumption per query. Furthermore, validation under 4-bit Activation-aware Weight Quantization (AWQ) proves that uncertainty separation remains highly robust (Delta U = 1.786 nats, p < 10^-11) while compressing the model footprint to 2.2 GB VRAM, proving feasibility for standalone, private edge deployment.")

    doc.add_page_break()

    # ── TABLE OF CONTENTS ──
    p_ch = doc.add_paragraph()
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ch.paragraph_format.space_before = Pt(0)
    p_ch.paragraph_format.space_after = Pt(14)
    r_ch = p_ch.add_run("Contents")
    r_ch.bold = True
    r_ch.font.size = Pt(16)

    # Clean TOC Table
    toc_data = [
        ("", "Certificate", "i"),
        ("", "Declaration", "ii"),
        ("", "Acknowledgements", "iii"),
        ("", "Abstract", "iv"),
        ("", "List of Tables", "vii"),
        ("", "List of Figures", "viii"),
        ("", "List of Acronyms and Abbreviations", "ix"),
        ("Chapter 1", "Introduction", "1"),
        ("", "1.1 Introduction and Background of RAG", "1"),
        ("", "1.2 Problem Statement & Identified Deficiencies", "3"),
        ("", "1.3 Motivation: Edge Computing & Quantized SLMs", "4"),
        ("", "1.4 Purpose, Scope, and Objectives of the Seminar", "6"),
        ("", "1.5 Interdisciplinary Alignment with AI&DS Curriculum", "7"),
        ("", "1.6 Organization of the Report", "8"),
        ("Chapter 2", "Literature Review and Comparative Evaluation", "9"),
        ("", "2.1 Evolution of Retrieval Architectures: From Dense to Adaptive", "9"),
        ("", "2.2 Survey of Existing Adaptive Retrieval Frameworks", "11"),
        ("", "2.3 Context Distraction & Noise-Induced Hallucination Mechanics", "13"),
        ("", "2.4 Post-Training Weight Quantization in Edge AI (AWQ vs. GPTQ)", "15"),
        ("", "2.5 Comparative Literature Survey Matrix", "17"),
        ("", "2.6 Critical Research Gap and Positioning", "18"),
        ("Chapter 3", "Proposed Methodology and System Architecture", "19"),
        ("", "3.1 Architectural Overview & Core Workflow", "19"),
        ("", "3.2 Prefix Predictive Shannon Entropy Probe Formulation", "21"),
        ("", "3.3 Dynamic Uncertainty Gating Threshold Mechanism", "23"),
        ("", "3.4 Dense Vector Retrieval Subsystem with FAISS", "25"),
        ("", "3.5 Native INT4 AWQ Quantization Integration", "26"),
        ("", "3.6 Benchmark Datasets and Stratification", "28"),
        ("", "3.7 Hardware Testbed, Software Requirements & Instrumentation", "29"),
        ("", "3.8 Statistical Evaluation Protocol", "31"),
        ("Chapter 4", "Results, Empirical Evaluation, and Discussion", "32"),
        ("", "4.1 Empirical Prefix Entropy Distributions across Knowledge Tiers", "32"),
        ("", "4.2 End-to-End Task Performance Benchmark", "34"),
        ("", "4.3 Hardware Telemetry Profiles: Latency & Energy Conservation", "36"),
        ("", "4.4 Robustness Under Controlled Context Noise Injection", "38"),
        ("", "4.5 Ablation Analysis: Prefix Horizon M and Threshold tau", "40"),
        ("", "4.6 Quantization Impact: FP16 vs. INT4 AWQ", "42"),
        ("", "4.7 Qualitative Case Studies & Failure Mode Analysis", "43"),
        ("", "4.8 Architectural Discussion & Practical Edge Guidelines", "45"),
        ("Chapter 5", "Conclusion and Future Scope", "47"),
        ("", "5.1 Summary of Major Findings & Contributions", "47"),
        ("", "5.2 Fulfillment of Research Objectives", "48"),
        ("", "5.3 Limitations of the Current Study", "49"),
        ("", "5.4 Future Work & Next-Generation Directions", "50"),
        ("", "References", "51"),
        ("", "Appendix: Research Publication & Acceptance Certificate", "54"),
    ]

    toc_table = doc.add_table(rows=len(toc_data) + 1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    format_college_table(toc_table, 3, [Inches(1.5), Inches(4.2), Inches(0.8)])
    
    # Header
    style_cell(toc_table.cell(0, 0), "Chapter", is_header=True)
    style_cell(toc_table.cell(0, 1), "Contents", is_header=True)
    style_cell(toc_table.cell(0, 2), "Page No.", is_header=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    
    for r_i, (ch_col, title_col, pg_col) in enumerate(toc_data, 1):
        is_ch = ch_col.startswith("Chapter") or title_col in ["References", "Abstract", "Certificate", "Acknowledgements"]
        style_cell(toc_table.cell(r_i, 0), ch_col, is_bold=is_ch)
        style_cell(toc_table.cell(r_i, 1), title_col, is_bold=is_ch)
        style_cell(toc_table.cell(r_i, 2), pg_col, is_bold=is_ch, align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # ── LIST OF TABLES ──
    p_lth = doc.add_paragraph()
    p_lth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lth.paragraph_format.space_before = Pt(0)
    p_lth.paragraph_format.space_after = Pt(14)
    r_lth = p_lth.add_run("List of Tables")
    r_lth.bold = True
    r_lth.font.size = Pt(16)

    lot_data = [
        ("Table 2.1", "Comparative literature survey matrix of selective and adaptive RAG methods", "17"),
        ("Table 3.1", "Benchmark dataset characteristics and knowledge stratification", "28"),
        ("Table 3.2", "Hardware testbed and software execution environment specifications", "30"),
        ("Table 4.1", "Empirical prefix predictive Shannon entropy distribution across query categories", "33"),
        ("Table 4.2", "End-to-end task performance and hardware telemetry across models and benchmarks", "35"),
        ("Table 4.3", "Hallucination Error Rate (HER %) under controlled context noise injection", "38"),
        ("Table 4.4", "Ablation study on prefix horizon M and gating threshold tau (Llama-3.2-3B)", "40"),
        ("Table 4.5", "Quantization comparison: FP16 precision vs. INT4 AWQ efficiency", "42"),
    ]

    lot_table = doc.add_table(rows=len(lot_data) + 1, cols=3)
    format_college_table(lot_table, 3, [Inches(1.5), Inches(4.2), Inches(0.8)])
    style_cell(lot_table.cell(0, 0), "Table No.", is_header=True)
    style_cell(lot_table.cell(0, 1), "Title", is_header=True)
    style_cell(lot_table.cell(0, 2), "Page No.", is_header=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    
    for r_i, (tno, title, pno) in enumerate(lot_data, 1):
        style_cell(lot_table.cell(r_i, 0), tno, is_bold=True)
        style_cell(lot_table.cell(r_i, 1), title)
        style_cell(lot_table.cell(r_i, 2), pno, align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # ── LIST OF FIGURES ──
    p_lfh = doc.add_paragraph()
    p_lfh.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lfh.paragraph_format.space_before = Pt(0)
    p_lfh.paragraph_format.space_after = Pt(14)
    r_lfh = p_lfh.add_run("List of Figures")
    r_lfh.bold = True
    r_lfh.font.size = Pt(16)

    lof_data = [
        ("Figure 1.1", "Architectural paradigm comparison: Conventional Always-On RAG vs. Proposed Uncertainty-Gated Selective Retrieval", "2"),
        ("Figure 3.1", "Comprehensive system architectural flowchart and hardware execution pipeline", "20"),
        ("Figure 4.1", "Empirical prefix Shannon entropy distributions across Popular and Long-Tail queries for Qwen2.5 and Llama-3.2", "33"),
        ("Figure 4.2", "Hallucination Error Rate (HER %) vulnerability curves under controlled context noise injection", "39"),
        ("Figure 4.3", "Inference latency (ms) and GPU energy consumption (J) benchmarks across models", "37"),
    ]

    lof_table = doc.add_table(rows=len(lof_data) + 1, cols=3)
    format_college_table(lof_table, 3, [Inches(1.5), Inches(4.2), Inches(0.8)])
    style_cell(lof_table.cell(0, 0), "Figure No.", is_header=True)
    style_cell(lof_table.cell(0, 1), "Title", is_header=True)
    style_cell(lof_table.cell(0, 2), "Page No.", is_header=True, align=WD_ALIGN_PARAGRAPH.RIGHT)
    
    for r_i, (fno, title, pno) in enumerate(lof_data, 1):
        style_cell(lof_table.cell(r_i, 0), fno, is_bold=True)
        style_cell(lof_table.cell(r_i, 1), title)
        style_cell(lof_table.cell(r_i, 2), pno, align=WD_ALIGN_PARAGRAPH.RIGHT)

    doc.add_page_break()

    # ── LIST OF ACRONYMS AND ABBREVIATIONS ──
    p_ach = doc.add_paragraph()
    p_ach.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ach.paragraph_format.space_before = Pt(0)
    p_ach.paragraph_format.space_after = Pt(14)
    r_ach = p_ach.add_run("List of Acronyms and Abbreviations")
    r_ach.bold = True
    r_ach.font.size = Pt(16)

    acronyms = [
        ("RAG", "Retrieval-Augmented Generation"),
        ("SLM", "Small Language Model (1B – 8B parameters)"),
        ("LLM", "Large Language Model"),
        ("AWQ", "Activation-aware Weight Quantization"),
        ("FAISS", "Facebook AI Similarity Search"),
        ("HER", "Hallucination Error Rate (%)"),
        ("EM", "Exact Match Accuracy (%)"),
        ("TTFT", "Time-To-First-Token (milliseconds)"),
        ("CI", "Confidence Interval (Bootstrap 95%)"),
        ("NQ", "Natural Questions Open-Domain Benchmark"),
        ("PopQA", "Popularity-Stratified Entity Question Answering Benchmark"),
        ("CUDA", "Compute Unified Device Architecture (NVIDIA)"),
        ("VRAM", "Video Random Access Memory"),
        ("TDP", "Thermal Design Power (Watts)"),
        ("GPU", "Graphics Processing Unit"),
        ("CPU", "Central Processing Unit"),
        ("NVML", "NVIDIA Management Library"),
        ("NLP", "Natural Language Processing"),
        ("NLI", "Natural Language Inference"),
        ("FP16", "16-bit Half-Precision Floating Point"),
        ("INT4", "4-bit Integer Precision Quantization"),
        ("HOD", "Head of the Department"),
        ("SPPU", "Savitribai Phule Pune University"),
        ("JSPM", "Jayawant Shikshan Prasarak Mandal"),
        ("NTC", "Narhe Technical Campus"),
    ]

    acro_table = doc.add_table(rows=len(acronyms) + 1, cols=2)
    format_college_table(acro_table, 2, [Inches(2.0), Inches(4.5)])
    style_cell(acro_table.cell(0, 0), "Acronym / Abbreviation", is_header=True)
    style_cell(acro_table.cell(0, 1), "Expanded Description", is_header=True)
    
    for r_i, (acr, desc) in enumerate(acronyms, 1):
        style_cell(acro_table.cell(r_i, 0), acr, is_bold=True)
        style_cell(acro_table.cell(r_i, 1), desc)

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: MAIN CHAPTERS (Arabic Numerals 1, 2, 3...)
    # ══════════════════════════════════════════════════════════════════════════
    s2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    s2.top_margin = Inches(1.0)
    s2.bottom_margin = Inches(1.0)
    s2.left_margin = Inches(1.0)
    s2.right_margin = Inches(1.0)
    s2.header.is_linked_to_previous = False
    s2.footer.is_linked_to_previous = False
    
    # Arabic footer
    p_foot2 = s2.footer.paragraphs[0]
    p_foot2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_number_field(p_foot2.add_run())
    
    sectPr2 = s2._sectPr
    pgNumType2 = parse_xml(f'<w:pgNumType {nsdecls("w")} w:fmt="decimal" w:start="1"/>')
    sectPr2.append(pgNumType2)

    return doc

print("Template builder initialized.")
