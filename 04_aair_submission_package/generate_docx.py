"""
generate_docx.py
Production-grade DOCX generator for the AAIR Journal submission manuscript.
Adheres strictly to the authentic published AAIR (DergiPark) journal layout:
- Running Header: "Aktaş et al. / AAIR vol 6 (2026) 10-17" -> "Shedage et al. / AAIR vol 6 (2026) 42-59" (or Blinded)
- Running Footer: Right-aligned "P a g e  X" with dynamic Word page number
- Single-column justified layout (Cambria 9.5pt, 1.15 line spacing)
- Authentic 3-line Booktabs table format (solid black top/bottom lines, line under header, NO inside borders, NO header background fill)
- Centered table captions: "Table X. *Title*" (Bold label, italicized title)
- Centered figure captions below figures
- Hierarchical bold headings (11pt, 10pt, 9.5pt)
- Formatted bullet lists and bold-labeled numbered lists
"""

import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def apply_aair_table_borders(table, border_color="000000"):
    """
    Applies authentic published AAIR table borders:
    - Top border: solid line 1.0 pt (sz="8")
    - Bottom border: solid line 1.0 pt (sz="8")
    - Inside horizontal: NONE
    - Inside vertical: NONE
    - Left / Right: NONE
    """
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
    """Applies a solid horizontal line under the header row, exactly as in published AAIR articles."""
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
          <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>
        ''')
        tcPr.append(tcBorders)

def format_aair_table(word_tbl, num_cols, table_num=None):
    """
    Applies authentic published AAIR table styling matching Table 2 / Table 4:
    - Full text width (6.5 inches / 9360 dxa) spanning cleanly across page margins
    - Proportional column widths summing to 6.5 inches
    - Three solid black horizontal rules:
        * Top border: solid 1.0 pt
        * Header bottom border: solid 0.75 pt
        * Bottom border: solid 1.0 pt
    - Zero vertical borders, zero interior horizontal rules
    - All column headers repeated on subsequent pages (<w:tblHeader/>)
    - All rows protected against mid-row page splits (<w:cantSplit/>)
    - Pure white header and cell backgrounds (no shading)
    """
    word_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    word_tbl.autofit = False
    
    # 1. Enforce 100% text width (6.5 inches = 9360 dxa)
    tblPr = word_tbl._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblW'):
            tblPr.remove(child)
    tblW_xml = parse_xml(f'<w:tblW {nsdecls("w")} w:w="9360" w:type="dxa"/>')
    tblPr.append(tblW_xml)
    
    # 2. Apply 3-line borders
    apply_aair_table_borders(word_tbl)
    if len(word_tbl.rows) > 0:
        apply_header_bottom_border(word_tbl.rows[0])
        
    # 3. Column width mapping (summing to 6.5 in)
    col_width_map = {
        1: [1.10, 1.20, 1.10, 1.20, 1.90],             # Table 1: Method, Fine-Tuning, Latency, Quantized, Limitation
        2: [1.30, 1.10, 1.60, 2.50],                   # Table 2: Dataset, Total Queries, Knowledge Type, Key Feature
        3: [1.80, 2.40, 2.30],                         # Table 3: Subsystem, Specification, Operational Role
        4: [1.10, 1.20, 0.90, 0.70, 0.55, 0.55, 1.50],# Table 4: Model, Category, Mean, Std, Min, Max, 95% CI
        5: [1.90, 0.90, 0.90, 0.95, 0.95, 0.90],       # Table 5: Model/Setup, PopQA, NQ, TruthfulQA, Latency, Energy
        6: [2.10, 1.10, 1.10, 1.10, 1.10],             # Table 6: Method, 0%, 25%, 50%, 100%
        7: [1.15, 1.15, 1.05, 1.05, 1.05, 1.05],       # Table 7: Prefix Horizon, Threshold, PopQA, Bypass, Gating, Total
        8: [1.80, 0.90, 0.90, 1.00, 1.00, 0.90],       # Table 8: Model/Precision, Memory, PopQA, Pop Ent, Tail Ent, Delta U
    }
    
    widths = col_width_map.get(table_num)
    if widths is None or len(widths) != num_cols:
        col_w = 6.5 / num_cols
        widths = [col_w] * num_cols
        
    for r_idx, row in enumerate(word_tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
            
        for c_idx, cell in enumerate(row.cells):
            if c_idx < len(widths):
                cell.width = Inches(widths[c_idx])

def style_table_cell(cell, text, is_header=False, is_bold=False, is_italic=False, font_size=8.5, align=WD_ALIGN_PARAGRAPH.LEFT):
    """
    Styles table cells matching the published AAIR sample:
    - Clean white background (no dark fill)
    - Bold black header text
    - All columns LEFT-ALIGNED (matching Table 2 & Table 4 in AAIR)
    - Comfortable cell padding (margins)
    """
    cell.text = text
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(2.5)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.05
    
    run = p.runs[0] if p.runs else p.add_run(text)
    run.font.name = 'Cambria'
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

def create_aair_document(md_path, docx_path):
    doc = Document()

    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    is_blinded = "[Anonymized" in "".join(lines[:25])

    # ── 1. PAGE SETUP (A4, 1-inch margins, running headers & footers) ──
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Configure different first page
        section.different_first_page_header_footer = True
        
        # Running Header for Page 2+
        header = section.header
        p_head = header.paragraphs[0]
        p_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_head.paragraph_format.space_after = Pt(4)
        
        hdr_text = "Advances in Artificial Intelligence Research (AAIR)  |  Manuscript Submission Draft" if is_blinded else "Shedage & Bhoge  /  Advances in Artificial Intelligence Research (AAIR)  |  Submission Draft"
        r_head = p_head.add_run(hdr_text)
        r_head.font.name = 'Cambria'
        r_head.font.size = Pt(8.5)
        r_head.font.color.rgb = RGBColor(70, 70, 70)
        
        # Running Footer for Page 2+ (Matches "P a g e  16" in AAIR sample)
        footer = section.footer
        p_foot = footer.paragraphs[0]
        p_foot.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_foot.paragraph_format.space_before = Pt(4)
        r_foot = p_foot.add_run("P a g e  ")
        r_foot.font.name = 'Cambria'
        r_foot.font.size = Pt(8.5)
        r_foot.font.color.rgb = RGBColor(90, 90, 90)
        
        # Dynamic Word page field
        fld = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        p_foot._p.append(fld)

    # ── 2. BASE STYLES ──
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Cambria'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(20, 25, 30)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4.5)

    # ── 3. FIRST PAGE HEADER BANNER ──
    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_after = Pt(2)
    run_h1 = p_header.add_run("Advances in Artificial Intelligence Research (AAIR)")
    run_h1.bold = True
    run_h1.font.size = Pt(9.5)
    p_header.add_run("   |   e-ISSN: 2757-7422   |   https://dergipark.org.tr/en/pub/aair\n")
    if is_blinded:
        run_h2 = p_header.add_run("Original Research Article   |   Manuscript Prepared for Double-Blind Peer Review")
    else:
        run_h2 = p_header.add_run("Original Research Article   |   Manuscript Submission Draft   |   Academic Year: 2025–26")
    run_h2.font.size = Pt(8.5)
    run_h2.font.color.rgb = RGBColor(100, 100, 100)

    # Divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_after = Pt(12)
    p_div_run = p_div.add_run("─" * 78)
    p_div_run.font.color.rgb = RGBColor(180, 180, 180)

    # In an unblinded manuscript, include authentic submission status.
    # In a blinded manuscript, no corresponding author or dates appear on the main text (stored on Title Page).
    if not is_blinded:
        p_meta = doc.add_paragraph()
        p_meta.paragraph_format.space_after = Pt(10)
        r_corr = p_meta.add_run("*Corresponding author: ")
        r_corr.bold = True
        r_corr.font.size = Pt(8.5)
        p_meta.add_run("omkarshedage1977@gmail.com\n").font.size = Pt(8.5)
        r_dates = p_meta.add_run("Submission Draft (November 2026); Status: Under Peer Review.")
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
        r_aff = p_aff.add_run("[Author identities, institutional affiliations, and contact details are documented on the Title Page]")
        r_aff.italic = True
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
                p_img.paragraph_format.space_after = Pt(3)
                r_pic = p_img.add_run()
                pic_width = Inches(6.2) if "figure1" in img_rel or "table1" in img_rel else Inches(5.5)
                r_pic.add_picture(img_path, width=pic_width)
            i += 1
            continue

        # Handle Figure Captions (Strictly BELOW figures per AAIR)
        if line.startswith("Figure 1.") or line.startswith("**Figure 1."):
            clean_fc = line.replace("**", "").strip()
            p_fc = doc.add_paragraph()
            p_fc.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_fc.paragraph_format.space_before = Pt(3)
            p_fc.paragraph_format.space_after = Pt(12)
            
            # Format: "Figure 1." bold, rest regular
            fig_match = re.match(r'^(Figure\s+\d+[\.:]?)\s*(.*)', clean_fc)
            if fig_match:
                r_flbl = p_fc.add_run(fig_match.group(1).rstrip('.') + '. ')
                r_flbl.bold = True
                r_flbl.font.size = Pt(8.5)
                r_ftxt = p_fc.add_run(fig_match.group(2))
                r_ftxt.font.size = Pt(8.5)
            else:
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
            p_h.paragraph_format.space_before = Pt(14 if not (is_sub or is_subsub) else (10 if is_sub else 8))
            p_h.paragraph_format.space_after = Pt(3)
            r_h = p_h.add_run(line.replace("**", "").strip())
            r_h.bold = True
            f_size = 11.0 if not (is_sub or is_subsub) else (10.0 if is_sub else 9.5)
            r_h.font.size = Pt(f_size)
            i += 1
            continue

        # Handle Table Captions (Strictly CENTERED ABOVE tables per published AAIR: "Table 2. Prompt Configuration...")
        tbl_cap_match = re.match(r'^\*?\*?(Table\s+([0-9R]+)[\.:].*?)\*?\*?$', line)
        if tbl_cap_match:
            clean_tc = tbl_cap_match.group(1).replace("**", "").strip()
            table_raw_id = tbl_cap_match.group(2)
            current_table_num = int(table_raw_id) if table_raw_id.isdigit() else None
            
            p_tc = doc.add_paragraph()
            p_tc.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_tc.paragraph_format.space_before = Pt(14)
            p_tc.paragraph_format.space_after = Pt(3)
            p_tc.paragraph_format.keep_with_next = True
            
            # Extract "Table X." and Title
            tc_m = re.match(r'^(Table\s+[0-9R]+[\.:]?)\s*(.*)', clean_tc)
            if tc_m:
                r_tlbl = p_tc.add_run(tc_m.group(1).rstrip('.') + '. ')
                r_tlbl.bold = True
                r_tlbl.font.name = 'Cambria'
                r_tlbl.font.size = Pt(9.5)
                
                r_tttl = p_tc.add_run(tc_m.group(2).strip())
                r_tttl.italic = True
                r_tttl.font.name = 'Cambria'
                r_tttl.font.size = Pt(9.5)
            else:
                r_tc = p_tc.add_run(clean_tc)
                r_tc.bold = True
                r_tc.font.name = 'Cambria'
                r_tc.font.size = Pt(9.5)
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
                # Skip separator line like |:---:|:---:|
                if re.match(r'^\|[\s:\-]+\|', cur_line):
                    i += 1
                    continue
                cells = [c.strip() for c in cur_line.split('|')[1:-1]]
                if cells:
                    pipe_rows.append(cells)
                i += 1

            if pipe_rows:
                max_cols = max(len(r) for r in pipe_rows)
                word_tbl = doc.add_table(rows=len(pipe_rows), cols=max_cols)
                format_aair_table(word_tbl, max_cols, table_num=current_table_num)

                cell_font_size = 8.0 if max_cols >= 6 else 8.5
                for r_idx, r_data in enumerate(pipe_rows):
                    is_hdr = (r_idx == 0)
                    for c_idx in range(max_cols):
                        raw_c = r_data[c_idx] if c_idx < len(r_data) else ""
                        is_bold_cell = raw_c.startswith('**') and raw_c.endswith('**')
                        clean_c = raw_c.replace('**', '').replace('★', '').strip()
                        cell = word_tbl.cell(r_idx, c_idx)
                        style_table_cell(cell, clean_c, is_header=is_hdr, is_bold=is_bold_cell, font_size=cell_font_size, align=WD_ALIGN_PARAGRAPH.LEFT)

                # Spacing below table
                p_spacer = doc.add_paragraph()
                p_spacer.paragraph_format.space_before = Pt(4)
                p_spacer.paragraph_format.space_after = Pt(2)
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
                parts = [c.strip() for c in re.split(r'\s{2,}', tbl_line) if c.strip()]
                if parts:
                    table_rows.append(parts)
                i += 1

            if table_rows:
                max_cols = max(len(r) for r in table_rows)
                word_tbl = doc.add_table(rows=len(table_rows), cols=max_cols)
                format_aair_table(word_tbl, max_cols, table_num=current_table_num)

                cell_font_size = 7.5 if (current_table_num in [4, 5] or max_cols >= 6) else 8.5
                for row_idx, row_data in enumerate(table_rows):
                    is_hdr = (row_idx == 0)
                    is_subgroup = (len(row_data) == 1 and not is_hdr)
                    is_note = (len(row_data) == 1 and row_data[0].startswith('Note:'))

                    if is_note:
                        a = word_tbl.cell(row_idx, 0)
                        b = word_tbl.cell(row_idx, max_cols - 1)
                        a.merge(b)
                        style_table_cell(a, row_data[0], is_header=False, is_italic=True, font_size=7.5, align=WD_ALIGN_PARAGRAPH.LEFT)
                        continue

                    for col_idx in range(max_cols):
                        cell = word_tbl.cell(row_idx, col_idx)
                        text = row_data[col_idx] if col_idx < len(row_data) else ""
                        style_table_cell(cell, text, is_header=is_hdr, is_bold=is_subgroup, font_size=cell_font_size, align=WD_ALIGN_PARAGRAPH.LEFT)

                # Spacing below table
                p_spacer = doc.add_paragraph()
                p_spacer.paragraph_format.space_before = Pt(4)
                p_spacer.paragraph_format.space_after = Pt(2)
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

        # Handle bullet lists (Matches sample: "• Bullet text...")
        if line.startswith("• ") or line.startswith("- ") or line.startswith("* "):
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.25)
            p_b.paragraph_format.space_after = Pt(2.5)
            p_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            r_bullet = p_b.add_run("•  ")
            r_bullet.bold = True
            r_bullet.font.size = Pt(9.0)
            
            raw_item = line[2:].strip()
            # If item has a bold prefix like "**Prefix:** text"
            bp_m = re.match(r'^\*\*(.*?)\*\*(.*)', raw_item)
            if bp_m:
                r_bp_hdr = p_b.add_run(bp_m.group(1))
                r_bp_hdr.bold = True
                r_bp_hdr.font.size = Pt(9.0)
                r_bp_txt = p_b.add_run(bp_m.group(2))
                r_bp_txt.font.size = Pt(9.0)
            else:
                r_b = p_b.add_run(raw_item)
                r_b.font.size = Pt(9.0)
            i += 1
            continue

        # Handle numbered lists with bold terms (Matches sample: "1. Reliability: text...")
        num_m = re.match(r'^(\d+\.)\s+(\*\*(.*?)\*\*|\b[A-Za-z\s]+:)?\s*(.*)', line)
        if num_m and not re.match(r'^[1-6]\.\d*\.?', line) and not line.startswith("["):
            p_num = doc.add_paragraph()
            p_num.paragraph_format.left_indent = Inches(0.25)
            p_num.paragraph_format.space_after = Pt(3)
            p_num.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            
            r_num = p_num.add_run(num_m.group(1) + " ")
            r_num.bold = True
            r_num.font.size = Pt(9.0)
            
            tag = num_m.group(2)
            rest = num_m.group(4)
            if tag:
                clean_tag = tag.replace("**", "").strip()
                r_tag = p_num.add_run(clean_tag + " ")
                r_tag.bold = True
                r_tag.font.size = Pt(9.0)
            if rest:
                r_rest = p_num.add_run(rest.strip())
                r_rest.font.size = Pt(9.0)
            i += 1
            continue

        # Regular body paragraphs
        if line.strip():
            p_body = doc.add_paragraph()
            p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_body.paragraph_format.space_after = Pt(4.5)
            r_body = p_body.add_run(line.strip())
            r_body.font.size = Pt(9.5)

        i += 1

    doc.save(docx_path)
    print(f"[SUCCESS] Generated: {docx_path}")

if __name__ == "__main__":
    md_file = r"d:\play\RAG\04_aair_submission_package\manuscript_draft_aair.md"
    docx_file = r"d:\play\RAG\04_aair_submission_package\Manuscript_AAIR.docx"
    create_aair_document(md_file, docx_file)
