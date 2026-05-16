# 🎯 JobFit AI — Resume & JD Analyzer

An AI-powered web application that analyzes how well your resume matches a job description, identifies skill gaps, generates tailored cover letter bullets, and creates a personalized learning roadmap.

---

## 🚀 Live Demo

🔗 **[Click here to try JobFit AI](https://skillmatch-app.streamlit.app/)**

---

## ✨ Features

| Feature | Tech Used |
|--------|-----------|
| Resume text extraction (PDF/DOCX) | PyPDF2, python-docx |
| Skill extraction & matching | spaCy, regex, custom taxonomy |
| Overall match score | TF-IDF + cosine similarity (sklearn) |
| Per-category skill breakdown | Custom NLP pipeline |
| JD insights (role, exp, salary) | Groq API (Llama 3.3 70b) |
| AI cover letter bullets | Groq API (Llama 3.3 70b) |
| Personalized skill roadmap | Groq API (Llama 3.3 70b) |
| Downloadable report | Streamlit |
---

## 🛠 Tech Stack

- **Python 3.10+**
- **Streamlit** — web UI
- **scikit-learn** — TF-IDF vectorization, cosine similarity
- **spaCy** — NLP text processing
- **Groq API (Llama 3.3 70b)** — AI-powered insights (free)
- **PyPDF2 + python-docx** — document parsing

---

## 📦 Installation

```bash
# 1. Clone the repo
git clone https://github.com/AmulyaReddy1122/jobfit-ai.git
cd jobfit-ai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your Groq API key
export GROQ_API_KEY="your_api_key_here"
# Windows: set GROQ_API_KEY=your_api_key_here

# 5. Run the app
streamlit run app.py
```

---

## 🔑 API Key Setup

Get a free API key at [console.groq.com](https://console.groq.com).

For Streamlit Cloud deployment, add it as a secret:
```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "your_key_here"
```

---

## 📊 How It Works

```
JD Text + Resume
     │
     ▼
┌─────────────────────────┐
│  Skill Extraction (NLP) │  ← 150+ skills across 6 categories
└────────────┬────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
Matched Skills    Missing Skills
     │                │
     └───────┬────────┘
             ▼
   TF-IDF Cosine Similarity
             │
             ▼
      Match Score (0-100%)
             │
             ▼
    Groq API Calls
   ┌──────┬──────┬──────┐
   │  JD  │Cover │Skill │
   │Insig-│Letter│Road- │
   │ hts  │Bullets│map  │
   └──────┴──────┴──────┘
```

---

## 📁 Project Structure

```
jobfit-ai/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Dependencies
├── .streamlit/
│   └── config.toml         # Theme config
└── utils/
    ├── extractor.py        # PDF/DOCX text extraction
    ├── analyzer.py         # NLP matching engine
    └── ai_engine.py        # Groq API integration
```

---

## 🎯 Results

- Extracts **150+ skills** across 6 categories (ML/AI, Programming, Cloud, etc.)
- Generates match scores combining **skill overlap (60%)** and **semantic similarity (40%)**
- Produces **5 tailored cover letter bullets** in seconds
- Creates a **prioritized 6-step learning roadmap** for skill gaps

---

## 🔮 Future Improvements

- [ ] Multi-resume comparison
- [ ] ATS (Applicant Tracking System) score simulation
- [ ] LinkedIn profile import
- [ ] Interview question generator based on JD
- [ ] Email the report directly

---

Made by **Amulya Reddy**
