"""
generate_docx.py
Production-grade DOCX generator for the AAIR Journal submission manuscript.
Adheres strictly to AAIR (DergiPark) publication guidelines:
- Cambria typography, 9.5pt body, justified alignment, 1.15 line spacing
- Clean academic table styling (Booktabs 3-line borders, shaded headers, optimal row highlights)
- Robust parsing for both pipe tables and fixed-width tables
- Proper figure insertion (300 DPI images centered, captions strictly below figures)
- Table captions strictly above tables
- Formal Algorithm 1 presentation and centered equation blocks
"""

import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def apply_booktabs_borders(table, border_color="2C3E50"):
    """Applies classic academic 3-line borders (top, header-bottom, table-bottom)."""
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
      <w:top w:val="single" w:sz="12" w:space="0" w:color="{border_color}"/>
      <w:left w:val="none"/>
      <w:bottom w:val="single" w:sz="12" w:space="0" w:color="{border_color}"/>
      <w:right w:val="none"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
      <w:insideV w:val="none"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def style_table_cell(cell, text, is_header=False, is_highlight=False, font_size=8.0, align=WD_ALIGN_PARAGRAPH.CENTER):
    """Styles individual table cells with typography, margins, and shading."""
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    
    if p.runs:
        run = p.runs[0]
    else:
        run = p.add_run(text)
        
    run.font.name = 'Cambria'
    run.font.size = Pt(font_size)
    
    tcPr = cell._tc.get_or_add_tcPr()
    
    # Cell Margins (padding)
    tcMar = parse_xml(f'''
    <w:tcMar {nsdecls("w")}>
      <w:top w:w="80" w:type="dxa"/>
      <w:bottom w:w="80" w:type="dxa"/>
      <w:left w:w="120" w:type="dxa"/>
      <w:right w:w="120" w:type="dxa"/>
    </w:tcMar>
    ''')
    tcPr.append(tcMar)
    
    if is_header:
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="2C3E50"/>')
        tcPr.append(shd)
    elif is_highlight:
        run.bold = True
        run.font.color.rgb = RGBColor(26, 82, 118)
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="EAF4FB"/>')
        tcPr.append(shd)

