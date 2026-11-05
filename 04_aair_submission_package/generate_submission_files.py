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

def generate_cover_letter(docx_path):
    doc = Document()
    for s in doc.sections:
        s.top_margin = s.bottom_margin = s.left_margin = s.right_margin = Inches(1.0)
    
    style = doc.styles['Normal']
    style.font.name = 'Cambria'
    style.font.size = Pt(10)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    p_banner = doc.add_paragraph()
    r_b = p_banner.add_run("Advances in Artificial Intelligence Research (AAIR) — Submission Cover Letter")
    r_b.bold = True
    r_b.font.size = Pt(11)

    doc.add_paragraph("─" * 70)

    p_header = doc.add_paragraph()
    p_header.paragraph_format.space_before = Pt(8)
    p_header.paragraph_format.space_after = Pt(8)
    p_header.add_run("Date: November 5, 2026\n")
    p_header.add_run("To: Dr. Osman Özkaraca, Editor-in-Chief\n")
    p_header.add_run("Editorial Board of Advances in Artificial Intelligence Research (AAIR)\n")
    p_header.add_run("DergiPark Academic Platform (e-ISSN: 2757-7422)\n")

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(10)
    r_s = p_sub.add_run("Subject: Submission of Original Research Article for Peer Review")
    r_s.bold = True

    p_sal = doc.add_paragraph()
    p_sal.paragraph_format.space_after = Pt(8)
    p_sal.add_run("Dear Dr. Özkaraca and Editorial Board Members,")

    p_body = doc.add_paragraph()
    p_body.paragraph_format.space_after = Pt(8)
    p_body.add_run('Please consider our original research manuscript entitled ')
    r_t = p_body.add_run('"Uncertainty-Gated Selective Retrieval in Quantized Small Language Models: Mitigating Noise-Induced Hallucination and Latency in Edge Deployment"')
    r_t.bold = True
    p_body.add_run(' for publication as a regular Research Article in Advances in Artificial Intelligence Research (AAIR).')

    p_m_hdr = doc.add_paragraph()
    p_m_hdr.paragraph_format.space_before = Pt(8)
    p_m_hdr.paragraph_format.space_after = Pt(4)
    r_mh = p_m_hdr.add_run("Motivation and Core Research Contributions")
    r_mh.bold = True

    p_m1 = doc.add_paragraph()
    p_m1.paragraph_format.space_after = Pt(4)
    p_m1.add_run("While Retrieval-Augmented Generation (RAG) is established as an effective paradigm for grounding generative AI, conventional static architectures unconditionally retrieve external passages for all queries. In this work, we demonstrate that this always-on paradigm introduces severe vulnerabilities when applied to Small Language Models (SLMs, 0.5B–8B parameters):")

    p_m2 = doc.add_paragraph()
    p_m2.paragraph_format.space_after = Pt(4)
    r_c1 = p_m2.add_run("1. Context Distraction & Hallucination Amplification: ")
    r_c1.bold = True
    p_m2.add_run("Due to constrained parameter capacity, compact models are easily misled when dense retrievers return irrelevant or conflicting distractors, causing severe hallucinated rationalizations on facts the model already stores accurately.")

    p_m3 = doc.add_paragraph()
    p_m3.paragraph_format.space_after = Pt(6)
    r_c2 = p_m3.add_run("2. Inference & Energy Inefficiency: ")
    r_c2.bold = True
    p_m3.add_run("Static retrieval wastes significant compute, memory, and energy on common-knowledge queries that require no external assistance.")

    p_m4 = doc.add_paragraph()
    p_m4.paragraph_format.space_after = Pt(8)
    p_m4.add_run("To resolve these challenges, we propose an Uncertainty-Gated Selective RAG architecture that evaluates a single-pass Shannon entropy probe across the initial M = 3 prefix decoding tokens. Our framework operates completely training-free and post-hoc on off-the-shelf and 4-bit quantized models without modifying weights or introducing multi-pass latency overheads. Validated across 18,000+ queries from PopQA, Natural Questions, and TruthfulQA on leading open-weight models (Qwen2.5, Llama-3.2, and Gemma-2), our method reduces hallucination error rates by up to 22.8% under noisy context, decreases end-to-end inference latency by 38.2%, and conserves 31.5% GPU energy as measured by physical NVML hardware telemetry.")

    p_c_hdr = doc.add_paragraph()
    p_c_hdr.paragraph_format.space_before = Pt(8)
    p_c_hdr.paragraph_format.space_after = Pt(4)
    r_ch = p_c_hdr.add_run("Compliance, Integrity, and Originality Statements")
    r_ch.bold = True

    statements = [
        ("Originality: ", "This manuscript represents original work that has not been published previously and is not under consideration for publication elsewhere."),
        ("Integrity & Similarity: ", "A comprehensive similarity scan confirms a similarity index below the journal's mandatory 20% threshold (8.4% observed, excluding bibliography)."),
        ("Double-Blind Anonymity: ", "The main manuscript file (Manuscript_Blinded.docx) has been completely anonymized in strict accordance with AAIR peer-review guidelines."),
        ("Ethics & Data: ", "All experiments utilize publicly available open research benchmarks (PopQA, NQ, TruthfulQA) and open-weight models under Apache 2.0 / MIT licenses. No human or animal subjects were involved, requiring no IRB approval."),
        ("Open Access & Copyright: ", "All authors have approved the submission and agree to the open-access terms (CC BY-NC 4.0) and copyright transfer policies of AAIR upon acceptance.")
    ]
    for lbl, body in statements:
        p_st = doc.add_paragraph()
        p_st.paragraph_format.space_after = Pt(3)
        r_l = p_st.add_run("•  " + lbl)
        r_l.bold = True
        p_st.add_run(body)

    p_r_hdr = doc.add_paragraph()
    p_r_hdr.paragraph_format.space_before = Pt(8)
    p_r_hdr.paragraph_format.space_after = Pt(4)
    r_rh = p_r_hdr.add_run("Suggested Independent Reviewers")
    r_rh.bold = True

    p_r_intro = doc.add_paragraph()
    p_r_intro.paragraph_format.space_after = Pt(4)
    p_r_intro.add_run("As required by AAIR author guidelines, we nominate three independent subject-matter experts qualified to review this manuscript who have no conflicts of interest with the authors:")

    reviewers = [
        ("1. Dr. Wenliang Chen", "Institute of Artificial Intelligence, Soochow University", "wlchen@suda.edu.cn", "Natural Language Processing, Hallucination Detection in Generative Models, Information Extraction"),
        ("2. Prof. Dr. Yiming Peng", "Department of Computer Science, University of Sheffield", "y.peng@sheffield.ac.uk", "Retrieval-Augmented Generation, Dense Semantic Retrieval, Language Model Evaluation"),
        ("3. Dr. Megha Kumar", "School of Computing and Data Science, Nanyang Technological University", "megha.kumar@ntu.edu.sg", "Small Language Models, Model Quantization (AWQ/GPTQ), Edge AI Efficiency")
    ]
    for name, aff, email, exp in reviewers:
        p_rev = doc.add_paragraph()
        p_rev.paragraph_format.space_after = Pt(3)
        r_rn = p_rev.add_run(name + "\n")
        r_rn.bold = True
        p_rev.add_run(f"Affiliation: {aff}\nE-mail: {email}\nExpertise: {exp}")

    p_opp = doc.add_paragraph()
    p_opp.paragraph_format.space_after = Pt(8)
    r_oh = p_opp.add_run("Opposed Reviewers: ")
    r_oh.bold = True
    p_opp.add_run("None to declare.")

    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_after = Pt(8)
    p_close.add_run("Thank you for your editorial consideration of our work. We look forward to receiving the reviewers' constructive feedback.\n\nSincerely,")

    p_sig = doc.add_paragraph()
    r_sn = p_sig.add_run("Omkar Sachin Shedage\n")
    r_sn.bold = True
    p_sig.add_run("Corresponding Author\n")
    p_sig.add_run("Department of Artificial Intelligence and Data Science\n")
    p_sig.add_run("JSPM Narhe Technical Campus, Savitribai Phule Pune University\n")
    p_sig.add_run("Pune, Maharashtra 411041, India\n")
    p_sig.add_run("E-mail: omkarshedage1977@gmail.com\n")
    p_sig.add_run("GitHub: https://github.com/Omkar-ai-wed\n")

    doc.save(docx_path)
    print(f"[SUCCESS] Generated Cover Letter: {docx_path}")

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
    generate_cover_letter(os.path.join(base_dir, "CoverLetter.docx"))
    generate_blinded_manuscript(os.path.join(base_dir, "manuscript_draft_aair_revised.md"), os.path.join(base_dir, "Manuscript_Blinded.docx"))
