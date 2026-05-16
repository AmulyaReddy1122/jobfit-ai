"""
AI-powered insights using the Groq API (free).
Model: llama-3.3-70b-versatile
"""

from __future__ import annotations
import json
import re
import os
from groq import Groq

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
_MODEL  = "llama-3.3-70b-versatile"


def _ask(system: str, user: str, max_tokens: int = 1024) -> str:
    """Low-level wrapper — returns assistant text."""
    response = _client.chat.completions.create(
        model=_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
    )
    return response.choices[0].message.content.strip()


def _parse_json(raw: str) -> any:
    """Strip markdown fences and parse JSON safely."""
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(clean)


# ── Public functions ───────────────────────────────────────────────────────────

def extract_jd_insights(jd_text: str) -> dict:
    """
    Extract structured insights from a JD.
    Returns: { core_skills, experience, nice_to_have, role_title, salary_hint }
    """
    system = (
        "You are a senior recruiter. Analyse job descriptions and return ONLY valid JSON. "
        "No preamble, no markdown fences, no extra text."
    )
    user = f"""Analyse this job description and return a JSON object with these exact keys:
- core_skills: list of 5-8 must-have technical skills (strings)
- experience: string like "2-3 years", "Entry level", "5+ years"
- nice_to_have: list of 3-5 bonus skills (strings)
- role_title: cleaned job title (string)
- salary_hint: estimated salary range if inferable, else "Not specified"

JOB DESCRIPTION:
{jd_text[:3000]}
"""
    try:
        raw = _ask(system, user)
        return _parse_json(raw)
    except Exception:
        return {
            "core_skills":  [],
            "experience":   "Not specified",
            "nice_to_have": [],
            "role_title":   "Data Science Role",
            "salary_hint":  "Not specified",
        }


def generate_cover_letter_bullets(
    resume_text: str, jd_text: str, match_data: dict
) -> str:
    """
    Generate 5 punchy cover letter bullet points tailored to the JD.
    Returns a plain string with bullet points.
    """
    matched = ", ".join(match_data.get("matched_skills", [])[:10])
    system = (
        "You are an expert career coach who writes compelling cover letters. "
        "Be specific, quantify where possible, and avoid generic phrases."
    )
    user = f"""Write 5 powerful cover letter bullet points for this candidate.

CANDIDATE'S MATCHED SKILLS: {matched}

JOB DESCRIPTION (first 1500 chars):
{jd_text[:1500]}

RESUME EXCERPT (first 1500 chars):
{resume_text[:1500]}

Rules:
- Start each bullet with a strong action verb
- Tie each point to a specific JD requirement
- Include numbers/metrics where you can infer them
- Keep each bullet to 1-2 lines
- Format: • Bullet text here
"""
    try:
        return _ask(system, user, max_tokens=600)
    except Exception:
        return "• Unable to generate cover letter bullets. Please check your API key."


def generate_skill_roadmap(missing_skills: list[str], jd_insights: dict) -> list[dict]:
    """
    Generate a prioritised learning roadmap for missing skills.
    Returns: list of { skill, how, timeframe }
    """
    if not missing_skills:
        return [{"skill": "Portfolio Project", "how": "Build an end-to-end ML project and deploy it on Streamlit Cloud.", "timeframe": "2 weeks"}]

    system = (
        "You are a data science mentor. Return ONLY valid JSON — no preamble, no markdown."
    )
    skills_str = ", ".join(missing_skills[:8])
    user = f"""Create a learning roadmap for these missing skills: {skills_str}

Return a JSON array of up to 6 objects, each with:
- skill: the skill name (string)
- how: 1-2 sentence actionable learning tip with a free resource (string)
- timeframe: realistic time to learn e.g. "3 days", "1 week" (string)

Prioritise skills that appear most in data science job descriptions.
"""
    try:
        raw = _ask(system, user, max_tokens=800)
        return _parse_json(raw)
    except Exception:
        return [{"skill": s, "how": f"Search '{s} tutorial' on YouTube or Kaggle Learn.", "timeframe": "1 week"} for s in missing_skills[:5]]


def generate_overall_summary(match_data: dict, jd_insights: dict) -> str:
    """One-sentence recruiter-style summary of the candidate's fit."""
    score  = match_data["score"]
    matched_count = len(match_data.get("matched_skills", []))
    missing_count = len(match_data.get("missing_skills", []))
    role   = jd_insights.get("role_title", "this role")
    exp    = jd_insights.get("experience", "the required experience")

    system = "You are a recruiter writing a one-sentence candidate summary. Be direct and honest."
    user = f"""Write ONE sentence summarising this candidate's fit.
Score: {score}%  |  Matched skills: {matched_count}  |  Missing skills: {missing_count}
Role: {role}  |  Required experience: {exp}
"""
    try:
        return _ask(system, user, max_tokens=100)
    except Exception:
        return f"Candidate matches {score}% of the job requirements for {role}."
