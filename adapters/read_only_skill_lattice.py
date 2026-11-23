"""Read-only discovery adapter for the Conzetian Skill Lattice.

This module indexes Markdown skill descriptions only. It never imports, evaluates,
executes, or installs skill content.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from pathlib import Path, PurePosixPath

from scripts.validate_skill_frontmatter import validate_skill_text


_FIELD_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$")


@dataclass(frozen=True)
class SkillDescriptor:
    name: str
    description: str
    relative_path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class SkillIssue:
    relative_path: str
    reason: str


@dataclass(frozen=True)
class SkillIndex:
    skills: tuple[SkillDescriptor, ...]
    invalid: tuple[SkillIssue, ...]


def _frontmatter_fields(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = _FIELD_RE.match(line)
        if match:
            key, value = match.groups()
            fields[key] = value.strip().strip('"').strip("'")
    return fields


def _resolve_skill(root: Path, relative_path: str) -> Path:
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or not rel.parts or any(
        part in ("", ".", "..") for part in rel.parts
    ):
        raise ValueError("skill path must be a confined relative path")
    if rel.name != "SKILL.md":
        raise ValueError("only SKILL.md files may be read")

    candidate = root.joinpath(*rel.parts)
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("symlinked skill paths are not allowed")

    resolved = candidate.resolve(strict=True)
    if resolved != root and root not in resolved.parents:
        raise ValueError("skill path escaped the lattice root")
    if not resolved.is_file():
        raise ValueError("skill path is not a regular file")
    return resolved


def list_skills(root: Path, *, strict: bool = False) -> SkillIndex:
    """Index valid skills while retaining diagnostics for invalid entries.

    With strict=True, any invalid entry raises ValueError. The default returns
    all valid descriptors plus a separate invalid-entry list.
    """
    root = Path(root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("lattice root must be a directory")

    records: list[SkillDescriptor] = []
    issues: list[SkillIssue] = []
    seen_names: dict[str, str] = {}

    for candidate in sorted(root.rglob("SKILL.md"), key=lambda path: path.as_posix()):
        relative = candidate.relative_to(root).as_posix()
        try:
            path = _resolve_skill(root, relative)
            raw = path.read_bytes()
            text = raw.decode("utf-8")
            errors = validate_skill_text(text, relative)
            if errors:
                raise ValueError("; ".join(errors))

            fields = _frontmatter_fields(text)
            name = fields.get("name", "").strip()
            description = fields.get("description", "").strip()
            if not name or not description:
                raise ValueError("frontmatter must include non-empty name and description")
            if name in seen_names:
                raise ValueError(
                    f"duplicate skill name {name!r}; first seen at {seen_names[name]}"
                )
            seen_names[name] = relative
            records.append(
                SkillDescriptor(
                    name=name,
                    description=description,
                    relative_path=relative,
                    sha256=hashlib.sha256(raw).hexdigest(),
                    size_bytes=len(raw),
                )
            )
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            issues.append(SkillIssue(relative, str(exc)))

    skills = tuple(sorted(records, key=lambda item: (item.name, item.relative_path)))
    invalid = tuple(sorted(issues, key=lambda item: item.relative_path))
    if strict and invalid:
        summary = "; ".join(
            f"{item.relative_path}: {item.reason}" for item in invalid
        )
        raise ValueError(f"invalid skill entries: {summary}")
    return SkillIndex(skills=skills, invalid=invalid)


def read_skill(root: Path, descriptor: SkillDescriptor) -> str:
    """Read a previously indexed skill only if its content hash is unchanged."""
    root = Path(root).expanduser().resolve(strict=True)
    path = _resolve_skill(root, descriptor.relative_path)
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != descriptor.sha256:
        raise ValueError("skill content changed after discovery; refresh the index")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("skill is not valid UTF-8") from exc
    errors = validate_skill_text(text, descriptor.relative_path)
    if errors:
        raise ValueError("; ".join(errors))
    fields = _frontmatter_fields(text)
    if fields.get("name") != descriptor.name:
        raise ValueError("skill identity changed after discovery")
    return text
