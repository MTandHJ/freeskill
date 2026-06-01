r"""Validate freeskill Agent Skills directories."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

__all__ = ["SkillValidator"]


DESCRIPTION_MIN_LENGTH = 20
REFERENCE_PATTERN = re.compile(r"(?P<path>(?:scripts|references|assets)/[A-Za-z0-9._/\-]+)")
VALID_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


class SkillValidator:
    r"""Validate one or more Agent Skill directories.

    Parameters
    ----------
    skill_dir : Path, optional
        Skill directory for single-skill validation.
    skills_root : Path, optional
        Directory containing skill subdirectories for CLI validation.
    """

    def __init__(self, skill_dir: Optional[Path] = None, skills_root: Optional[Path] = None) -> None:
        self.skill_dir = skill_dir
        self.skills_root = skills_root or self.default_skills_root()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    @property
    def ok(self) -> bool:
        r"""Return whether the current validation has no errors."""

        return not self.errors

    @classmethod
    def source_checkout_root(cls) -> Path:
        r"""Return the source checkout root when running from this repository."""

        return Path(__file__).resolve().parents[2]

    @classmethod
    def default_skills_root(cls) -> Path:
        r"""Return the default skills root."""

        env_root = os.environ.get("FREESKILL_SKILLS_ROOT")
        if env_root:
            return Path(env_root).expanduser()

        cwd_skills = Path.cwd() / "skills"
        if cwd_skills.exists():
            return cwd_skills

        return cls.source_checkout_root() / "skills"

    @classmethod
    def parse_frontmatter(cls, text: str) -> Tuple[Dict[str, str], str, List[str]]:
        r"""Parse the simple YAML frontmatter needed by Agent Skills."""

        warnings: List[str] = []
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            raise ValueError("SKILL.md must start with YAML frontmatter")

        closing_index = None
        for index, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing_index = index
                break

        if closing_index is None:
            raise ValueError("YAML frontmatter is missing a closing --- line")

        metadata: Dict[str, str] = {}
        for line_number, line in enumerate(lines[1:closing_index], start=2):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if ":" not in stripped:
                warnings.append(f"frontmatter line {line_number} is not a key-value pair")
                continue
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            if key:
                metadata[key] = value

        body = "\n".join(lines[closing_index + 1 :])
        return metadata, body, warnings

    @classmethod
    def referenced_supporting_files(cls, text: str) -> List[str]:
        r"""Return supporting files referenced from SKILL.md."""

        paths = []
        for match in REFERENCE_PATTERN.finditer(text):
            path = match.group("path").rstrip(").,;:]")
            if path not in paths:
                paths.append(path)
        return paths

    def validate(self) -> "SkillValidator":
        r"""Validate `self.skill_dir` and return this validator."""

        self.errors.clear()
        self.warnings.clear()
        if self.skill_dir is None:
            self.errors.append("skill directory is not set")
            return self

        skill_md = self.skill_dir / "SKILL.md"
        if not self.skill_dir.exists():
            self.errors.append("skill directory does not exist")
            return self

        if not self.skill_dir.is_dir():
            self.errors.append("skill path is not a directory")
            return self

        if not skill_md.exists():
            self.errors.append("missing SKILL.md")
            return self

        try:
            text = skill_md.read_text(encoding="utf-8")
            metadata, body, frontmatter_warnings = self.parse_frontmatter(text)
        except UnicodeDecodeError:
            self.errors.append("SKILL.md must be UTF-8 text")
            return self
        except ValueError as exc:
            self.errors.append(str(exc))
            return self

        self.warnings.extend(frontmatter_warnings)
        self._validate_metadata(metadata)
        self._validate_supporting_files(body)
        return self

    def resolve_skill_paths(self, args: Sequence[str]) -> List[Path]:
        r"""Resolve CLI arguments into skill directories."""

        if not args:
            if not self.skills_root.exists():
                return []
            return sorted(path for path in self.skills_root.iterdir() if path.is_dir() and not path.name.startswith("."))

        paths = []
        for arg in args:
            candidate = Path(arg)
            if candidate.exists():
                paths.append(candidate)
            else:
                paths.append(self.skills_root / arg)
        return paths

    def validate_command(self, skill_args: Sequence[str]) -> int:
        r"""Validate skills from command arguments."""

        root = Path.cwd()
        validators = [
            SkillValidator(skill_dir=path, skills_root=self.skills_root).validate()
            for path in self.resolve_skill_paths(skill_args)
        ]

        if not validators:
            print(f"No skill directories found under {self.skills_root}", file=sys.stderr)
            return 1

        for validator in validators:
            validator.print_result(root)

        error_count = sum(len(validator.errors) for validator in validators)
        warning_count = sum(len(validator.warnings) for validator in validators)
        print(f"\nValidated {len(validators)} skill(s): {error_count} error(s), {warning_count} warning(s)")

        return 1 if error_count else 0

    def print_result(self, root: Path) -> None:
        r"""Print one validation result."""

        if self.skill_dir is None:
            label = "<unset>"
        else:
            try:
                label = self.skill_dir.resolve().relative_to(root)
            except ValueError:
                label = self.skill_dir

        status = "PASS" if self.ok else "FAIL"
        print(f"{status} {label}")

        for message in self.errors:
            print(f"  ERROR: {message}")
        for message in self.warnings:
            print(f"  WARNING: {message}")

    def _validate_metadata(self, metadata: Dict[str, str]) -> None:
        name = metadata.get("name", "").strip()
        description = metadata.get("description", "").strip()
        skill_name = self.skill_dir.name if self.skill_dir is not None else ""

        if not name:
            self.errors.append("frontmatter is missing required field: name")
        elif not VALID_NAME_PATTERN.match(name):
            self.errors.append(
                "frontmatter field 'name' must use lowercase letters, numbers, dots, underscores, or hyphens"
            )
        elif name != skill_name:
            self.warnings.append(f"frontmatter name '{name}' does not match directory name '{skill_name}'")

        if not description:
            self.errors.append("frontmatter is missing required field: description")
        elif len(description) < DESCRIPTION_MIN_LENGTH:
            self.warnings.append(f"description is short ({len(description)} chars); describe when to use this skill")

    def _validate_supporting_files(self, body: str) -> None:
        if self.skill_dir is None:
            return

        for referenced_path in self.referenced_supporting_files(body):
            target = self.skill_dir / referenced_path
            if not target.exists():
                self.errors.append(f"referenced supporting file does not exist: {referenced_path}")

    @classmethod
    def build_parser(cls) -> argparse.ArgumentParser:
        r"""Build the standalone validator parser."""

        parser = argparse.ArgumentParser(description="Validate freeskill Agent Skills directories.")
        parser.add_argument(
            "skills",
            nargs="*",
            help="Skill names under skills/ or paths to skill directories. Defaults to all skills.",
        )
        parser.add_argument(
            "--skills-root",
            type=Path,
            default=cls.default_skills_root(),
            help="Directory containing freeskill skills.",
        )
        return parser

    @classmethod
    def main(cls, argv: Optional[Sequence[str]] = None) -> int:
        r"""Run the validator."""

        parser = cls.build_parser()
        namespace = parser.parse_args(argv)
        return cls(skills_root=namespace.skills_root).validate_command(namespace.skills)


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Run the standalone validator."""

    return SkillValidator.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
