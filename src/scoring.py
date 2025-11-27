from typing import Dict, Set, Tuple


def compute_category_scores(
    jd_skills: Dict[str, Set[str]],
    resume_skills: Dict[str, Set[str]],
) -> Dict[str, float]:
    """
    Compute match ratio per category (hard, soft, tools).
    Returns values between 0 and 1.
    """
    scores = {}
    for cat in ["hard", "soft", "tools"]:
        jd_cat = jd_skills.get(cat, set())
        resume_cat = resume_skills.get(cat, set())
        if not jd_cat:
            scores[cat] = 0.0
            continue
        matched = jd_cat & resume_cat
        scores[cat] = len(matched) / len(jd_cat)
    return scores


def overall_fit_score(cat_scores: Dict[str, float]) -> float:
    """
    Weighted overall score from category scores.
    Hard skills matter the most, then tools, then soft.
    """
    hard = cat_scores.get("hard", 0.0)
    soft = cat_scores.get("soft", 0.0)
    tools = cat_scores.get("tools", 0.0)

    score = (
        0.6 * hard +
        0.2 * tools +
        0.2 * soft
    )
    return round(score * 100, 1)  # percentage


def score_label(score: float) -> str:
    if score >= 80:
        return "Strong fit"
    elif score >= 60:
        return "Moderate fit"
    elif score >= 40:
        return "Weak fit"
    else:
        return "Poor fit"


def compute_overlap_sets(
    jd_skills: Dict[str, Set[str]],
    resume_skills: Dict[str, Set[str]],
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Return (matched, missing, extra) sets across all categories combined.
    """
    jd_all = set().union(*jd_skills.values()) if jd_skills else set()
    resume_all = set().union(*resume_skills.values()) if resume_skills else set()

    matched = jd_all & resume_all
    missing = jd_all - resume_all
    extra = resume_all - jd_all
    return matched, missing, extra
