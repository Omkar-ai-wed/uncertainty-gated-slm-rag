import re
import html
import os

def build_aair_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.splitlines()

    html_out = []
    html_out.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Uncertainty-Gated Selective Retrieval in Quantized Small Language Models - AAIR Journal Paper</title>
<style>
  @page {
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
  }
  body {
    font-family: 'Cambria', 'Georgia', 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.4;
    color: #111;
    margin: 0 auto;
    max-width: 860px;
    padding: 30px;
    background-color: #fff;
    text-align: justify;
  }
  .header-table {
    width: 100%;
    border-collapse: collapse;
    border-bottom: 2px solid #000;
    margin-bottom: 16px;
    font-size: 8.5pt;
  }
  .header-table td {
    vertical-align: top;
    padding-bottom: 6px;
  }
  .header-left {
    text-align: left;
    line-height: 1.3;
  }
  .header-right {
    text-align: right;
    line-height: 1.3;
  }
  .journal-title {
    font-weight: bold;
    font-size: 9.5pt;
    color: #0d233a;
  }
  .doi-link {
    color: #003399;
    text-decoration: underline;
  }
  .meta-sub {
    font-size: 8.5pt;
    margin-top: 8px;
    margin-bottom: 18px;
    line-height: 1.35;
    padding: 8px 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
  }
  h1.paper-title {
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    margin: 22px 0 16px 0;
    line-height: 1.3;
    color: #0d233a;
  }
  .author-block {
    text-align: center;
    font-size: 11pt;
    margin-bottom: 8px;
  }
  .author-name {
    font-weight: bold;
  }
  .affiliation-block {
    text-align: center;
    font-size: 9pt;
    color: #444;
    margin-bottom: 20px;
    line-height: 1.35;
  }
  .abstract-box {
    margin: 18px 0;
    background: #fbfcfe;
    border-left: 3.5px solid #0288d1;
    padding: 12px 16px;
    border-radius: 2px;
  }
  .abstract-title {
    font-weight: bold;
    font-size: 10pt;
    margin-bottom: 6px;
    color: #01579b;
  }
  .abstract-text {
    font-style: italic;
    font-size: 9pt;
    text-align: justify;
    line-height: 1.42;
    color: #222;
  }
  .keywords-block {
    font-size: 9pt;
    margin-top: 10px;
    margin-bottom: 22px;
  }
  .keywords-label {
    font-weight: bold;
    font-style: italic;
    color: #01579b;
  }
  h2.sec-heading {
    font-size: 11pt;
    font-weight: bold;
    margin-top: 26px;
    margin-bottom: 8px;
    border-bottom: 1.2px solid #cbd5e1;
    padding-bottom: 3px;
    color: #0d233a;
    text-align: left;
  }
  h3.subsec-heading {
    font-size: 10pt;
    font-weight: bold;
    margin-top: 16px;
    margin-bottom: 6px;
    color: #1e3a8a;
    text-align: left;
  }
  h4.subsubsec-heading {
    font-size: 9.5pt;
    font-weight: bold;
    margin-top: 12px;
    margin-bottom: 4px;
    color: #334155;
    text-align: left;
  }
  p {
    margin-top: 4px;
    margin-bottom: 8px;
    text-indent: 1.5em;
  }
  p.no-indent {
    text-indent: 0;
  }
  ol, ul {
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 28px;
  }
  li {
    margin-bottom: 5px;
    line-height: 1.38;
  }
  .equation {
    text-align: center;
    margin: 12px 0;
    font-style: italic;
    background: #f8fafc;
    padding: 8px 14px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    font-family: 'Cambria Math', 'Times New Roman', serif;
  }
  .eq-number {
    float: right;
    font-style: normal;
    font-weight: bold;
  }
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 14px 0;
    font-size: 8.5pt;
    border-top: 1.5px solid #000;
    border-bottom: 1.5px solid #000;
  }
  table.data-table th, table.data-table td {
    border: none;
    padding: 6px 8px;
    text-align: left;
    vertical-align: middle;
  }
  table.data-table th {
    background-color: transparent;
    font-weight: bold;
    border-bottom: 1.0px solid #000;
    color: #000;
  }
  table.data-table tr.subgroup td {
    font-weight: bold;
    font-style: italic;
    background-color: #f8fafc;
    padding-top: 7px;
  }
  .table-caption {
    font-size: 9pt;
    margin-top: 18px;
    margin-bottom: 6px;
    text-align: center;
    color: #000;
  }
  .table-caption-lbl {
    font-weight: bold;
  }
  .table-caption-title {
    font-style: italic;
  }
  figure.figure-box {
    text-align: center;
    margin: 22px 0 16px 0;
  }
  figcaption.figure-caption {
    font-size: 9pt;
    font-weight: bold;
    text-align: center;
    margin-top: 8px;
    color: #0f172a;
  }
  .algorithm-box {
    margin: 14px 0;
    padding: 12px 14px;
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 8pt;
    line-height: 1.4;
    white-space: pre-wrap;
    text-align: left;
  }
  .reference-list {
    font-size: 8.5pt;
    line-height: 1.35;
    padding-left: 20px;
    list-style-type: none;
  }
  .reference-list li {
    text-indent: -1.8em;
    padding-left: 1.8em;
    margin-bottom: 6px;
  }
  .page-footer {
    border-top: 1px solid #cbd5e1;
    margin-top: 36px;
    padding-top: 8px;
    font-size: 8pt;
    text-align: center;
    color: #64748b;
  }
