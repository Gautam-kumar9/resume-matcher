import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.ranker import rank_resumes
import shutil
from dotenv import load_dotenv
load_dotenv()

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    plotting_available = True
except ModuleNotFoundError:
    plotting_available = False

st.set_page_config(page_title="AI Resume Matcher Advanced", layout="wide")

# ---------- Custom CSS Styling ----------
st.markdown("""
    <style>
    /* Custom font and background */
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9fafe;
    }
    h1, h2, h3, h4 {
        color: #202020;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: None;
        padding: 8px 20px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stFileUploader>div>div>div>button {
        background-color: #0366d6;
        color: white;
    }
    .stTextArea textarea {
        background-color: #000 !important; color: #fff !important;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    .css-1kyxreq, .css-1n76uvr, .css-1v3fvcr { 
        padding-top: 0px !important; 
    }
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Project Details", "About Me"])

if page == "Home":
    st.title("🤖 AI Resume Matcher & Skill Advisor")
    st.markdown("Upload a Job Description (.txt or .pdf) and multiple resumes (.pdf) to get detailed match analysis.")

    st.subheader("✏️ Enter or Upload Job Description")
    jd_text_input = st.text_area("Or type your job description here:")
    uploaded_jd = st.file_uploader("Upload Job Description (.txt or .pdf)", type=["txt", "pdf"])
    uploaded_resumes = st.file_uploader("Upload Resumes (.pdf)", type=["pdf"], accept_multiple_files=True)

    if (uploaded_jd or jd_text_input) and uploaded_resumes:
        jd_text = jd_text_input
        jd_ext = "txt"
        if uploaded_jd:
            jd_ext = uploaded_jd.name.split('.')[-1]
            jd_path = f"temp_jd.{jd_ext}"
            with open(jd_path, "wb") as f:
                f.write(uploaded_jd.read())
        else:
            jd_path = "temp_jd.txt"
            with open(jd_path, "w", encoding="utf-8") as f:
                f.write(jd_text_input)

        resumes_dir = "temp_resumes"
        os.makedirs(resumes_dir, exist_ok=True)
        for file in uploaded_resumes:
            with open(os.path.join(resumes_dir, file.name), "wb") as f:
                f.write(file.read())

        st.subheader("📍 Job Description Preview")
        if uploaded_jd and jd_ext == "pdf":
            from app.utils.pdf_parser import extract_text_from_pdf
            jd_text = extract_text_from_pdf(jd_path)
        elif uploaded_jd and jd_ext == "txt":
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_text = f.read()

        st.text_area("JD Content", jd_text, height=200)

        st.subheader("🧠 Suggestions to Improve JD (Local AI)")
        def rule_based_jd_feedback(jd_text):
            suggestions = []
            if len(jd_text) < 100:
                suggestions.append("The job description is very short. Consider adding more details about responsibilities and requirements.")
            if "salary" not in jd_text.lower():
                suggestions.append("You may want to include salary or compensation details to attract more candidates.")
            if "experience" not in jd_text.lower():
                suggestions.append("Mentioning required years of experience could help filter relevant candidates.")
            if "responsibilities" not in jd_text.lower():
                suggestions.append("Consider outlining job responsibilities clearly.")
            if "requirements" not in jd_text.lower():
                suggestions.append("List key requirements or skills expected from candidates.")
            return suggestions if suggestions else ["The job description looks well-structured!"]

        if st.button("Suggest Improvements to JD"):
            with st.spinner("Analyzing JD with basic AI logic..."):
                feedback = rule_based_jd_feedback(jd_text)
                st.markdown("### ✍️ Suggested Improvements:")
                for suggestion in feedback:
                    st.markdown(f"- {suggestion}")

        st.subheader("🔍 Ranking Resumes...")
        df = rank_resumes(jd_path, resumes_dir)
        st.success("✅ Matching Complete")
        st.dataframe(df)

        st.subheader("📈 Suggestions for Candidate Skill Improvement")
        for _, row in df.iterrows():
            st.markdown(f"#### Candidate: {row['Candidate']}")
            missing_skills = row['Missing Skills']
            if missing_skills:
                st.markdown(f"**Skills to Improve or Learn:** {missing_skills}")
            else:
                st.markdown("✅ This candidate matches all required skills!")

        if plotting_available:
            st.subheader("📊 Skill Matching Graph")
            num_candidates = len(df)
            for i in range(0, num_candidates, 2):
                fig, axes = plt.subplots(1, 2, figsize=(6, 2.5))
                for j in range(2):
                    if i + j < num_candidates:
                        row = df.iloc[i + j]
                        candidate = row['Candidate']
                        matched = len(row['Matched Skills'].split(', ')) if row['Matched Skills'] else 0
                        missing = len(row['Missing Skills'].split(', ')) if row['Missing Skills'] else 0
                        ax = axes[j]
                        sns.barplot(x=["Matched", "Missing"], y=[matched, missing], palette=["green", "red"], ax=ax)
                        ax.set_title(f"{candidate}", fontsize=10)
                        ax.set_ylabel("Skills", fontsize=8)
                        ax.set_xlabel("")
                        ax.tick_params(axis='x', labelsize=8)
                        ax.tick_params(axis='y', labelsize=8)
                    else:
                        fig.delaxes(axes[j])
                plt.tight_layout()
                st.pyplot(fig)
        else:
            st.warning("matplotlib or seaborn is not installed. Please install them to see graphs.")

        shutil.rmtree(resumes_dir)
        os.remove(jd_path)

elif page == "Project Details":
    st.title("📚 Project Details")
    st.markdown("""
    **AI Resume Matcher & Skill Advisor** is a smart recruitment assistance platform built to improve candidate-job matching efficiency.

    ### 🔧 Features:
    - **Automated Resume Parsing:** Extracts and cleans resume content from PDF files.
    - **JD Input Options:** Accepts job descriptions via file upload or direct text entry.
    - **Semantic Skill Matching:** Uses NLP (Spacy/BERT) and keyword techniques to match skills from resumes with job descriptions.
    - **Skill Gap Analysis:** Highlights missing skills for each candidate and suggests improvements.
    - **Rule-Based JD Advisor:** Offers local, AI-style recommendations to enhance clarity and effectiveness of JDs.
    - **Visual Insights:** Provides bar charts comparing matched vs missing skills for all candidates.
    - **Modern UI:** Streamlit-based responsive frontend with a sidebar navigation experience.

    ### 🧠 Why This Project?
    Hiring teams often struggle with filtering high volumes of resumes. This tool:
    - Saves recruiter time
    - Enhances fairness by matching on actual content
    - Encourages candidates to upskill via skill-gap suggestions

    ### ⚙️ Tech Stack:
    - **Language:** Python
    - **Framework:** Streamlit
    - **Libraries:** Pandas, Matplotlib, Seaborn, Spacy
    - **Optional:** OpenAI for GPT-4 suggestions (if API is enabled)

    """)

elif page == "About Me":
    st.title("👨‍🎓 About Me")
    st.markdown("""
    **Gautam Kumar**  
    Roll No: 231212013  
    Email: 231212013@nitdelhi.ac.in  
    College: National Institute of Technology Delhi  
    
    This project was built with ❤️ for learning and innovation.
    
    ---
    © 2025 Gautam Kumar. All rights reserved.
    """)
