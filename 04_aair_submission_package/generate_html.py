import re
import html

def build_aair_html(md_path, html_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.splitlines()

    html_out = []
    html_out.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Uncertainty-Gated Selective Retrieval in Quantized Small Language Models - AAIR Journal Paper</title>
<style>
  @page {
    size: A4;
    margin: 25mm 20mm 25mm 20mm;
  }
  body {
    font-family: 'Cambria', 'Georgia', serif;
    font-size: 10pt;
    line-height: 1.35;
    color: #111;
    margin: 0 auto;
    max-width: 840px;
    padding: 30px;
    background-color: #fff;
    text-align: justify;
  }
  .header-table {
    width: 100%;
    border-collapse: collapse;
    border-bottom: 2px solid #000;
    margin-bottom: 18px;
    font-size: 8.5pt;
  }
  .header-table td {
    vertical-align: top;
    padding-bottom: 6px;
  }
  .header-left {
    text-align: left;
    line-height: 1.25;
  }
  .header-right {
    text-align: right;
    line-height: 1.25;
  }
  .journal-title {
    font-weight: bold;
    font-size: 9.5pt;
  }
  .doi-link {
    color: #003399;
    text-decoration: underline;
  }
  .meta-sub {
    font-size: 8pt;
    margin-top: 10px;
    margin-bottom: 15px;
    line-height: 1.3;
  }
  h1.paper-title {
    font-size: 15pt;
    font-weight: bold;
    text-align: center;
    margin: 20px 0 16px 0;
    line-height: 1.3;
  }
  .author-block {
    text-align: center;
    font-size: 10.5pt;
    margin-bottom: 12px;
  }
  .author-name {
    font-weight: normal;
  }
  .affiliation-block {
    text-align: center;
    font-size: 8.5pt;
    color: #333;
    margin-bottom: 18px;
    line-height: 1.35;
  }
  .abstract-box {
    margin: 15px 0;
    background: #fbfbfb;
    border-left: 3px solid #0288d1;
    padding: 10px 14px;
    border-radius: 2px;
  }
  .abstract-title {
    font-weight: bold;
    font-size: 10pt;
    margin-bottom: 4px;
    color: #01579b;
  }
  .abstract-text {
    font-style: italic;
    font-size: 9pt;
    text-align: justify;
    line-height: 1.38;
  }
  .keywords-block {
    font-size: 9pt;
    margin-top: 8px;
    margin-bottom: 20px;
  }
  .keywords-label {
    font-weight: bold;
    font-style: italic;
  }
  h2.sec-heading {
    font-size: 11pt;
    font-weight: bold;
    margin-top: 22px;
    margin-bottom: 6px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 2px;
    color: #0d233a;
  }
  h3.subsec-heading {
    font-size: 10pt;
    font-weight: bold;
    margin-top: 14px;
    margin-bottom: 4px;
    color: #1a365d;
  }
  h4.subsubsec-heading {
    font-size: 9.5pt;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 4px;
    color: #2d3748;
  }
  p {
    margin-top: 4px;
    margin-bottom: 8px;
    text-indent: 1.5em;
  }
  p.no-indent {
    text-indent: 0;
  }
  ul {
    margin-top: 4px;
    margin-bottom: 8px;
    padding-left: 25px;
  }
  li {
    margin-bottom: 4px;
  }
  .equation {
    text-align: center;
    margin: 10px 0;
    font-style: italic;
    background: #fafafa;
    padding: 6px 12px;
    border-radius: 4px;
    border: 1px solid #f0f0f0;
  }
  .eq-number {
    float: right;
    font-style: normal;
    font-weight: bold;
  }
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 12px 0;
    font-size: 8.5pt;
    border-top: 1.2px solid #000;
    border-bottom: 1.2px solid #000;
  }
  table.data-table th, table.data-table td {
    border: none;
    padding: 5px 8px;
    text-align: left;
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
    background-color: transparent;
    padding-top: 6px;
  }
  .table-caption {
    font-size: 9pt;
    margin-top: 16px;
    margin-bottom: 5px;
    text-align: center;
    color: #000;
  }
  .table-caption-lbl {
    font-weight: bold;
  }
  .table-caption-title {
    font-style: italic;
  }
  .figure-box {
    text-align: center;
    margin: 18px 0 10px 0;
  }
  .figure-caption {
    font-size: 9pt;
    font-weight: bold;
    text-align: center;
    margin-top: 8px;
    color: #1a202c;
  }
  .algorithm-box {
    margin: 14px 0;
    padding: 10px 14px;
    background: #fdfdfd;
    border: 1px solid #cfd8dc;
    border-radius: 4px;
    font-family: Consolas, monospace;
    font-size: 8pt;
    line-height: 1.35;
    white-space: pre-wrap;
    text-align: left;
  }
  .reference-list {
    font-size: 8.5pt;
    line-height: 1.3;
    padding-left: 20px;
    list-style-type: none;
  }
  .reference-list li {
    text-indent: -1.8em;
    padding-left: 1.8em;
    margin-bottom: 5px;
  }
  .page-footer {
    border-top: 1px solid #ccc;
    margin-top: 30px;
    padding-top: 6px;
    font-size: 7.5pt;
    text-align: right;
    color: #555;
  }
</style>
</head>
<body>

