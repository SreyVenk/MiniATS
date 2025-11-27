import os
import sqlite3
from functools import lru_cache
from typing import Dict, List, Set

from .text_cleaning import basic_clean

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "skills.db")


@lru_cache(maxsize=1)
def load_skills_from_db() -> Dict[str, List[str]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name, category FROM skills")
    rows = cur.fetchall()
    conn.close()

    skills_by_cat: Dict[str, List[str]] = {"hard": [], "soft": [], "tools": []}
    for name, category in rows:
        category = category.strip().lower()
        if category in skills_by_cat:
            skills_by_cat[category].append(name.strip().lower())
    return skills_by_cat


def _build_token_set(text: str) -> Set[str]:
    cleaned = basic_clean(text)
    tokens = cleaned.split()
    token_set: Set[str] = set(tokens)
    for t in tokens:
        if t.endswith("s") and len(t) > 3:
            token_set.add(t[:-1])
    return token_set


def _find_matches(candidates: List[str], cleaned_text: str, token_set: Set[str]) -> Set[str]:
    hits: Set[str] = set()
    span = " " + cleaned_text + " "
    for skill in candidates:
        sc = basic_clean(skill)
        if not sc:
            continue
        if " " in sc:
            if sc in span:
                hits.add(skill)
        else:
            if sc in token_set:
                hits.add(skill)
    return hits


def extract_skill_matches(text: str) -> Dict[str, Set[str]]:
    if not text:
        return {"hard": set(), "tools": set(), "soft": set()}

    skills_by_cat = load_skills_from_db()
    cleaned = basic_clean(text)
    token_set = _build_token_set(text)

    hard_hits = _find_matches(skills_by_cat.get("hard", []), cleaned, token_set)
    tool_hits = _find_matches(skills_by_cat.get("tools", []), cleaned, token_set)
    soft_hits = _find_matches(skills_by_cat.get("soft", []), cleaned, token_set)

    return {
        "hard": hard_hits,
        "tools": tool_hits,
        "soft": soft_hits,
    }


def union_skills(skill_dict: Dict[str, Set[str]]) -> Set[str]:
    all_skills: Set[str] = set()
    for s in skill_dict.values():
        all_skills |= s
    return all_skills
