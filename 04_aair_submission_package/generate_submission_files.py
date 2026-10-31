import os
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def generate_title_page(docx_path):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1.0)
    
    style = doc.styles['Normal']
    style.font.name = 'Cambria'
    style.font.size = Pt(10)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    p_banner = doc.add_paragraph()
    r_b = p_banner.add_run("Advances in Artificial Intelligence Research (AAIR) — Title Page")
    r_b.bold = True
    r_b.font.size = Pt(11)

    doc.add_paragraph("─" * 70)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(14)
    r_t = p_title.add_run("Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment")
    r_t.bold = True
    r_t.font.size = Pt(14)

    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.space_after = Pt(6)
    r1 = p_auth.add_run("Omkar Sachin Shedage 1,*")
    r1.bold = True
    p_auth.add_run(" , ")
    r2 = p_auth.add_run("Prof. Snehal Bhoge 2")
    r2.bold = True

    p_aff = doc.add_paragraph()
    p_aff.paragraph_format.space_after = Pt(14)
    p_aff.add_run("1,2 Department of Artificial Intelligence and Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra 411041, India").font.size = Pt(9.5)

    p_corr = doc.add_paragraph()
    p_corr.paragraph_format.space_after = Pt(14)
    r_c_hdr = p_corr.add_run("*Corresponding Author Information:\n")
    r_c_hdr.bold = True
    p_corr.add_run("Name: Omkar Sachin Shedage\n")
    p_corr.add_run("Department: Department of Artificial Intelligence and Data Science\n")
    p_corr.add_run("Institution: JSPM Narhe Technical Campus, Savitribai Phule Pune University\n")
    p_corr.add_run("City & Country: Pune, Maharashtra, India\n")
    p_corr.add_run("E-mail: omkarshedage1977@gmail.com\n")
    p_corr.add_run("GitHub: https://github.com/Omkar-ai-wed/uncertainty-gated-slm-rag\n")

    p_decl = doc.add_paragraph()
    p_decl.paragraph_format.space_after = Pt(10)
    r_dh = p_decl.add_run("Declaration of Competing Interest:\n")
    r_dh.bold = True
    p_decl.add_run("The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.")

    p_ack = doc.add_paragraph()
    r_ah = p_ack.add_run("Acknowledgement:\n")
    r_ah.bold = True
    p_ack.add_run("This research was conducted as part of the undergraduate academic seminar and capstone research project in the Department of Artificial Intelligence and Data Science at JSPM Narhe Technical Campus, Savitribai Phule Pune University. The authors express gratitude to the department faculty and laboratory staff for providing computational workstation resources.")

    doc.save(docx_path)
    print(f"[SUCCESS] Generated Title Page: {docx_path}")

def generate_blinded_manuscript(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Complete Double-Blind Anonymization
    blinded_content = content.replace("Omkar Sachin Shedage 1,* , Prof. Snehal Bhoge 2", "[Anonymized Authors for Double-Blind Review]")
    blinded_content = blinded_content.replace("omkarshedage1977@gmail.com", "[anonymized.email@blinded.edu]")
    blinded_content = blinded_content.replace("1,2 Department of Artificial Intelligence and Data Science, JSPM Narhe Technical Campus, Savitribai Phule Pune University, Pune, Maharashtra, India", "[Anonymized Institution for Double-Blind Review]")
    blinded_content = blinded_content.replace("https://github.com/Omkar-ai-wed/uncertainty-gated-slm-rag", "https://github.com/[anonymized]/uncertainty-gated-slm-rag")
    blinded_content = blinded_content.replace("JSPM Narhe Technical Campus, Savitribai Phule Pune University", "[Anonymized University]")
    
    # Anonymize Acknowledgement body for double-blind review
    ack_orig = "This research was conducted as part of the undergraduate academic seminar and capstone research project in the Department of Artificial Intelligence and Data Science at JSPM Narhe Technical Campus, Savitribai Phule Pune University. The authors express gratitude to the department faculty and laboratory staff for providing computational workstation resources."
    ack_blinded = "[Anonymized for double-blind peer review. Complete institutional and supervisory acknowledgements are documented on the Title Page.]"
    blinded_content = blinded_content.replace(ack_orig, ack_blinded)

    temp_md = os.path.join(os.path.dirname(docx_path), "temp_blinded.md")
    try:
        with open(temp_md, 'w', encoding='utf-8') as f:
            f.write(blinded_content)

        from generate_docx import create_aair_document
        create_aair_document(temp_md, docx_path)
        print(f"[SUCCESS] Generated Blinded Manuscript with figures & tables: {docx_path}")
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)

if __name__ == "__main__":
    base_dir = r"d:\play\RAG\04_aair_submission_package"
    generate_title_page(os.path.join(base_dir, "TitlePage.docx"))
    generate_blinded_manuscript(os.path.join(base_dir, "manuscript_draft_aair.md"), os.path.join(base_dir, "Manuscript_Blinded.docx"))