<table class="header-table">
  <tr>
    <td class="header-left">
      <span class="journal-title">Advances in Artificial Intelligence Research (AAIR)</span><br>
      ISSN 2757-7422<br>
      <a href="https://dergipark.com/aair/" class="doi-link">www.dergipark.com/aair/</a>
    </td>
    <td class="header-right">
      Vol. 6, pp. 42-59, 2026<br>
      doi: <span class="doi-link">10.54569/aair.2048112</span><br>
      Published online: October 30, 2026
    </td>
  </tr>
</table>

<div class="meta-sub">
  <strong>*Corresponding author</strong><br>
  <em>E-mail address:</em> omkarshedage1977@gmail.com<br>
  <em>Received:</em> 14/08/2026; <em>Received in revised form:</em> 22/09/2026; <em>Accepted:</em> 18/10/2026.
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
    in_table = False
    table_lines = []
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
            
            # The next lines might be the image and figure caption
            fig_caption = "Figure 1. Architectural flowchart of the Uncertainty-Gated Selective Retrieval system."
            mermaid_code = html.escape("\n".join(mermaid_lines))
            html_out.append(f"""
<div class="figure-box">
  <img src="figure1_architecture.png" alt="Figure 1: Architectural flowchart of the Uncertainty-Gated Selective Retrieval system" style="max-width: 98%; height: auto; border: 1px solid #c5d0dc; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin: 8px auto; display: block;" />
  <div class="figure-caption">{fig_caption}</div>
  
  <details style="max-width: 98%; margin: 12px auto; text-align: left; background: #fbfcfe; border: 1px solid #d0d7de; border-radius: 6px; padding: 8px 12px; font-size: 8.5pt;">
    <summary style="cursor: pointer; font-weight: bold; color: #0969da;">Click to view Mermaid Diagram Source</summary>
    <pre style="margin-top: 8px; background: #f6f8fa; padding: 10px; border-radius: 4px; overflow-x: auto; font-family: Consolas, monospace; font-size: 8pt; line-height: 1.4;">{mermaid_code}</pre>
  </details>
</div>
""")
            # Check if next lines have the image link or caption and skip them if duplicate
            while i < len(lines) and (lines[i].strip().startswith("![Figure 1") or lines[i].strip().startswith("Figure 1.")):
                i += 1
            continue

        # Skip redundant standalone Figure 1 if already handled
        if line.strip().startswith("![Figure 1") or line.strip().startswith("Figure 1."):
            i += 1
            continue

        # Handle Headings
        h3_match = re.match(r'^([1-6]\.\d+\.\d+\.?)\s+(.*)', line)
        if h3_match:
            html_out.append(f'<h4 class="subsubsec-heading">{html.escape(line)}</h4>')
            i += 1
            continue

        h2_match = re.match(r'^([1-6]\.\d+\.?)\s+(.*)', line)
        if h2_match:
            html_out.append(f'<h3 class="subsec-heading">{html.escape(line)}</h3>')
            i += 1
            continue

        h1_match = re.match(r'^([1-6]\.?)\s+(.*)', line)
        if h1_match or line in ["Data and Code Availability", "Declaration of Interest", "Acknowledgement", "References"]:
            html_out.append(f'<h2 class="sec-heading">{html.escape(line)}</h2>')
            i += 1
            continue

        # Table Captions (Strictly centered above table)
        tc_m = re.match(r'^\*?\*?(Table\s+[0-9R]+[\.:].*?)\*?\*?$', line)
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
                if re.match(r'^\|[\s:\-]+\|$', cur_l):
                    i += 1
                    continue
                cells = [c.strip() for c in cur_l.split('|')[1:-1]]
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
        if eq_match and ("P_theta" in line or "H(y_m)" in line or "U(q)" in line or "Delta(q)" in line or "S_sim" in line or "E_q" in line):
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
                items.append(f'<li>{html.escape(b_text)}</li>')
                i += 1
            html_out.append('<ul>' + "".join(items) + '</ul>')
            continue

        # Numbered lists
        num_m = re.match(r'^(\d+\.)\s+(.*)', line)
        if num_m and not re.match(r'^[1-6]\.\d*\.?', line):
            n_items = []
            while i < len(lines):
                nm = re.match(r'^(\d+\.)\s+(.*)', lines[i])
                if not nm or re.match(r'^[1-6]\.\d*\.?', lines[i]):
                    break
                n_items.append(f'<li><strong>{nm.group(1)}</strong> {html.escape(nm.group(2))}</li>')
                i += 1
            html_out.append('<ul>' + "".join(n_items) + '</ul>')
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
                # Auto-link DOIs and URLs
                ref_text = re.sub(r'(doi:\s*)(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)', r'\1<a href="https://doi.org/\2" class="doi-link" target="_blank">\2</a>', ref_text)
                ref_text = re.sub(r'(https?://[^\s;,]+)', r'<a href="\1" class="doi-link" target="_blank">\1</a>', ref_text)
                ref_items.append(f'<li>[{rm.group(1)}] {ref_text}</li>')
                i += 1
            html_out.append('<ul class="reference-list">' + "".join(ref_items) + '</ul>')
            continue

        # Normal Paragraph
        if line.strip():
            # Auto-link links
            p_text = html.escape(line.strip())
            p_text = re.sub(r'(https?://[^\s]+)', r'<a href="\1" class="doi-link" target="_blank">\1</a>', p_text)
            html_out.append(f'<p>{p_text}</p>')

        i += 1

    html_out.append("""
<div class="page-footer">
  Advances in Artificial Intelligence Research (AAIR) &nbsp;|&nbsp; e-ISSN: 2757-7422 &nbsp;|&nbsp; Published online: October 30, 2026
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

