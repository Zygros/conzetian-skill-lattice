# Official Agent Skills Specification (Captured from agentskills.io)

Source: https://github.com/agentskills/agentskills (and agentskills.io)
Captured under Total Sovereignty of Justin Neal Thomas Conzet — 2026-08-20

## Directory structure

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

## SKILL.md format

YAML frontmatter + Markdown body.

### Required Frontmatter

- **name**: 1-64 chars, lowercase a-z 0-9 hyphens only, no leading/trailing/consecutive hyphens, must match directory name.
- **description**: 1-1024 chars. Must describe both *what* the skill does and *when* to use it. This is the primary trigger mechanism.

### Optional Frontmatter

- license
- compatibility (max 500 chars)
- metadata (key-value map)
- allowed-tools (experimental, space-separated)

### Progressive Disclosure

1. **Discovery** (~100 tokens): name + description only, always loaded.
2. **Activation** (<5000 tokens recommended): full SKILL.md body when matched.
3. **Execution**: scripts/ references/ assets/ loaded on demand.

Keep main SKILL.md under 500 lines. Move detail to references/.

## Body

No rigid structure required. Recommended: Overview, When to Use, Steps/Process, Examples, Edge cases.

This format is the open standard used across Claude Code, Cursor, Codex, and many other agents.
