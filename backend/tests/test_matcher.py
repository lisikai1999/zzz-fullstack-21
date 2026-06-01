import pytest
from app.services.matcher import (
    check_hard_requirements,
    compute_skill_score,
    compute_experience_score,
    compute_education_score,
    compute_industry_score,
    compute_match_score,
)


class TestHardRequirements:
    def test_education_fail(self):
        candidate = {"education_level": "high_school", "years_of_experience": 5, "skills": ["Python"]}
        job = {"min_education": "bachelor", "min_years": None, "required_skills": []}
        passes, failures = check_hard_requirements(candidate, job)
        assert not passes
        assert any("学历" in f for f in failures)

    def test_education_pass(self):
        candidate = {"education_level": "master", "years_of_experience": 5, "skills": ["Python"]}
        job = {"min_education": "bachelor", "min_years": None, "required_skills": []}
        passes, _ = check_hard_requirements(candidate, job)
        assert passes

    def test_years_fail(self):
        candidate = {"education_level": "bachelor", "years_of_experience": 1, "skills": []}
        job = {"min_education": None, "min_years": 3, "required_skills": []}
        passes, failures = check_hard_requirements(candidate, job)
        assert not passes
        assert any("年限" in f for f in failures)

    def test_years_pass(self):
        candidate = {"education_level": "bachelor", "years_of_experience": 5, "skills": []}
        job = {"min_education": None, "min_years": 3, "required_skills": []}
        passes, _ = check_hard_requirements(candidate, job)
        assert passes

    def test_required_skills_all_present(self):
        candidate = {"education_level": "bachelor", "years_of_experience": 3, "skills": ["Python", "Docker"]}
        job = {"min_education": None, "min_years": None, "required_skills": ["Python", "Docker"]}
        passes, _ = check_hard_requirements(candidate, job)
        assert passes

    def test_required_skills_missing_one(self):
        candidate = {"education_level": "bachelor", "years_of_experience": 3, "skills": ["Python"]}
        job = {"min_education": None, "min_years": None, "required_skills": ["Python", "Docker"]}
        passes, failures = check_hard_requirements(candidate, job)
        assert not passes
        assert any("Docker" in f for f in failures)

    def test_required_skills_synonym_match(self):
        candidate = {"education_level": "bachelor", "years_of_experience": 3, "skills": ["JavaScript"]}
        job = {"min_education": None, "min_years": None, "required_skills": ["JS"]}
        passes, _ = check_hard_requirements(candidate, job)
        assert passes


class TestSkillScore:
    def test_all_matched(self):
        score, matched, missing = compute_skill_score(
            ["Python", "Docker", "Kubernetes"],
            [{"skill": "Python", "weight": 8}, {"skill": "Docker", "weight": 6}],
        )
        assert score == 100.0
        assert "Python" in matched
        assert "Docker" in matched
        assert missing == []

    def test_none_matched(self):
        score, matched, missing = compute_skill_score(
            ["Java", "Spring"],
            [{"skill": "Python", "weight": 8}, {"skill": "Docker", "weight": 6}],
        )
        assert score == 0.0
        assert matched == []
        assert len(missing) == 2

    def test_partial_weighted(self):
        score, matched, missing = compute_skill_score(
            ["Python"],
            [{"skill": "Python", "weight": 8}, {"skill": "Docker", "weight": 2}],
        )
        assert score == 80.0
        assert "Python" in matched
        assert "Docker" in missing

    def test_empty_preferences(self):
        score, _, _ = compute_skill_score(["Python"], [])
        assert score == 100.0


class TestExperienceScore:
    def test_minimum_met(self):
        score = compute_experience_score(3.0, 3.0)
        assert score == 60.0

    def test_exceeds_bonus(self):
        score = compute_experience_score(8.0, 3.0)
        assert score == 100.0

    def test_slightly_above(self):
        score = compute_experience_score(4.0, 3.0)
        assert 60 < score < 100

    def test_no_minimum(self):
        score = compute_experience_score(5.0, None)
        assert score == 90.0


class TestEducationScore:
    def test_meets_minimum(self):
        score = compute_education_score("bachelor", "bachelor")
        assert score == 70.0

    def test_exceeds(self):
        score = compute_education_score("master", "bachelor")
        assert score > 70.0

    def test_below_minimum(self):
        score = compute_education_score("high_school", "bachelor")
        assert score == 50.0


class TestIndustryScore:
    def test_match(self):
        work = [{"company": "腾讯科技", "title": "工程师", "description": "互联网产品开发"}]
        score = compute_industry_score(work, "互联网")
        assert score == 100.0

    def test_no_match(self):
        work = [{"company": "中国银行", "title": "工程师", "description": "银行系统"}]
        score = compute_industry_score(work, "互联网")
        assert score == 30.0

    def test_no_preference(self):
        score = compute_industry_score([], None)
        assert score == 100.0


class TestTotalScore:
    def test_weighted_sum(self, sample_candidate, sample_job):
        result = compute_match_score(sample_candidate, sample_job)
        assert result["passes_hard_requirements"] is True
        assert 0 < result["total_score"] <= 100
        assert isinstance(result["matched_skills"], list)
        assert isinstance(result["missing_skills"], list)

    def test_fails_hard_returns_zero(self):
        candidate = {"education_level": "high_school", "years_of_experience": 1, "skills": []}
        job = {"min_education": "master", "min_years": 5, "required_skills": ["Python"], "weighted_skills": [], "preferred_industry": None}
        result = compute_match_score(candidate, job)
        assert result["total_score"] == 0.0
        assert result["passes_hard_requirements"] is False

    def test_deterministic(self, sample_candidate, sample_job):
        r1 = compute_match_score(sample_candidate, sample_job)
        r2 = compute_match_score(sample_candidate, sample_job)
        assert r1["total_score"] == r2["total_score"]

    def test_top_k_ordering(self, sample_job):
        candidates = [
            {"name": "A", "education_level": "master", "years_of_experience": 8, "skills": ["Python", "Docker", "Kubernetes", "PostgreSQL"], "work_experience": [{"company": "互联网公司", "title": "", "description": ""}]},
            {"name": "B", "education_level": "bachelor", "years_of_experience": 3, "skills": ["Python"], "work_experience": []},
            {"name": "C", "education_level": "bachelor", "years_of_experience": 4, "skills": ["Python", "Docker"], "work_experience": []},
        ]
        scores = [(c["name"], compute_match_score(c, sample_job)["total_score"]) for c in candidates]
        scores.sort(key=lambda x: x[1], reverse=True)
        assert scores[0][0] == "A"
