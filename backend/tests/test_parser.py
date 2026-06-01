import pytest
from app.services.field_extractor import (
    extract_email,
    extract_phone,
    extract_name,
    detect_education_level,
    extract_education_history,
    extract_work_experience,
    compute_years_of_experience,
    extract_skills,
)


class TestExtractEmail:
    def test_basic_email(self):
        assert extract_email("Contact: john@example.com for info") == "john@example.com"

    def test_no_email(self):
        assert extract_email("No email here") is None

    def test_complex_email(self):
        assert extract_email("Email: zhang.san+work@company.co.uk") == "zhang.san+work@company.co.uk"


class TestExtractPhone:
    def test_chinese_mobile(self):
        assert extract_phone("电话: 13812345678") == "13812345678"

    def test_no_phone(self):
        assert extract_phone("No phone here") is None

    def test_us_format(self):
        result = extract_phone("Phone: +1-650-555-1234")
        assert result is not None


class TestExtractName:
    def test_name_first_line(self):
        text = "张三\nzhangsan@email.com\n13800138000"
        assert extract_name(text) == "张三"

    def test_english_name(self):
        text = "John Smith\njohn@email.com\nExperience"
        assert extract_name(text) == "John Smith"

    def test_skips_email_line(self):
        text = "john@example.com\n张三\n工作经历"
        assert extract_name(text) == "张三"


class TestDetectEducationLevel:
    def test_bachelor(self):
        assert detect_education_level("本科毕业于北京大学") == "bachelor"

    def test_master(self):
        assert detect_education_level("清华大学 硕士学位") == "master"

    def test_phd(self):
        assert detect_education_level("PhD in Computer Science") == "phd"

    def test_none(self):
        assert detect_education_level("工作三年经验") is None


class TestExtractEducationHistory:
    def test_basic_education_section(self):
        text = """张三
Education
2015-2019 北京大学 Bachelor 计算机科学
2019-2022 清华大学 Master 软件工程
Skills
Python, Java"""
        entries = extract_education_history(text)
        assert len(entries) >= 1

    def test_no_education_section_with_keyword(self):
        text = "张三\n本科毕业\nPython开发"
        entries = extract_education_history(text)
        assert len(entries) >= 1
        assert entries[0]["degree"] == "bachelor"


class TestExtractWorkExperience:
    def test_date_range_detection(self):
        text = """Work Experience
2019.01-2022.06 腾讯科技 高级工程师
负责后端系统设计
2017.07-2018.12 百度 工程师
搜索引擎开发"""
        entries = extract_work_experience(text)
        assert len(entries) == 2
        assert entries[0]["company"] != ""

    def test_present_date(self):
        text = """工作经历
2020.03-至今 阿里巴巴 架构师
微服务架构"""
        entries = extract_work_experience(text)
        assert len(entries) == 1
        assert entries[0]["end"] == "present"


class TestComputeYears:
    def test_single_job(self):
        work = [{"start": "2020.1", "end": "2023.1"}]
        years = compute_years_of_experience(work)
        assert years == 3.0

    def test_multiple_jobs(self):
        work = [
            {"start": "2018.1", "end": "2020.1"},
            {"start": "2020.6", "end": "2023.6"},
        ]
        years = compute_years_of_experience(work)
        assert years == 5.0

    def test_current_job(self):
        work = [{"start": "2023.1", "end": "present"}]
        years = compute_years_of_experience(work)
        assert years > 0

    def test_empty(self):
        assert compute_years_of_experience([]) == 0.0


class TestExtractSkills:
    def test_comma_separated(self):
        text = """技能
Python, JavaScript, Docker, Kubernetes
Vue.js, React, TypeScript"""
        skills = extract_skills(text)
        assert len(skills) >= 4
        assert "Python" in skills

    def test_no_skills_section(self):
        text = "张三\n工作三年"
        skills = extract_skills(text)
        assert skills == []
