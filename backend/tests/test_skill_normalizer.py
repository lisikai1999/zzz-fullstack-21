import pytest


class TestNormalize:
    def test_js_to_javascript(self, normalizer):
        assert normalizer.normalize("JS") == "JavaScript"

    def test_k8s_to_kubernetes(self, normalizer):
        assert normalizer.normalize("k8s") == "Kubernetes"

    def test_case_insensitive(self, normalizer):
        assert normalizer.normalize("python") == "Python"
        assert normalizer.normalize("PYTHON") == "Python"

    def test_unknown_passes_through(self, normalizer):
        assert normalizer.normalize("SomeRandomSkill") == "SomeRandomSkill"

    def test_vue_aliases(self, normalizer):
        assert normalizer.normalize("Vue") == "Vue.js"
        assert normalizer.normalize("vue3") == "Vue.js"
        assert normalizer.normalize("VueJS") == "Vue.js"


class TestNormalizeList:
    def test_deduplicates(self, normalizer):
        result = normalizer.normalize_list(["JS", "JavaScript", "javascript"])
        assert result == ["JavaScript"]

    def test_preserves_order(self, normalizer):
        result = normalizer.normalize_list(["Python", "Docker", "Vue"])
        assert result == ["Python", "Docker", "Vue.js"]


class TestHierarchy:
    def test_vue_is_frontend(self, normalizer):
        parents = normalizer.get_parent_categories("Vue.js")
        assert "frontend" in parents

    def test_python_is_backend(self, normalizer):
        parents = normalizer.get_parent_categories("Python")
        assert "backend" in parents

    def test_docker_is_devops(self, normalizer):
        parents = normalizer.get_parent_categories("Docker")
        assert "devops" in parents

    def test_unknown_no_parents(self, normalizer):
        parents = normalizer.get_parent_categories("UnknownSkill")
        assert parents == set()


class TestSkillsMatch:
    def test_direct_match(self, normalizer):
        assert normalizer.skills_match("Python", "Python") is True

    def test_synonym_match(self, normalizer):
        assert normalizer.skills_match("JS", "JavaScript") is True

    def test_hierarchy_match(self, normalizer):
        assert normalizer.skills_match("Vue.js", "frontend") is True

    def test_no_match(self, normalizer):
        assert normalizer.skills_match("Python", "JavaScript") is False

    def test_reverse_hierarchy_no_match(self, normalizer):
        assert normalizer.skills_match("frontend", "Vue.js") is False