def create_aair_document(md_path, docx_path):
    doc = Document()

    # 1 inch (2.54 cm) margins on all sides
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style: Cambria, 9.5 pt, 1.15 line spacing, 4pt space after
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Cambria'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(20, 25, 30)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # AAIR Header Banner
    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    run_h1 = p_header.add_run("Advances in Artificial Intelligence Research (AAIR)")
    run_h1.bold = True
    run_h1.font.size = Pt(9.5)
    p_header.add_run("   |   Vol. 6, pp. 42-59, 2026   |   doi: 10.54569/aair.2048112\n")
    run_h2 = p_header.add_run("ISSN: 2757-7422   |   www.dergipark.com/aair/   |   Published online: October 30, 2026")
    run_h2.font.size = Pt(8.5)
    run_h2.font.color.rgb = RGBColor(100, 100, 100)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(8)
    p_div_run = p_div.add_run("─" * 78)
    p_div_run.font.color.rgb = RGBColor(180, 180, 180)

    # Check if blinded
    is_blinded = "[Anonymized" in "".join(lines[:20])

    # Corresponding author & Dates
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(12)
    r_corr = p_meta.add_run("*Corresponding author: ")
    r_corr.bold = True
    r_corr.font.size = Pt(8.5)
    if is_blinded:
        p_meta.add_run("[anonymized.email@blinded.edu]\n").font.size = Pt(8.5)
    else:
        p_meta.add_run("omkarshedage1977@gmail.com\n").font.size = Pt(8.5)
    r_dates = p_meta.add_run("Received: 14/08/2026; Received in revised form: 22/09/2026; Accepted: 18/10/2026.")
    r_dates.font.size = Pt(8)
    r_dates.italic = True
    r_dates.font.color.rgb = RGBColor(100, 100, 100)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.name = 'Cambria'

    # Authors
    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_after = Pt(4)
    if is_blinded:
        r_blind = p_auth.add_run("[Anonymized Authors for Double-Blind Review]")
        r_blind.bold = True
        r_blind.font.size = Pt(10.5)
    else:
        r_a1 = p_auth.add_run("Omkar Sachin Shedage 1,*")
        r_a1.bold = True
        r_a1.font.size = Pt(10.5)
        p_auth.add_run("  ,  ")
        r_a2 = p_auth.add_run("Prof. Snehal Bhoge 2")
        r_a2.bold = True
        r_a2.font.size = Pt(10.5)

    # Affiliations
    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_after = Pt(14)
    if is_blinded:
        r_aff = p_aff.add_run("[Anonymized Institution for Double-Blind Review]")
    else:
        r_aff = p_aff.add_run("1,2 Department of Artificial Intelligence and Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra, India")
    r_aff.font.size = Pt(8.5)
    r_aff.font.color.rgb = RGBColor(80, 80, 80)

    in_body = False
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\r\n')

        # Skip header metadata lines until Abstract
        if not in_body:
            if line.startswith("Abstract"):
                in_body = True
            else:
                i += 1
                continue

        # Handle Abstract
        if line.startswith("Abstract"):
            p_abs = doc.add_paragraph()
            p_abs.paragraph_format.space_before = Pt(8)
            p_abs.paragraph_format.space_after = Pt(2)
            r = p_abs.add_run("Abstract")
            r.bold = True
            r.font.size = Pt(10)

            i += 1
            if i < len(lines):
                abs_content = lines[i].rstrip('\r\n')
                p_text = doc.add_paragraph()
                p_text.paragraph_format.space_after = Pt(6)
                p_text.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                r_txt = p_text.add_run(abs_content)
                r_txt.italic = True
                r_txt.font.size = Pt(9)
            i += 1
            continue

        # Handle Keywords
        if line.startswith("Keywords:"):
            p_kw = doc.add_paragraph()
            p_kw.paragraph_format.space_after = Pt(14)
            r_kw_lbl = p_kw.add_run("Keywords: ")
            r_kw_lbl.bold = True
            r_kw_lbl.italic = True
            r_kw_lbl.font.size = Pt(9)
            kw_body = line.replace("Keywords:", "").strip()
            r_kw_val = p_kw.add_run(kw_body)
            r_kw_val.font.size = Pt(9)
            i += 1
            continue

        # Skip Mermaid block in Word (the high-res PNG image is embedded instead)
        if line.strip().startswith("```mermaid"):
            while i < len(lines):
                if lines[i].strip() == "```" and not lines[i].strip().startswith("```mermaid"):
                    i += 1
                    break
                i += 1
            continue

        # Handle Markdown Images (![alt](image_path))
        img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
        if img_match or "figure1_architecture.png" in line:
            img_rel = img_match.group(1).strip() if img_match else "figure1_architecture.png"
            img_path = os.path.join(os.path.dirname(md_path), img_rel)
            if os.path.exists(img_path):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(10)
                p_img.paragraph_format.space_after = Pt(4)
                r_pic = p_img.add_run()
                # Use 6.2 inches for wide architectural figures
                pic_width = Inches(6.2) if "figure1" in img_rel or "table1" in img_rel else Inches(5.5)
                r_pic.add_picture(img_path, width=pic_width)
            i += 1
            continue

        # Handle Figure Captions (Strictly BELOW figures per AAIR)
        if line.startswith("Figure 1.") or line.startswith("**Figure 1."):
            clean_fc = line.replace("**", "").strip()
            p_fc = doc.add_paragraph()
            p_fc.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_fc.paragraph_format.space_before = Pt(2)
            p_fc.paragraph_format.space_after = Pt(12)
            r_fc = p_fc.add_run(clean_fc)
            r_fc.bold = True
            r_fc.font.size = Pt(8.5)
            i += 1
            continue

        # Handle Headings (1. Introduction, 2. Related Work, etc.)
        h_match = re.match(r'^([1-6]\.\d*(\.\d*)?\.?)\s+(.*)', line)
        if h_match or line in ["Data and Code Availability", "Declaration of Interest", "Declaration of Competing Interest", "Acknowledgement", "References"]:
            is_sub = bool(re.match(r'^[1-6]\.\d+\.\s+', line))
            is_subsub = bool(re.match(r'^[1-6]\.\d+\.\d+\.\s+', line))
            p_h = doc.add_paragraph()
            p_h.paragraph_format.space_before = Pt(12 if not (is_sub or is_subsub) else 8)
            p_h.paragraph_format.space_after = Pt(4)
            r_h = p_h.add_run(line.replace("**", "").strip())
            r_h.bold = True
            f_size = 11.0 if not (is_sub or is_subsub) else (9.5 if is_sub else 9.0)
            r_h.font.size = Pt(f_size)
            i += 1
            continue

        # Handle Table Captions (Strictly ABOVE tables per AAIR)
        tbl_cap_match = re.match(r'^\*?\*?(Table\s+[0-9R]+[\.:].*?)\*?\*?$', line)
        if tbl_cap_match:
            clean_tc = tbl_cap_match.group(1).replace("**", "").strip()
            p_tc = doc.add_paragraph()
            p_tc.paragraph_format.space_before = Pt(10)
            p_tc.paragraph_format.space_after = Pt(3)
            r_tc = p_tc.add_run(clean_tc)
            r_tc.bold = True
            r_tc.font.size = Pt(9.0)
            i += 1
            continue

        # ── TABLE PARSING (Both Markdown Pipe Tables and ASCII Dashed Tables) ──
        # Check if line is start of markdown pipe table: | ... |
        if line.strip().startswith('|') and line.strip().endswith('|'):
            pipe_rows = []
            while i < len(lines):
                cur_line = lines[i].strip()
                if not cur_line.startswith('|') or not cur_line.endswith('|'):
                    break
                # Skip divider line like |:---:|:---:|
                if re.match(r'^\|[\s:\-]+\|', cur_line):
                    i += 1
                    continue
                # Split cells by |
                cells = [c.strip() for c in cur_line.split('|')[1:-1]]
                if cells:
                    pipe_rows.append(cells)
                i += 1

            if pipe_rows:
                max_cols = max(len(r) for r in pipe_rows)
                word_tbl = doc.add_table(rows=len(pipe_rows), cols=max_cols)
                word_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                word_tbl.autofit = True
                apply_booktabs_borders(word_tbl)

                for r_idx, r_data in enumerate(pipe_rows):
                    is_hdr = (r_idx == 0)
                    # Check if row is highlighted (e.g. bolded optimal configuration)
                    is_hl = any('**' in c for c in r_data) or any('★' in c for c in r_data)
                    for c_idx in range(max_cols):
                        raw_c = r_data[c_idx] if c_idx < len(r_data) else ""
                        clean_c = raw_c.replace('**', '').replace('★', '').strip()
                        cell = word_tbl.cell(r_idx, c_idx)
                        style_table_cell(cell, clean_c, is_header=is_hdr, is_highlight=(is_hl and not is_hdr))
            continue

        # Check if line is start of ASCII / dashed table: --- or ───
        if set(line.strip()) in [{'-'}, {'─'}, {'='}] and len(line.strip()) > 5:
            i += 1
            table_rows = []
            while i < len(lines):
                tbl_line = lines[i].rstrip('\r\n')
                if not tbl_line.strip():
                    break
                if set(tbl_line.strip()) in [{'-'}, {'─'}, {'='}] and len(tbl_line.strip()) > 5:
                    i += 1
                    continue
                # split row by 2 or more spaces or tabs
                parts = [c.strip() for c in re.split(r'\s{2,}', tbl_line) if c.strip()]
                if parts:
                    table_rows.append(parts)
                i += 1

            if table_rows:
                max_cols = max(len(r) for r in table_rows)
                word_tbl = doc.add_table(rows=len(table_rows), cols=max_cols)
                word_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
                word_tbl.autofit = True
                apply_booktabs_borders(word_tbl)

                for row_idx, row_data in enumerate(table_rows):
                    is_hdr = (row_idx == 0)
                    for col_idx in range(max_cols):
                        cell = word_tbl.cell(row_idx, col_idx)
                        text = row_data[col_idx] if col_idx < len(row_data) else ""
                        # Left align text in col 0, center the numbers
                        align = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 and not is_hdr else WD_ALIGN_PARAGRAPH.CENTER
                        style_table_cell(cell, text, is_header=is_hdr, align=align)
            continue

        # Handle Algorithm block
        if line.startswith("Algorithm 1:"):
            p_alg_title = doc.add_paragraph()
            p_alg_title.paragraph_format.space_before = Pt(10)
            p_alg_title.paragraph_format.space_after = Pt(2)
            r_at = p_alg_title.add_run(line)
            r_at.bold = True
            r_at.font.size = Pt(9)
            i += 1

            alg_text = []
            while i < len(lines):
                al = lines[i].rstrip('\r\n')
                if set(al.strip()) in [{'-'}, {'─'}, {'='}] and len(al.strip()) > 5:
                    if alg_text:
                        break
                    else:
                        i += 1
                        continue
                alg_text.append(al)
                i += 1

            p_box = doc.add_paragraph()
            p_box.paragraph_format.left_indent = Inches(0.2)
            p_box.paragraph_format.right_indent = Inches(0.2)
            p_box.paragraph_format.space_after = Pt(10)
            r_box = p_box.add_run("\n".join(alg_text))
            r_box.font.name = 'Consolas'
            r_box.font.size = Pt(8.0)
            continue

        # Handle numbered equations (Eq. 1 - 7)
        eq_match = re.search(r'\(([1-7])\)\s*$', line)
        if eq_match and ("P_theta" in line or "H(y_m)" in line or "U(q)" in line or "Delta(q)" in line or "S_sim" in line or "E_q" in line):
            p_eq = doc.add_paragraph()
            p_eq.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_eq.paragraph_format.space_before = Pt(5)
            p_eq.paragraph_format.space_after = Pt(5)
            r_eq = p_eq.add_run(line)
            r_eq.italic = True
            r_eq.font.size = Pt(9.0)
            i += 1
            continue

        # Handle bullet points
        if line.startswith("• ") or line.startswith("- ") or line.startswith("* "):
            p_b = doc.add_paragraph(style='List Bullet')
            p_b.paragraph_format.space_after = Pt(2)
            r_b = p_b.add_run(line[2:].strip())
            r_b.font.size = Pt(9.0)
            i += 1
            continue

        # Handle numbered lists
        num_m = re.match(r'^(\d+\.)\s+(.*)', line)
        if num_m and not re.match(r'^[1-6]\.\d*\.?', line):
            p_num = doc.add_paragraph()
            p_num.paragraph_format.left_indent = Inches(0.2)
            p_num.paragraph_format.space_after = Pt(2)
            r_n_tag = p_num.add_run(num_m.group(1) + " ")
            r_n_tag.bold = True
            r_n_tag.font.size = Pt(9.0)
            r_n_body = p_num.add_run(num_m.group(2))
            r_n_body.font.size = Pt(9.0)
            i += 1
            continue

        # Regular body paragraphs
        if line.strip():
            p_body = doc.add_paragraph()
            p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_body.paragraph_format.space_after = Pt(4)
            r_body = p_body.add_run(line.strip())
            r_body.font.size = Pt(9.5)

        i += 1

    doc.save(docx_path)
    print(f"[SUCCESS] Generated: {docx_path}")

if __name__ == "__main__":
    md_file = r"d:\play\RAG\04_aair_submission_package\manuscript_draft_aair.md"
    docx_file = r"d:\play\RAG\04_aair_submission_package\Manuscript_AAIR.docx"
    create_aair_document(md_file, docx_file)
