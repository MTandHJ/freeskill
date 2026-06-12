r"""freeskill command-line interface."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from .validator import SkillValidator

__all__ = ["FreeskillCLI"]


class FreeskillCLI:
    r"""Manage freeskill commands for validation and installation.

    Parameters
    ----------
    argv : Optional[Sequence[str]], optional
        Command arguments. When omitted, arguments are read from `sys.argv`.
    """

    def __init__(self, argv: Optional[Sequence[str]] = None) -> None:
        self.argv = argv

    @property
    def root(self) -> Path:
        r"""Return the current project root for project-scope installs."""

        return Path.cwd()

    def run(self) -> int:
        r"""Parse arguments and run the selected command."""

        parser = self.build_parser()
        namespace = parser.parse_args(self.argv)
        return namespace.func(namespace)

    def build_parser(self) -> argparse.ArgumentParser:
        r"""Build the command-line parser."""

        parser = argparse.ArgumentParser(description="Manage freeskill Agent Skills.")
        subparsers = parser.add_subparsers(dest="command", required=True)

        validate_parser = subparsers.add_parser("validate", help="Validate skills.")
        validate_parser.add_argument(
            "skills",
            nargs="*",
            help="Skill names under skills/ or paths to skill directories. Defaults to all skills.",
        )
        validate_parser.add_argument(
            "--skills-root",
            type=Path,
            default=SkillValidator.default_skills_root(),
            help="Directory containing freeskill skills.",
        )
        validate_parser.set_defaults(func=self.validate_command)

        install_parser = subparsers.add_parser("install", help="Install skills into a target tool.")
        install_parser.add_argument(
            "skill_names",
            nargs="*",
            help="Skill names under skills/ or paths to skill directories.",
        )
        install_parser.add_argument("--target", choices=["claude", "codex"], required=True)
        install_parser.add_argument("--scope", choices=["user", "project"], default="user")
        install_parser.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
        install_parser.add_argument(
            "--all",
            action="store_true",
            help="Install all non-template skills from the skills root.",
        )
        install_parser.add_argument(
            "--skills-root",
            type=Path,
            default=SkillValidator.default_skills_root(),
            help="Directory containing freeskill skills.",
        )
        install_parser.add_argument(
            "--target-dir",
            type=Path,
            help="Override target parent directory. The skill directory is installed under this path.",
        )
        install_parser.set_defaults(func=self.install_command)

        return parser

    def validate_command(self, namespace: argparse.Namespace) -> int:
        r"""Run `freeskill validate`."""

        return SkillValidator(skills_root=namespace.skills_root).validate_command(namespace.skills)

    def install_command(self, namespace: argparse.Namespace) -> int:
        r"""Install one or more skills into a target tool."""

        source_dirs = self.resolve_install_source_dirs(namespace)
        if not source_dirs:
            return 1

        validations = [
            SkillValidator(skill_dir=source_dir, skills_root=namespace.skills_root).validate()
            for source_dir in source_dirs
        ]
        for validation in validations:
            self.print_validation_result(validation)

        if any(validation.errors for validation in validations):
            print("Install aborted because validation failed.", file=sys.stderr)
            return 1

        target_parent = namespace.target_dir
        if target_parent is None:
            target_parent = self.default_target_parent(namespace.target, namespace.scope)

        results: List[Tuple[str, Path, Path]] = []
        failures = 0
        for source_dir in source_dirs:
            target_dir = target_parent.expanduser() / source_dir.name
            action = self.install_one(source_dir, target_dir, namespace.mode)
            results.append((action, source_dir, target_dir))
            if action == "failed":
                failures += 1

        if len(results) == 1 and results[0][0] != "failed":
            _, source_dir, target_dir = results[0]
            self.print_install_summary(source_dir, namespace.target, namespace.scope, namespace.mode, target_dir)
        else:
            self.print_batch_install_summary(results, namespace.target, namespace.scope, namespace.mode)

        return 1 if failures else 0

    def resolve_install_source_dirs(self, namespace: argparse.Namespace) -> List[Path]:
        r"""Resolve install arguments into source skill directories."""

        if namespace.all and namespace.skill_names:
            print("Install accepts either skill names or --all, not both.", file=sys.stderr)
            return []

        if namespace.all:
            validator = SkillValidator(skills_root=namespace.skills_root)
            return [path for path in validator.resolve_skill_paths([]) if not path.name.startswith("_")]

        if not namespace.skill_names:
            print("Install requires at least one skill name or --all.", file=sys.stderr)
            return []

        return [self.resolve_skill_dir(skill_name, namespace.skills_root) for skill_name in namespace.skill_names]

    def install_one(self, source_dir: Path, target_dir: Path, mode: str) -> str:
        r"""Install a single skill and return the action name."""

        try:
            should_install = self.ensure_available_target(target_dir, source_dir)
            if should_install:
                self.install(source_dir, target_dir, mode)
                return "installed"

            return "skipped"
        except OSError as exc:
            print(f"Install failed for {source_dir.name}: {exc}", file=sys.stderr)
            if mode == "symlink":
                print(
                    "Try again with --mode copy if the target does not support symlinks.",
                    file=sys.stderr,
                )
            return "failed"

    def default_target_parent(self, target: str, scope: str) -> Path:
        r"""Return the default target parent directory for a target and scope."""

        if target == "claude":
            if scope == "user":
                return Path.home() / ".claude" / "skills"
            return self.root / ".claude" / "skills"

        if target == "codex":
            if scope == "user":
                return Path.home() / ".codex" / "skills"
            return self.root / ".codex" / "skills"

        raise ValueError(f"unsupported target: {target}")

    def resolve_skill_dir(self, skill_name: str, skills_root: Path) -> Path:
        r"""Resolve a skill name or path to a source skill directory."""

        candidate = Path(skill_name)
        if candidate.exists():
            return candidate
        return skills_root / skill_name

    def print_validation_result(self, validation: SkillValidator) -> None:
        r"""Print validation errors and warnings for install."""

        if validation.skill_dir is None:
            label = "<unset>"
        else:
            try:
                label = validation.skill_dir.resolve().relative_to(self.root)
            except ValueError:
                label = validation.skill_dir

        for message in validation.errors:
            print(f"ERROR {label}: {message}", file=sys.stderr)
        for message in validation.warnings:
            print(f"WARNING {label}: {message}", file=sys.stderr)

    def ensure_available_target(self, target_dir: Path, source_dir: Path) -> bool:
        r"""Return whether target_dir can be installed into."""

        if not target_dir.exists() and not target_dir.is_symlink():
            return True

        if target_dir.is_symlink():
            try:
                if target_dir.resolve() == source_dir.resolve():
                    print(f"Already installed: {target_dir} -> {source_dir}")
                    return False
            except FileNotFoundError:
                pass

        raise FileExistsError(
            f"target already exists and will not be overwritten without an explicit future option: {target_dir}"
        )

    def install(self, source_dir: Path, target_dir: Path, mode: str) -> None:
        r"""Install a skill by symlink or copy."""

        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if mode == "symlink":
            target_dir.symlink_to(source_dir.resolve(), target_is_directory=True)
        else:
            shutil.copytree(source_dir, target_dir)

    def print_install_summary(self, source_dir: Path, target: str, scope: str, mode: str, target_dir: Path) -> None:
        r"""Print installation details and manual verification guidance."""

        print("\nInstall summary")
        print(f"  skill:  {source_dir}")
        print(f"  target: {target}")
        print(f"  scope:  {scope}")
        print(f"  mode:   {mode}")
        print(f"  path:   {target_dir}")

        print("\nManual verification")
        print("  Ask the target tool to describe when this skill should be used.")
        print("  Installation only confirms file-level placement, not immediate tool recognition.")

    def print_batch_install_summary(
        self, results: Sequence[Tuple[str, Path, Path]], target: str, scope: str, mode: str
    ) -> None:
        r"""Print batch installation details and manual verification guidance."""

        installed = sum(1 for action, _, _ in results if action == "installed")
        skipped = sum(1 for action, _, _ in results if action == "skipped")
        failed = sum(1 for action, _, _ in results if action == "failed")

        print("\nInstall summary")
        print(f"  target:    {target}")
        print(f"  scope:     {scope}")
        print(f"  mode:      {mode}")
        print(f"  installed: {installed}")
        print(f"  skipped:   {skipped}")
        print(f"  failed:    {failed}")

        for action, source_dir, target_dir in results:
            print(f"  {action}: {source_dir.name} -> {target_dir}")

        print("\nManual verification")
        print("  Ask the target tool to describe when an installed skill should be used.")
        print("  Installation only confirms file-level placement, not immediate tool recognition.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    r"""Run the freeskill CLI."""

    return FreeskillCLI(argv).run()


if __name__ == "__main__":
    raise SystemExit(main())