</style>
</head>
<body>

<table class="header-table">
  <tr>
    <td class="header-left">
      <span class="journal-title">Advances in Artificial Intelligence Research (AAIR)</span><br>
      e-ISSN: 2757-7422<br>
      <a href="https://dergipark.org.tr/en/pub/aair" class="doi-link" target="_blank">https://dergipark.org.tr/en/pub/aair</a>
    </td>
    <td class="header-right">
      <strong>Original Research Article</strong><br>
      Target Journal: AAIR (DergiPark / ULAKBİM TR Dizin)<br>
      Academic Year: 2025–26 &nbsp;|&nbsp; Peer-Review Submission Draft
    </td>
  </tr>
</table>

<div class="meta-sub">
  <strong>*Corresponding Author:</strong> Omkar Sachin Shedage &lt;<a href="mailto:omkarshedage1977@gmail.com" class="doi-link">omkarshedage1977@gmail.com</a>&gt;<br>
  <strong>Department & Institution:</strong> Department of Artificial Intelligence and Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra 411041, India<br>
  <strong>GitHub Repository:</strong> <a href="https://github.com/Omkar-ai-wed/uncertainty-gated-slm-rag" class="doi-link" target="_blank">https://github.com/Omkar-ai-wed/uncertainty-gated-slm-rag</a>
</div>

<h1 class="paper-title">Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment</h1>

<div class="author-block">
  <span class="author-name">Omkar Sachin Shedage<sup>1,*</sup></span>, 
  <span class="author-name">Prof. Snehal Bhoge<sup>2</sup></span>
</div>

<div class="affiliation-block">
  <sup>1,2</sup> Department of Artificial Intelligence and Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra, India
</div>
""")

    in_body = False
    current_table_caption = ""
    i = 0

    while i < len(lines):
        line = lines[i].rstrip('\r\n')

        if not in_body:
            if line.startswith("Abstract"):
                in_body = True
            else:
                i += 1
                continue

        if line.startswith("Abstract"):
            i += 1
            abs_text = lines[i].strip() if i < len(lines) else ""
            html_out.append(f"""
<div class="abstract-box">
  <div class="abstract-title">Abstract</div>
  <div class="abstract-text">{html.escape(abs_text)}</div>
</div>
""")
            i += 1
            continue

        if line.startswith("Keywords:"):
            kw_body = line.replace("Keywords:", "").strip()
            html_out.append(f"""
<div class="keywords-block">
  <span class="keywords-label">Keywords:</span> {html.escape(kw_body)}
