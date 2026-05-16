import streamlit as st

st.set_page_config(
    page_title="JobFit AI – Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* Reset & base */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Hero header */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed22, #06b6d422);
    border: 1px solid #7c3aed55;
    color: #a78bfa;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 70%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* Cards */
.card {
    background: #13131a;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: #7c3aed44; }
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #7c3aed;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Score ring */
.score-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem;
}
.score-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    font-family: 'Syne', sans-serif;
}
.score-num {
    font-size: 2.8rem;
    font-weight: 800;
    line-height: 1;
}
.score-label { font-size: 0.7rem; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase; }

/* Skill tags */
.tag {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    margin: 0.2rem;
}
.tag-match  { background: #05966922; color: #34d399; border: 1px solid #05966944; }
.tag-miss   { background: #dc262622; color: #f87171; border: 1px solid #dc262644; }
.tag-jd     { background: #7c3aed22; color: #a78bfa; border: 1px solid #7c3aed44; }

/* Progress bar */
.progress-wrap { margin: 0.5rem 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.82rem; color: #94a3b8; margin-bottom: 0.3rem; }
.progress-bar { height: 6px; background: #1e1e2e; border-radius: 999px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #7c3aed, #38bdf8); transition: width 1s ease; }

/* Cover letter box */
.cover-box {
    background: #0d0d14;
    border: 1px solid #1e1e2e;
    border-left: 3px solid #7c3aed;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cbd5e1;
    white-space: pre-wrap;
}

/* Roadmap step */
.roadmap-step {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    padding: 0.8rem 0;
    border-bottom: 1px solid #1e1e2e;
}
.roadmap-step:last-child { border-bottom: none; }
.step-num {
    min-width: 28px; height: 28px;
    background: linear-gradient(135deg, #7c3aed, #38bdf8);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; font-family: 'Syne', sans-serif;
}
.step-content h4 { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.2rem; }
.step-content p  { font-size: 0.8rem; color: #64748b; line-height: 1.5; }

/* Streamlit overrides */
div[data-testid="stTextArea"] textarea {
    background: #0d0d14 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px #7c3aed22 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 2rem !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

div[data-testid="stFileUploader"] {
    background: #0d0d14 !important;
    border: 1px dashed #1e1e2e !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] {
    background: #13131a !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 12px !important;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #7c3aed55, transparent);
    margin: 2rem 0;
}

/* Alert boxes */
.alert-info {
    background: #38bdf822;
    border: 1px solid #38bdf844;
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #7dd3fc;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
import sys
sys.path.insert(0, "/home/claude/job-analyzer")

from utils.extractor  import extract_text_from_pdf, extract_text_from_docx
from utils.analyzer   import analyze_match
from utils.ai_engine  import (
    extract_jd_insights,
    generate_cover_letter_bullets,
    generate_skill_roadmap,
    generate_overall_summary,
)
import json

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">AI-Powered · NLP · Resume Intelligence</div>
  <h1>JobFit AI</h1>
  <p>Paste a job description, upload your resume — get your match score, skill gaps, cover letter bullets & a learning roadmap in seconds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Input columns ─────────────────────────────────────────────────────────────
col_jd, col_res = st.columns(2, gap="large")

with col_jd:
    st.markdown('<div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area(
        label="jd",
        placeholder="Paste the full job description here…",
        height=280,
        label_visibility="collapsed",
    )

with col_res:
    st.markdown('<div class="card-title">📄 Your Resume</div>', unsafe_allow_html=True)
    resume_file = st.file_uploader(
        "Upload resume (PDF or DOCX)",
        type=["pdf", "docx"],
        label_visibility="collapsed",
    )
    resume_text_manual = st.text_area(
        label="resume_manual",
        placeholder="…or paste your resume text here",
        height=200,
        label_visibility="collapsed",
    )

# ── Analyze button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze_btn = st.button("⚡ Analyze My Fit", use_container_width=True)

# ── Processing ────────────────────────────────────────────────────────────────
if analyze_btn:
    # Extract resume text
    resume_text = ""
    if resume_file:
        if resume_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        elif resume_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(resume_file)
    if not resume_text:
        resume_text = resume_text_manual.strip()

    if not jd_text.strip():
        st.error("⚠️ Please paste a job description.")
    elif not resume_text:
        st.error("⚠️ Please upload or paste your resume.")
    else:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.spinner("🔍 Analyzing your profile…"):
            # NLP-based analysis
            match_data  = analyze_match(resume_text, jd_text)
            # AI insights
            jd_insights = extract_jd_insights(jd_text)
            cover_pts   = generate_cover_letter_bullets(resume_text, jd_text, match_data)
            roadmap     = generate_skill_roadmap(match_data["missing_skills"], jd_insights)
            summary     = generate_overall_summary(match_data, jd_insights)

        score = match_data["score"]

        # ── Score colour ─────────────────────────────────────────────────────
        if score >= 75:
            ring_color  = "linear-gradient(135deg, #059669, #34d399)"
            score_color = "#34d399"
            verdict     = "Strong Match 🎉"
        elif score >= 50:
            ring_color  = "linear-gradient(135deg, #d97706, #fbbf24)"
            score_color = "#fbbf24"
            verdict     = "Moderate Match 🔧"
        else:
            ring_color  = "linear-gradient(135deg, #dc2626, #f87171)"
            score_color = "#f87171"
            verdict     = "Needs Work 📚"

        # ── Layout ───────────────────────────────────────────────────────────
        top_left, top_right = st.columns([1, 2], gap="large")

        # Score card
        with top_left:
            st.markdown(f"""
            <div class="card score-wrap">
              <div class="score-ring" style="background:{ring_color}; box-shadow: 0 0 40px {score_color}44;">
                <span class="score-num" style="color:white;">{score}%</span>
                <span class="score-label" style="color:rgba(255,255,255,0.7);">Match</span>
              </div>
              <div style="font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:700; color:{score_color};">{verdict}</div>
              <div style="font-size:0.82rem; color:#64748b; margin-top:0.4rem; text-align:center;">{summary}</div>
            </div>
            """, unsafe_allow_html=True)

        # Skill breakdown
        with top_right:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🧠 Skill Breakdown</div>', unsafe_allow_html=True)

            for cat, pct in match_data["category_scores"].items():
                st.markdown(f"""
                <div class="progress-wrap">
                  <div class="progress-label"><span>{cat}</span><span>{pct}%</span></div>
                  <div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        mid_left, mid_right = st.columns(2, gap="large")

        # Matched / Missing skills
        with mid_left:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            tags = " ".join(f'<span class="tag tag-match">{s}</span>' for s in match_data["matched_skills"])
            st.markdown(tags or "<span style='color:#64748b;font-size:0.85rem;'>None detected</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with mid_right:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            tags = " ".join(f'<span class="tag tag-miss">{s}</span>' for s in match_data["missing_skills"])
            st.markdown(tags or "<span style='color:#64748b;font-size:0.85rem;'>None — great match!</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # JD key requirements
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📌 What the Job is Really Looking For", expanded=True):
            req_cols = st.columns(3)
            labels = ["🎯 Core Skills", "📚 Experience Level", "💡 Nice-to-Haves"]
            keys   = ["core_skills", "experience", "nice_to_have"]
            for col, lbl, key in zip(req_cols, labels, keys):
                with col:
                    st.markdown(f"**{lbl}**")
                    items = jd_insights.get(key, [])
                    if isinstance(items, list):
                        for item in items:
                            st.markdown(f"<span class='tag tag-jd'>{item}</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span class='tag tag-jd'>{items}</span>", unsafe_allow_html=True)

        # Cover letter bullets
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("✉️ Cover Letter Bullets (AI Generated)", expanded=True):
            st.markdown('<div class="cover-box">' + cover_pts.replace("\n", "<br>") + '</div>', unsafe_allow_html=True)
            st.download_button("⬇️ Download Cover Letter Bullets", cover_pts, file_name="cover_letter_bullets.txt")

        # Skill roadmap
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🗺️ Your Personalised Skill Roadmap", expanded=True):
            steps = roadmap if isinstance(roadmap, list) else []
            for i, step in enumerate(steps, 1):
                st.markdown(f"""
                <div class="roadmap-step">
                  <div class="step-num">{i}</div>
                  <div class="step-content">
                    <h4>{step.get('skill','')}</h4>
                    <p>{step.get('how','')}</p>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # Download full report
        st.markdown("<br>", unsafe_allow_html=True)
        report = f"""JOBFIT AI — ANALYSIS REPORT
{'='*50}

MATCH SCORE: {score}%
VERDICT: {verdict}

SUMMARY:
{summary}

MATCHED SKILLS:
{', '.join(match_data['matched_skills'])}

MISSING SKILLS:
{', '.join(match_data['missing_skills'])}

COVER LETTER BULLETS:
{cover_pts}

SKILL ROADMAP:
""" + "\n".join([f"{i+1}. {s.get('skill','')}: {s.get('how','')}" for i, s in enumerate(steps)])

        _, dl_col, _ = st.columns([1, 2, 1])
        with dl_col:
            st.download_button("📥 Download Full Report", report, file_name="jobfit_report.txt", use_container_width=True)
