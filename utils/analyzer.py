"""
NLP-based resume ↔ JD matching using sklearn + spaCy.
"""

from __future__ import annotations
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ── Comprehensive skill taxonomy ───────────────────────────────────────────────
SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "r", "sql", "java", "scala", "julia", "c++", "c#",
        "javascript", "typescript", "go", "rust", "bash", "shell",
    ],
    "ML / AI": [
        "machine learning", "deep learning", "nlp", "natural language processing",
        "computer vision", "reinforcement learning", "transfer learning",
        "generative ai", "llm", "large language model", "transformers",
        "bert", "gpt", "neural network", "cnn", "rnn", "lstm", "xgboost",
        "lightgbm", "catboost", "gradient boosting", "random forest",
        "regression", "classification", "clustering", "dimensionality reduction",
        "feature engineering", "model deployment", "mlops",
    ],
    "Libraries & Frameworks": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
        "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
        "huggingface", "spacy", "nltk", "opencv", "fastapi", "flask",
        "streamlit", "gradio", "pyspark", "dask", "ray",
    ],
    "Data Engineering": [
        "sql", "nosql", "mongodb", "postgresql", "mysql", "bigquery",
        "snowflake", "redshift", "spark", "hadoop", "kafka", "airflow",
        "dbt", "etl", "data pipeline", "data warehouse", "data lake",
        "databricks",
    ],
    "Cloud & MLOps": [
        "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
        "mlflow", "kubeflow", "ci/cd", "github actions", "terraform",
        "sagemaker", "vertex ai", "azure ml",
    ],
    "Analytics & Viz": [
        "tableau", "power bi", "looker", "excel", "eda",
        "exploratory data analysis", "a/b testing", "statistics",
        "hypothesis testing", "data visualization", "business intelligence",
    ],
}

ALL_SKILLS = {skill for skills in SKILL_CATEGORIES.values() for skill in skills}


def _normalise(text: str) -> str:
    return text.lower()


def _extract_skills(text: str) -> set[str]:
    text_lower = _normalise(text)
    found: set[str] = set()
    for skill in ALL_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def _category_scores(resume_skills: set[str], jd_skills: set[str]) -> dict[str, int]:
    scores: dict[str, int] = {}
    for cat, skills in SKILL_CATEGORIES.items():
        jd_cat   = {s for s in skills if s in jd_skills}
        res_cat  = {s for s in skills if s in resume_skills}
        if not jd_cat:
            continue
        pct = int(len(jd_cat & res_cat) / len(jd_cat) * 100)
        scores[cat] = pct
    return scores


def analyze_match(resume_text: str, jd_text: str) -> dict:
    """
    Returns a dict with:
      score            – overall match % (0-100)
      matched_skills   – list of skills in both resume & JD
      missing_skills   – list of skills in JD but not resume
      category_scores  – per-category breakdown
    """
    resume_skills = _extract_skills(resume_text)
    jd_skills     = _extract_skills(jd_text)

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    # Skill-overlap score
    skill_score = int(len(matched) / max(len(jd_skills), 1) * 100)

    # TF-IDF cosine similarity (holistic text similarity)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vec.fit_transform([resume_text, jd_text])
        cos_sim = int(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)
    except Exception:
        cos_sim = 0

    # Blend: 60% skill overlap + 40% text similarity
    overall = int(skill_score * 0.6 + cos_sim * 0.4)
    overall = max(0, min(overall, 100))

    cat_scores = _category_scores(resume_skills, jd_skills)

    return {
        "score":           overall,
        "matched_skills":  sorted(matched),
        "missing_skills":  sorted(missing),
        "category_scores": cat_scores,
        "skill_score":     skill_score,
        "cos_sim":         cos_sim,
    }
