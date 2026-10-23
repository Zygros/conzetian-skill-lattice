import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from receipt_chain import build_chain, verify_chain

class ReceiptChainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "receipts.jsonl"
        self.chain = self.root / "receipts.chain.jsonl"
        self.manifest = self.root / "receipts.manifest.json"
        self.source.write_text('{"task_id":"a","score":1}\n{"task_id":"b","score":0}\n', encoding="utf-8")
    def tearDown(self):
        self.temp.cleanup()
    def test_build_and_verify(self):
        manifest = build_chain(self.source, self.chain, self.manifest)
        self.assertEqual(manifest["record_count"], 2)
        result = verify_chain(self.chain, self.manifest)
        self.assertTrue(result["verified"], result)
        self.assertEqual(result["records_checked"], 2)
    def test_payload_mutation_detected(self):
        build_chain(self.source, self.chain, self.manifest)
        rows = [json.loads(x) for x in self.chain.read_text().splitlines()]
        rows[0]["payload"]["score"] = 99
        self.chain.write_text("".join(json.dumps(r) + "\n" for r in rows))
        result = verify_chain(self.chain, self.manifest)
        self.assertFalse(result["verified"])
    def test_truncation_detected_by_manifest(self):
        build_chain(self.source, self.chain, self.manifest)
        rows = self.chain.read_text().splitlines()
        self.chain.write_text(rows[0] + "\n")
        result = verify_chain(self.chain, self.manifest)
        self.assertFalse(result["verified"])
        self.assertIn(result["reason"], {"record_count_mismatch", "chain_file_digest_mismatch"})
    def test_refuses_overwrite(self):
        build_chain(self.source, self.chain, self.manifest)
        with self.assertRaises(FileExistsError):
            build_chain(self.source, self.chain, self.manifest)

if __name__ == "__main__":
    unittest.main()
