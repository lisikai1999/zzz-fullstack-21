from pathlib import Path

import yaml

from app.config import DATA_DIR


class SkillNormalizer:
    def __init__(self, synonyms_path: Path | None = None, hierarchy_path: Path | None = None):
        synonyms_path = synonyms_path or (DATA_DIR / "skill_synonyms.yaml")
        hierarchy_path = hierarchy_path or (DATA_DIR / "skill_hierarchy.yaml")

        self._synonym_map: dict[str, str] = {}
        self._child_to_parents: dict[str, set[str]] = {}

        self._load_synonyms(synonyms_path)
        self._load_hierarchy(hierarchy_path)

    def _load_synonyms(self, path: Path):
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or []
        for group in data:
            canonical = group["canonical"]
            self._synonym_map[canonical.lower()] = canonical
            for alias in group.get("aliases", []):
                self._synonym_map[alias.lower()] = canonical

    def _load_hierarchy(self, path: Path):
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        for parent, children in data.items():
            for child in children:
                canonical_child = self.normalize(child)
                self._child_to_parents.setdefault(canonical_child.lower(), set()).add(parent.lower())

    def normalize(self, raw_skill: str) -> str:
        key = raw_skill.strip().lower()
        return self._synonym_map.get(key, raw_skill.strip())

    def normalize_list(self, raw_skills: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for s in raw_skills:
            canonical = self.normalize(s)
            if canonical.lower() not in seen:
                seen.add(canonical.lower())
                result.append(canonical)
        return result

    def get_parent_categories(self, skill: str) -> set[str]:
        canonical = self.normalize(skill)
        return self._child_to_parents.get(canonical.lower(), set())

    def skills_match(self, candidate_skill: str, required_skill: str) -> bool:
        c = self.normalize(candidate_skill).lower()
        r = self.normalize(required_skill).lower()
        if c == r:
            return True
        parents = self._child_to_parents.get(c, set())
        return r in parents
