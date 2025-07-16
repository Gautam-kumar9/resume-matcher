<img width="1862" height="756" alt="image" src="https://github.com/user-attachments/assets/d217d318-8cd2-499f-8046-6514630751f9" />🤖 AI Resume Matcher & Skill Advisor
Live App: https://resume-matcher-9.streamlit.app
GitHub: https://github.com/Gautam-kumar9/resume-matcher

📌 Overview
The AI Resume Matcher & Skill Advisor is a smart recruitment assistant that helps match job descriptions with resumes using natural language processing (NLP) techniques. It also provides improvement suggestions for both the job description and the resumes, helping recruiters and job seekers alike.

🔍 Features
✅ Upload and parse Job Description (PDF or TXT)

📁 Upload multiple Resumes (PDF)

📊 Resume Ranking based on JD relevance

🔎 Extracted skills with Matched vs Missing breakdown

📈 Visual graphs for skill comparison

🧠 Suggestions to improve the JD

🎨 Clean, responsive UI built using Streamlit

🗃️ No database needed — lightweight and file-based

🖥️ Demo
👉 Click here to try the live demo
📽️ Watch demo video (optional: add a Loom/YouTube link here)

💻 Tech Stack
Tool	Purpose
Python	Core Programming Language
Streamlit	Frontend Web App Framework
Spacy	NLP for skill extraction
Pandas	Data manipulation
Matplotlib & Seaborn	Data visualization
dotenv	Environment config
PyMuPDF	PDF Parsing (in pdf_parser.py)

📂 Folder Structure
bash
Copy
Edit
resume-matcher/
│
├── streamlit_app.py         # Main Streamlit app
├── ranker.py                # Resume scoring logic
├── pdf_parser.py            # PDF parsing utilities
├── .gitignore
├── requirements.txt
└── README.md
🚀 Getting Started
🛠️ Setup
bash
Copy
Edit
git clone https://github.com/Gautam-kumar9/resume-matcher.git
cd resume-matcher
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run streamlit_app.py
✏️ Example Job Description
You can paste your JD into the textbox or upload .txt or .pdf.

📄 Resumes
Upload one or more PDF resumes, and get ranked outputs with suggestions.



🙋‍♂️ About Me
Gautam Kumar
B.Tech | NIT Delhi
Roll No: 231212013
📧 231212013@nitdelhi.ac.in
🌐 GitHub - Gautam-kumar9

📜 License
This project is licensed under the MIT License.
© 2025 Gautam Kumar. All rights reserved.

⭐️ Show Your Support
If you like this project:

⭐️ Star the repo

🍴 Fork it

🐛 Report issues

📢 Share it
