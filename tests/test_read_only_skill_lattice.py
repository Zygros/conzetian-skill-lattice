import hashlib
from pathlib import Path
import tempfile
import unittest

from adapters.read_only_skill_lattice import (
    SkillDescriptor,
    list_skills,
    read_skill,
)


def write_skill(root: Path, relative: str, name: str, body: str = "Read-only instructions.") -> Path:
    path = root / relative / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nname: {name}\ndescription: Description for {name}.\n---\n\n{body}\n",
        encoding="utf-8",
    )
    return path


class ReadOnlySkillLatticeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_index_is_sorted_and_hash_linked(self):
        write_skill(self.root, "skills/zeta", "zeta")
        alpha = write_skill(self.root, "skills/alpha", "alpha")
        records = list_skills(self.root)
        self.assertEqual([item.name for item in records], ["alpha", "zeta"])
        self.assertEqual(records[0].sha256, hashlib.sha256(alpha.read_bytes()).hexdigest())
        self.assertEqual(records[0].size_bytes, len(alpha.read_bytes()))

    def test_read_returns_markdown_without_executing_it(self):
        marker = self.root / "executed.txt"
        body = f'If executed, this would write: {marker}\n'
        path = write_skill(self.root, "skills/no-exec", "no-exec", body)
        descriptor = list_skills(self.root)[0]
        content = read_skill(self.root, descriptor)
        self.assertIn("If executed", content)
        self.assertFalse(marker.exists())
        self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_modified_skill_is_rejected_after_indexing(self):
        path = write_skill(self.root, "skills/change", "change")
        descriptor = list_skills(self.root)[0]
        path.write_text(path.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "content changed"):
            read_skill(self.root, descriptor)

    def test_path_traversal_is_rejected(self):
        descriptor = SkillDescriptor(
            name="escape",
            description="escape",
            relative_path="../outside/SKILL.md",
            sha256="0" * 64,
            size_bytes=1,
        )
        with self.assertRaisesRegex(ValueError, "confined relative path"):
            read_skill(self.root, descriptor)

    def test_symlinked_skill_is_rejected(self):
        outside = self.root.parent / "outside-skill"
        outside.mkdir(exist_ok=True)
        target = write_skill(outside, "outside", "outside")
        link_dir = self.root / "skills"
        link_dir.mkdir()
        link = link_dir / "linked"
        try:
            link.symlink_to(target.parent, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable on this platform")
        with self.assertRaises(ValueError):
            list_skills(self.root)

    def test_duplicate_names_are_rejected(self):
        write_skill(self.root, "skills/one", "duplicate")
        write_skill(self.root, "skills/two", "duplicate")
        with self.assertRaisesRegex(ValueError, "duplicate skill name"):
            list_skills(self.root)


if __name__ == "__main__":
    unittest.main()
