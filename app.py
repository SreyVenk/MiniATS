import os
import sys

import pandas as pd
import streamlit as st
from src.suggestions import generate_suggestions

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from src.parsers import extract_resume_text
from src.keyword_extractor import extract_skill_matches
from src.scoring import (
    compute_category_scores,
    overall_fit_score,
    score_label,
    compute_overlap_sets,
)

st.set_page_config(page_title="Mini ATS", page_icon="📄", layout="wide")

CUSTOM_CSS = """
<style>
main.block-container {
    padding-top: 1.25rem;
    padding-bottom: 1.25rem;
}

/* Overall fit / section headings */
.section-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-top: 0.35rem;
    margin-bottom: 0.4rem;
}

/* Score pill */
.score-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    font-size: 0.85rem;
}

/* Skill chips */
.skill-chip {
    display: inline-block;
    padding: 0.16rem 0.65rem;
    margin: 0.16rem;
    border-radius: 999px;
    font-size: 0.8rem;
    border: 1px solid rgba(148, 163, 184, 0.45);
    background: radial-gradient(circle at top left, #111827 0, #020617 55%);
    color: #e5e7eb;
    white-space: nowrap;
}

/* Suggestion cards */
.suggestion-card {
    border-radius: 0.9rem;
    padding: 0.7rem 0.9rem;
    margin-bottom: 0.45rem;
    background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,64,175,0.35));
    border: 1px solid rgba(129, 140, 248, 0.45);
    font-size: 0.9rem;
}

/* Mini metric cards for category breakdown */
.mini-card {
    border-radius: 0.8rem;
    padding: 0.55rem 0.75rem;
    background: radial-gradient(circle at top left, #020617, #020617 40%, #0b1120 100%);
    border: 1px solid rgba(51, 65, 85, 0.9);
    margin-bottom: 0.4rem;
}
.mini-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9ca3af;
}
.mini-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #e5e7eb;
}

/* Soft divider */
.soft-divider {
    border-top: 1px solid rgba(55, 65, 81, 0.7);
    margin: 0.75rem 0 0.6rem 0;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_skill_chips(skills):
    if not skills:
        st.markdown("_None_")
        return
    chips_html = "".join(
        f'<span class="skill-chip">{s}</span>' for s in sorted(skills)
    )
    st.markdown(chips_html, unsafe_allow_html=True)


def main():
    st.markdown("### 📄 Mini ATS")
    st.markdown(
        "Quickly see how well your resume lines up with a specific job description."
    )

    with st.sidebar:
        st.markdown("#### Inputs")
        resume_file = st.file_uploader(
            "Resume (PDF or DOCX)", type=["pdf", "docx"]
        )
        jd_text = st.text_area(
            "Job description",
            height=260,
            placeholder="Paste the full job description here...",
        )
        st.markdown("---")
        job_title_input = st.text_input(
            "Job title (optional)",
            placeholder="e.g., Data Analyst, Application Analyst",
        )
        analyze_clicked = st.button("Run analysis", type="primary", use_container_width=True)

    if not analyze_clicked:
        st.info("Upload a resume and paste a job description in the sidebar, then click **Run analysis**.")
        return

    if resume_file is None:
        st.error("Please upload a resume file.")
        return
    if not jd_text.strip():
        st.error("Please paste a job description.")
        return

    with st.spinner("Analyzing resume vs job description..."):
        resume_text = extract_resume_text(resume_file)
        if resume_text is None:
            st.error("Unsupported resume format. Use PDF or DOCX.")
            return

        jd_skills = extract_skill_matches(jd_text)
        resume_skills = extract_skill_matches(resume_text)

        cat_scores = compute_category_scores(jd_skills, resume_skills)
        overall = overall_fit_score(cat_scores)
        label = score_label(overall)
        matched, missing, extra = compute_overlap_sets(jd_skills, resume_skills)

        skill_to_category = {}
        for cat, skills in jd_skills.items():
            for s in skills:
                skill_to_category[s] = cat

        if job_title_input.strip():
            job_title = job_title_input.strip()
        else:
            first_line = jd_text.strip().splitlines()[0] if jd_text.strip() else ""
            job_title = first_line[:80] if first_line else None

        suggestions = generate_suggestions(
            missing_skills=missing,
            skill_to_category=skill_to_category,
            job_title=job_title,
        )

    st.markdown("---")

    top_col1, top_col2 = st.columns([1, 2])

    with top_col1:
        st.markdown('<div class="section-title">Overall fit</div>', unsafe_allow_html=True)
        st.metric("Fit score", f"{overall}%", label)
        st.progress(min(max(overall / 100.0, 0.0), 1.0))
        st.markdown(
            f'<span class="score-pill"> Match level: <strong>{label}</strong></span>',
            unsafe_allow_html=True,
        )

    with top_col2:
        st.markdown('<div class="section-title">Category breakdown</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)

        cat_map = [
            ("Hard", "hard"),
            ("Tools", "tools"),
            ("Soft", "soft"),
        ]

        for col, (label_text, key) in zip([c1, c2, c3], cat_map):
            pct = round(cat_scores.get(key, 0.0) * 100, 1)
            with col:
                st.markdown(
                    f'''
                    <div class="mini-card">
                        <div class="mini-title">{label_text}</div>
                        <div class="mini-value">{pct:.1f}%</div>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
                st.progress(min(max(pct / 100.0, 0.0), 1.0))

    tabs = st.tabs(["Skills", "Recommendations", "Details"])

    with tabs[0]:
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown('<div class="section-title">Matched skills</div>', unsafe_allow_html=True)
            render_skill_chips(matched)

        with col_b:
            st.markdown('<div class="section-title">Missing from JD</div>', unsafe_allow_html=True)
            render_skill_chips(missing)

        with col_c:
            st.markdown('<div class="section-title">Extra in resume</div>', unsafe_allow_html=True)
            render_skill_chips(extra)

    with tabs[1]:
        st.markdown('<div class="section-title">Top suggestions</div>', unsafe_allow_html=True)
        if not suggestions:
            st.write("No specific recommendations generated. Your resume already covers most key skills.")
        else:
            for s in suggestions[:8]:
                st.markdown(f'<div class="suggestion-card">• {s}</div>', unsafe_allow_html=True)

            if len(suggestions) > 8:
                with st.expander("Show all suggestions"):
                    for s in suggestions[8:]:
                        st.markdown(f'<div class="suggestion-card">• {s}</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="section-title">Raw skill extraction</div>', unsafe_allow_html=True)
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        jd_cols = st.columns(3)
        resume_cols = st.columns(3)
        jd_labels = ["Hard (JD)", "Tools (JD)", "Soft (JD)"]
        resume_labels = ["Hard (Resume)", "Tools (Resume)", "Soft (Resume)"]
        jd_keys = ["hard", "tools", "soft"]

        st.markdown("**From job description:**")
        for col, label_text, key in zip(jd_cols, jd_labels, jd_keys):
            with col:
                st.markdown(f'<div class="section-title">{label_text}</div>', unsafe_allow_html=True)
                render_skill_chips(jd_skills.get(key, set()))

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
        st.markdown("**From resume:**")
        for col, label_text, key in zip(resume_cols, resume_labels, jd_keys):
            with col:
                st.markdown(f'<div class="section-title">{label_text}</div>', unsafe_allow_html=True)
                render_skill_chips(resume_skills.get(key, set()))


if __name__ == "__main__":
    main()
