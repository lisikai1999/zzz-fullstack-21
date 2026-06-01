from app.services.skill_normalizer import SkillNormalizer
from app.services.field_extractor import EDUCATION_ORDER

_normalizer = SkillNormalizer()

WEIGHT_SKILL = 0.50
WEIGHT_EXPERIENCE = 0.25
WEIGHT_EDUCATION = 0.15
WEIGHT_INDUSTRY = 0.10


def check_hard_requirements(candidate: dict, job: dict) -> tuple[bool, list[str]]:
    failures = []

    min_edu = job.get("min_education")
    if min_edu:
        candidate_edu = candidate.get("education_level") or "high_school"
        if EDUCATION_ORDER.get(candidate_edu, 0) < EDUCATION_ORDER.get(min_edu, 0):
            failures.append(f"学历不满足: 要求{min_edu}, 实际{candidate_edu}")

    min_years = job.get("min_years")
    if min_years is not None and min_years > 0:
        candidate_years = candidate.get("years_of_experience") or 0
        if candidate_years < min_years:
            failures.append(f"年限不满足: 要求{min_years}年, 实际{candidate_years}年")

    required_skills = job.get("required_skills", [])
    candidate_skills = candidate.get("skills", [])
    for req_skill in required_skills:
        matched = any(
            _normalizer.skills_match(cs, req_skill) for cs in candidate_skills
        )
        if not matched:
            failures.append(f"缺少必备技能: {req_skill}")

    return (len(failures) == 0, failures)


def compute_skill_score(candidate_skills: list[str], weighted_skills: list[dict]) -> tuple[float, list[str], list[str]]:
    if not weighted_skills:
        return 100.0, [], []

    total_weight = sum(ws.get("weight", 5) for ws in weighted_skills)
    if total_weight == 0:
        return 100.0, [], []

    earned_weight = 0.0
    matched = []
    missing = []

    for ws in weighted_skills:
        skill = ws.get("skill", "")
        weight = ws.get("weight", 5)
        hit = any(_normalizer.skills_match(cs, skill) for cs in candidate_skills)
        if hit:
            earned_weight += weight
            matched.append(skill)
        else:
            missing.append(skill)

    score = (earned_weight / total_weight) * 100
    return round(score, 1), matched, missing


def compute_experience_score(candidate_years: float, min_years: float | None) -> float:
    if min_years is None or min_years == 0:
        if candidate_years >= 5:
            return 90.0
        elif candidate_years >= 2:
            return 70.0
        return 50.0

    base = 60.0
    extra = candidate_years - min_years
    bonus_cap = 5.0
    bonus = min(extra / bonus_cap, 1.0) * 40
    return min(round(base + bonus, 1), 100.0)


def compute_education_score(candidate_edu: str | None, min_edu: str | None) -> float:
    edu_scores = {"high_school": 25, "bachelor": 50, "master": 75, "phd": 100}
    candidate_val = edu_scores.get(candidate_edu or "high_school", 25)
    min_val = edu_scores.get(min_edu or "high_school", 25)

    if candidate_val > min_val:
        return min(70.0 + (candidate_val - min_val) / 100.0 * 30.0, 100.0)
    elif candidate_val == min_val:
        return 70.0
    return 50.0


def compute_industry_score(work_experience: list[dict], preferred_industry: str | None) -> float:
    if not preferred_industry:
        return 100.0

    industry_lower = preferred_industry.lower()
    for exp in work_experience:
        text = (exp.get("company", "") + " " + exp.get("description", "") + " " + exp.get("title", "")).lower()
        if industry_lower in text:
            return 100.0
    return 30.0


def compute_match_score(candidate: dict, job: dict) -> dict:
    passes, failures = check_hard_requirements(candidate, job)

    if not passes:
        return {
            "total_score": 0.0,
            "skill_score": 0.0,
            "experience_score": 0.0,
            "education_score": 0.0,
            "industry_score": 0.0,
            "matched_skills": [],
            "missing_skills": [f.split(": ")[-1] for f in failures if "技能" in f],
            "passes_hard_requirements": False,
            "hard_requirement_failures": failures,
        }

    candidate_skills = candidate.get("skills", [])
    weighted_skills = job.get("weighted_skills", [])
    skill_score, matched, missing = compute_skill_score(candidate_skills, weighted_skills)

    exp_score = compute_experience_score(
        candidate.get("years_of_experience") or 0,
        job.get("min_years"),
    )

    edu_score = compute_education_score(
        candidate.get("education_level"),
        job.get("min_education"),
    )

    industry_score = compute_industry_score(
        candidate.get("work_experience", []),
        job.get("preferred_industry"),
    )

    total = (
        skill_score * WEIGHT_SKILL
        + exp_score * WEIGHT_EXPERIENCE
        + edu_score * WEIGHT_EDUCATION
        + industry_score * WEIGHT_INDUSTRY
    )

    return {
        "total_score": round(total, 1),
        "skill_score": skill_score,
        "experience_score": exp_score,
        "education_score": edu_score,
        "industry_score": industry_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "passes_hard_requirements": True,
        "hard_requirement_failures": [],
    }