</div>
""")
            i += 1
            continue

        # Skip Mermaid block in main text, handle it with Figure 1 image
        if line.strip().startswith("```mermaid"):
            mermaid_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                mermaid_lines.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip().startswith("```"):
                i += 1
            
            fig_caption = "Figure 1. Architectural flowchart of the Uncertainty-Gated Selective Retrieval system."
            mermaid_code = html.escape("\n".join(mermaid_lines))
            html_out.append(f"""
<figure class="figure-box">
  <img src="figure1_architecture.png" alt="Figure 1: Architectural flowchart of the Uncertainty-Gated Selective Retrieval system" style="max-width: 98%; height: auto; border: 1px solid #c5d0dc; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin: 8px auto; display: block;" />
  <figcaption class="figure-caption">{fig_caption}</figcaption>
  
  <details style="max-width: 98%; margin: 12px auto; text-align: left; background: #fbfcfe; border: 1px solid #d0d7de; border-radius: 6px; padding: 8px 12px; font-size: 8.5pt;">
    <summary style="cursor: pointer; font-weight: bold; color: #0969da;">Click to view Mermaid Diagram Source</summary>
    <pre style="margin-top: 8px; background: #f6f8fa; padding: 10px; border-radius: 4px; overflow-x: auto; font-family: Consolas, monospace; font-size: 8pt; line-height: 1.4;">{mermaid_code}</pre>
  </details>
