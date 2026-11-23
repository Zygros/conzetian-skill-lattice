# Read-only Skill Lattice Adapter

`adapters/read_only_skill_lattice.py` exposes a stable, dependency-free discovery contract for the Markdown skill lattice.

## Contract

- `list_skills(root)` returns a `SkillIndex` with valid descriptors sorted by skill name/path and a separate `invalid` diagnostics tuple. Invalid legacy entries do not discard valid descriptors. Use `strict=True` to reject any invalid entry.
- Each descriptor carries the frontmatter identity, description, relative `SKILL.md` path, SHA-256 digest, and byte length.
- `read_skill(root, descriptor)` returns the Markdown only if its path remains inside the lattice root, no path component is a symlink, the frontmatter remains valid, and the content hash still matches the descriptor.
- Duplicate skill names, malformed frontmatter, invalid UTF-8, path traversal, and symlinked skill files are recorded in `SkillIndex.invalid`; post-index content changes fail closed when read.
- The adapter never imports, evaluates, executes, installs, or transmits skill content. It performs local read-only filesystem operations only.

## Example

```python
from pathlib import Path
from adapters.read_only_skill_lattice import list_skills, read_skill

root = Path("skills")
index = list_skills(root)
for descriptor in index.skills:
    print(descriptor.name, descriptor.sha256)
    markdown = read_skill(root, descriptor)
for issue in index.invalid:
    print("SKIPPED", issue.relative_path, issue.reason)
```

The stable interface is intentionally limited to discovery and verified reading. Execution, permission grants, network access, and tool invocation are outside this adapter's authority.
