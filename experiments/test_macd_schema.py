import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent
HARNESS = ROOT / "paired_baseline_harness.py"
SCHEMA_PATH = ROOT / "macd-paired-run.schema.json"


class MacdSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)

    def test_schema_is_valid_and_rejects_wrong_version(self):
        self.assertTrue(self.validator.is_valid({
            "schema_version": "macd-paired-run/v1",
            "record_type": "experiment_summary",
            "created_unix": 1,
            "task_file": "tasks.jsonl",
            "task_file_sha256": "a" * 64,
            "task_count": 1,
            "baseline_command": "baseline",
            "monitored_command": "monitored",
            "seed": 420,
            "timeout_seconds": 2,
            "totals": {
                "baseline_correct": 1, "monitored_correct": 1,
                "pairs_complete": 1, "baseline_errors": 0, "monitored_errors": 0
            },
            "baseline_accuracy": 1.0,
            "monitored_accuracy": 1.0,
            "accuracy_delta_monitored_minus_baseline": 0.0,
            "interpretation_boundary": "Supplied cases only."
        }))
        invalid = {
            "schema_version": "macd-paired-run/v999",
            "record_type": "experiment_summary"
        }
        self.assertFalse(self.validator.is_valid(invalid))

    def test_harness_receipts_validate_against_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tasks = root / "tasks.jsonl"
            output = root / "receipts.jsonl"
            adapter = root / "adapter.py"
            tasks.write_text(
                json.dumps({"task_id": "case-1", "input": {"x": 1}, "expected": 2}) + "\n",
                encoding="utf-8"
            )
            adapter.write_text(
                "import json,sys\n"
                "task=json.loads(sys.stdin.readline())\n"
                "print(json.dumps({'answer':task['input']['x']+1,'metadata':{'test':'ok'}}))\n",
                encoding="utf-8"
            )
            command = f"{sys.executable} {adapter}"
            run = subprocess.run([
                sys.executable, str(HARNESS), "--tasks", str(tasks),
                "--baseline", command, "--monitored", command,
                "--out", str(output), "--seed", "420"
            ], capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stderr)
            records = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 2)
            for record in records:
                self.assertTrue(self.validator.is_valid(record), list(self.validator.iter_errors(record)))
            self.assertEqual(records[-1]["record_type"], "experiment_summary")


if __name__ == "__main__":
    unittest.main()