</figure>
""")
            while i < len(lines) and (lines[i].strip().startswith("![Figure 1") or lines[i].strip().startswith("Figure 1.")):
                i += 1
            continue

        # Skip redundant standalone Figure 1 if already handled
        if line.strip().startswith("![Figure 1") or line.strip().startswith("Figure 1."):
            i += 1
            continue

        # Sub-subsections: e.g. 3.6.1. Evaluated Model Architectures or 4.7.1. Case 1
        h3_match = re.match(r'^([1-6]\.\d+\.\d+\.?)\s+(.*)', line.strip())
        if h3_match and len(line.strip()) < 100:
            html_out.append(f'<h4 class="subsubsec-heading">{html.escape(line.strip())}</h4>')
            i += 1
            continue

        # Subsections: e.g. 2.1., 3.1., 4.4., 5.2., etc.
        h2_match = re.match(r'^([1-6]\.\d+\.?)\s+(.*)', line.strip())
        if h2_match and len(line.strip()) < 100:
            html_out.append(f'<h3 class="subsec-heading">{html.escape(line.strip())}</h3>')
            i += 1
            continue

        # Major Section Headings: e.g. 1. Introduction, 2. Related Work, etc.
        h1_match = re.match(r'^([1-6]\.?)\s+([A-Za-z\s,&/]+)$', line.strip())
        if h1_match or line.strip() in ["Data and Code Availability", "Declaration of Interest", "Acknowledgement", "References"]:
            html_out.append(f'<h2 class="sec-heading">{html.escape(line.strip())}</h2>')
            i += 1
            continue

        # Table Captions (Strictly centered above table)
        tc_m = re.match(r'^\*?\*?(Table\s+[0-9R]+[\.:].*?)\*?\*?$', line.strip())
        if tc_m:
            current_table_caption = tc_m.group(1).replace("**", "").strip()
            i += 1
            continue

        # Pipe Table Parsing
        if line.strip().startswith('|') and line.strip().endswith('|'):
            p_rows = []
            while i < len(lines):
                cur_l = lines[i].strip()
                if not cur_l.startswith('|') or not cur_l.endswith('|'):
                    break
                # Skip markdown separator rows like |:---|:---:|---|
                if re.match(r'^\|[\s:\-\|]+\|$', cur_l):
                    i += 1
                    continue
                cells = [c.strip() for c in cur_l.split('|')[1:-1]]
                # Double check that this isn't a separator row that slipped through
                if all(re.match(r'^:?-+:?$', c) for c in cells if c):
                    i += 1
                    continue
                if cells:
                    p_rows.append(cells)
                i += 1

            if p_rows:
                if current_table_caption:
                    m = re.match(r'^(Table\s+[0-9R]+[\.:]?)\s*(.*)', current_table_caption)
                    if m:
                        lbl = html.escape(m.group(1).rstrip('.') + '.')
                        ttl = html.escape(m.group(2).strip())
                        html_out.append(f'<div class="table-caption"><span class="table-caption-lbl">{lbl}</span> <span class="table-caption-title">{ttl}</span></div>')
                    else:
                        html_out.append(f'<div class="table-caption">{html.escape(current_table_caption)}</div>')
                    current_table_caption = ""
                html_out.append('<table class="data-table">')
                for r_idx, row in enumerate(p_rows):
                    tag = 'th' if r_idx == 0 else 'td'
                    html_out.append('  <tr>')
                    for c_idx, cell in enumerate(row):
                        c_clean = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(cell))
                        html_out.append(f'    <{tag} style="text-align:left;">{c_clean}</{tag}>')
                    html_out.append('  </tr>')
                html_out.append('</table>')
            continue

        # ASCII / Dashed Table Parsing
        if set(line.strip()) in [{'-'}, {'─'}, {'='}] and len(line.strip()) > 5:
            i += 1
            t_rows = []
            while i < len(lines):
                tl = lines[i].rstrip('\r\n')
                if not tl.strip():
                    break
                if set(tl.strip()) in [{'-'}, {'─'}, {'='}] and len(tl.strip()) > 5:
                    i += 1
                    continue
                cells = [c.strip() for c in re.split(r'\s{2,}', tl) if c.strip()]
                if cells:
                    t_rows.append(cells)
                i += 1

            if t_rows:
                if current_table_caption:
                    m = re.match(r'^(Table\s+[0-9R]+[\.:]?)\s*(.*)', current_table_caption)
                    if m:
                        lbl = html.escape(m.group(1).rstrip('.') + '.')
                        ttl = html.escape(m.group(2).strip())
                        html_out.append(f'<div class="table-caption"><span class="table-caption-lbl">{lbl}</span> <span class="table-caption-title">{ttl}</span></div>')
                    else:
                        html_out.append(f'<div class="table-caption">{html.escape(current_table_caption)}</div>')
                    current_table_caption = ""
                html_out.append('<table class="data-table">')
                for r_idx, row in enumerate(t_rows):
                    tag = 'th' if r_idx == 0 else 'td'
                    is_sub = (len(row) == 1 and r_idx > 0 and not row[0].startswith('Note:'))
                    is_note = (len(row) == 1 and row[0].startswith('Note:'))
                    if is_note:
                        html_out.append(f'  <tr class="note-row"><td colspan="{max(len(r) for r in t_rows)}" style="text-align:left;">{html.escape(row[0])}</td></tr>')
                        continue
                    tr_cls = ' class="subgroup"' if is_sub else ''
                    html_out.append(f'  <tr{tr_cls}>')
                    for c_idx, cell in enumerate(row):
                        html_out.append(f'    <{tag} style="text-align:left;">{html.escape(cell)}</{tag}>')
                    html_out.append('  </tr>')
                html_out.append('</table>')
            continue

        # Algorithm Box
        if line.startswith("Algorithm 1:"):
            alg_lines = [line]
            i += 1
            while i < len(lines):
                al = lines[i].rstrip('\r\n')
                if set(al.strip()) in [{'-'}, {'─'}, {'='}] and len(al.strip()) > 5:
                    if len(alg_lines) > 2:
                        break
                    else:
                        i += 1
                        continue
                alg_lines.append(al)
                i += 1
            html_out.append(f'<div class="algorithm-box">{html.escape(chr(10).join(alg_lines))}</div>')
            continue

        # Numbered Equations
        eq_match = re.search(r'\(([1-7])\)\s*$', line)
        if eq_match and any(tok in line for tok in ["P_theta", "H(y_m)", "U(q)", "Delta(q)", "S_sim", "E_q", "W_quant", "L_ret", "Score"]):
            eq_num = eq_match.group(1)
            eq_body = line[:eq_match.start()].strip()
            html_out.append(f'<div class="equation">{html.escape(eq_body)} <span class="eq-number">({eq_num})</span></div>')
            i += 1
            continue

        # Bullet lists
        if line.startswith("• ") or line.startswith("- ") or line.startswith("* "):
            items = []
            while i < len(lines) and (lines[i].startswith("• ") or lines[i].startswith("- ") or lines[i].startswith("* ")):
                b_text = re.sub(r'^[•\-\*]\s+', '', lines[i]).strip()
                b_text_esc = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html.escape(b_text))
                items.append(f'<li>{b_text_esc}</li>')
                i += 1
            html_out.append('<ul>' + "".join(items) + '</ul>')
            continue

        # Numbered list items (e.g. "1. Context Distraction...", "2. Computational...", etc.)
        num_m = re.match(r'^(\d+\.)\s+(.*)', line)
        if num_m:
            items = []
            while i < len(lines):
                nm = re.match(r'^(\d+\.)\s+(.*)', lines[i])
                if not nm:
                    break
                # Don't grab actual headings like "1. Introduction" if formatted as such
                if re.match(r'^[1-6]\.\s+[A-Za-z\s,&/]+$', lines[i].strip()):
                    break
                item_content = nm.group(2).strip()
                # bold leading phrase if it has a colon
                if ':' in item_content:
                    parts = item_content.split(':', 1)
                    item_formatted = f'<strong>{html.escape(parts[0])}:</strong> {html.escape(parts[1])}'
                else:
                    item_formatted = html.escape(item_content)
                item_formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', item_formatted)
                items.append(f'<li>{item_formatted}</li>')
                i += 1
            if items:
                html_out.append('<ol>' + "".join(items) + '</ol>')
                continue

        # References list item
        ref_m = re.match(r'^\[(\d+)\]\s+(.*)', line)
        if ref_m:
            ref_items = []
            while i < len(lines):
                rm = re.match(r'^\[(\d+)\]\s+(.*)', lines[i])
                if not rm:
                    break
                ref_text = html.escape(rm.group(2))
                # Safe DOI autolinking without nesting
                def link_doi(match):
                    doi_id = match.group(2)
                    return f'{match.group(1)}<a href="https://doi.org/{doi_id}" class="doi-link" target="_blank">{doi_id}</a>'
                ref_text = re.sub(r'(doi:\s*)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', link_doi, ref_text)
                # Standalone URLs that are NOT preceded by href="
                ref_text = re.sub(r'(?<!href=")(https?://[^\s<;,]+)', r'<a href="\1" class="doi-link" target="_blank">\1</a>', ref_text)
                ref_items.append(f'<li>[{rm.group(1)}] {ref_text}</li>')
                i += 1
            html_out.append('<ul class="reference-list">' + "\n".join(ref_items) + '</ul>')
            continue

        # Normal Paragraph
        if line.strip():
            p_text = html.escape(line.strip())
            # Bold markdown conversion
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', p_text)
            p_text = re.sub(r'(?<!href=")(https?://[^\s<;,]+)', r'<a href="\1" class="doi-link" target="_blank">\1</a>', p_text)
            html_out.append(f'<p>{p_text}</p>')

        i += 1

    html_out.append("""
<div class="page-footer">
  Advances in Artificial Intelligence Research (AAIR) &nbsp;|&nbsp; e-ISSN: 2757-7422 &nbsp;|&nbsp; Manuscript Submission Draft
</div>
</body>
</html>
""")

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(html_out))

    print(f"[SUCCESS] Generated HTML: {html_path}")

if __name__ == "__main__":
    md_in = r"d:\play\RAG\04_aair_submission_package\manuscript_draft_aair.md"
    html_out_path = r"d:\play\RAG\04_aair_submission_package\manuscript_draft_aair.html"
    build_aair_html(md_in, html_out_path)
