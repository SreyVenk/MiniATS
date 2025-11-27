# src/suggestions.py

from typing import Dict, List, Set, Optional


def generate_suggestions(
    missing_skills: Set[str],
    skill_to_category: Dict[str, str],
    job_title: Optional[str] = None,
) -> List[str]:
    """
    Turn missing skills into human-readable, actionable suggestions.

    - missing_skills: set of skill names (e.g., "python", "sql", "communication")
    - skill_to_category: mapping skill -> "hard" | "tools" | "soft"
    - job_title: optional job title string to personalize suggestions
    """
    suggestions: List[str] = []

    if not missing_skills:
        suggestions.append(
            "Your resume already covers most of the key skills in this job description. "
            "Focus on making your existing bullets more quantitative and impact-driven "
            "(metrics, scale, outcomes)."
        )
        return suggestions

    title_fragment = f"for this {job_title} role " if job_title else ""

    for skill in sorted(missing_skills):
        category = skill_to_category.get(skill, "hard")

        if category == "hard":
            suggestions.append(
                f"Add a concrete example of using **{skill}** in your Experience or Projects section "
                f"{title_fragment}—for example: _\"Used {skill} to analyze data, identify trends, and support decisions.\"_"
            )
        elif category == "tools":
            suggestions.append(
                f"Either list **{skill}** explicitly in your Skills section or add a bullet where you used it "
                f"in a real context (e.g., _\"Built dashboards using {skill} to track KPIs and report findings.\"_)."
            )
        elif category == "soft":
            suggestions.append(
                f"Demonstrate **{skill}** with a specific scenario rather than listing it alone—for example: "
                f"_\"Led a cross-functional team and used strong {skill} to align stakeholders and ship on time.\"_"
            )
        else:
            # Fallback if category is unknown
            suggestions.append(
                f"Consider mentioning **{skill}** somewhere in your Skills or Experience section if you truly have it, "
                f"and back it up with a concrete example."
            )

    # A final meta-suggestion so it doesn’t look purely mechanical
    suggestions.append(
        "Prioritize adding 2–4 of the most important missing skills, and update one or two bullets per experience "
        "to weave those skills in naturally instead of just dumping them in a list."
    )

    return suggestions
