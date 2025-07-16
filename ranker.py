import os
import pandas as pd
from pdf_parser import extract_text_from_pdf, extract_name
from matcher import compute_similarity, extract_skills

def extract_jd_text(jd_path):
    if jd_path.endswith('.txt'):
        with open(jd_path, 'r', encoding='utf-8') as f:
            return f.read()
    elif jd_path.endswith('.pdf'):
        return extract_text_from_pdf(jd_path)
    else:
        raise ValueError("Unsupported JD file format. Use .txt or .pdf")

def rank_resumes(jd_path, resumes_folder):
    jd_text = extract_jd_text(jd_path)
    jd_skills = set(extract_skills(jd_text))
    scores = []

    for resume_file in os.listdir(resumes_folder):
        if resume_file.endswith(".pdf"):
            path = os.path.join(resumes_folder, resume_file)
            resume_text = extract_text_from_pdf(path)
            resume_name = extract_name(resume_text)
            resume_skills = set(extract_skills(resume_text))

            matched_skills = list(jd_skills & resume_skills)
            missing_skills = list(jd_skills - resume_skills)

            score = compute_similarity(resume_text, jd_text)
            scores.append({
                "Candidate": resume_name,
                "File": resume_file,
                "Match Score (%)": round(score * 100, 2),
                "Matched Skills": ", ".join(matched_skills),
                "Missing Skills": ", ".join(missing_skills)
            })

    df = pd.DataFrame(scores)
    df = df.sort_values(by="Match Score (%)", ascending=False)
    return df
