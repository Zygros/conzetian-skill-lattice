import tempfile
import unittest
from pathlib import Path
from gateway import Gateway, MockAdapter
from browser_adapter import BrowserAdapter

class GatewayTests(unittest.TestCase):
    def make_gateway(self, mode="confirm_writes", scopes=None, approval=None):
        self.tmp = tempfile.TemporaryDirectory()
        policy = {
            "mode": mode,
            "scopes": scopes or ["computer.describe", "computer.observe", "computer.click", "computer.scroll", "browser.navigate"],
            "targets": ["mock:test"],
            "approval_required_for": approval if approval is not None else ["navigate"],
            "max_actions_per_minute": 30,
            "session_seconds": 3600
        }
        return Gateway(policy, MockAdapter(), str(Path(self.tmp.name) / "audit.jsonl"))
    def tearDown(self):
        if hasattr(self, "tmp"): self.tmp.cleanup()
    def call(self, g, action, args=None, **extra):
        return g.handle("computer.act", {"request_id": "request-0001", "target": "mock:test",
            "action": action, "args": args or {}, **extra})
    def test_browser_adapter_rejects_unlisted_origin(self):
        adapter = BrowserAdapter(["https://example.test"], "/tmp/cucb-test-profile")
        with self.assertRaises(PermissionError):
            adapter._check_origin("https://not-allowed.test/path")
    def test_browser_adapter_rejects_javascript_scheme(self):
        adapter = BrowserAdapter(["https://example.test"], "/tmp/cucb-test-profile")
        with self.assertRaises(PermissionError):
            adapter._check_origin("javascript:alert(1)")
    def test_browser_adapter_accepts_allowlisted_https_origin(self):
        adapter = BrowserAdapter(["https://example.test"], "/tmp/cucb-test-profile")
        adapter._check_origin("https://example.test/path")
    def test_describe_disclaims_real_device(self):
        g = self.make_gateway()
        self.assertFalse(g.handle("computer.describe", {})["real_device_access"])
    def test_observe_only_denies_click(self):
        g = self.make_gateway(mode="observe_only")
        self.assertEqual(self.call(g, "click", {"element_id": "test-button"})["status"], "denied")
    def test_unknown_tool_denied(self):
        g = self.make_gateway()
        self.assertEqual(g.handle("computer.shell_exec", {})["status"], "denied")
    def test_missing_scope_denied(self):
        g = self.make_gateway(scopes=["computer.describe", "computer.observe"])
        self.assertEqual(self.call(g, "click", {"element_id": "test-button"})["error"]["code"], "MISSING_SCOPE")
    def test_approval_required(self):
        g = self.make_gateway(approval=["navigate"])
        result = self.call(g, "navigate", {"url": "https://example.test"})
        self.assertEqual(result["status"], "needs_approval")
        self.assertIn(result["approval_id"], g.approvals)
    def test_target_allowlist(self):
        g = self.make_gateway()
        result = g.handle("computer.observe", {"target": "desktop:other"})
        self.assertEqual(result["status"], "denied")
    def test_postcondition_verified(self):
        g = self.make_gateway(approval=[])
        result = self.call(g, "click", {"element_id": "test-button"}, expected_state="Success")
        self.assertEqual(result["status"], "succeeded")
    def test_postcondition_mismatch_uncertain(self):
        g = self.make_gateway(approval=[])
        result = self.call(g, "click", {"element_id": "test-button"}, expected_state="not present")
        self.assertEqual(result["status"], "uncertain")
    def test_idempotency_deduplicates(self):
        g = self.make_gateway(approval=[])
        args = {"request_id": "request-0001", "target": "mock:test", "action": "click",
                "args": {"element_id": "test-button"}, "idempotency_key": "idem-key-0001"}
        a = g.handle("computer.act", args)
        b = g.handle("computer.act", args)
        self.assertEqual(a, b)
        self.assertEqual(g.adapter.state["click_count"], 1)
    def test_audit_is_appended(self):
        g = self.make_gateway(mode="observe_only")
        g.handle("computer.describe", {})
        self.assertTrue(Path(g.audit_path).exists())
        self.assertGreaterEqual(len(Path(g.audit_path).read_text().splitlines()), 1)
    def test_stale_observation_denied(self):
        g = self.make_gateway(approval=[])
        g.handle("computer.observe", {"target": "mock:test"})
        result = self.call(g, "click", {"element_id": "test-button"}, observation_id="old-observation")
        self.assertEqual(result["error"]["code"], "STALE_OBSERVATION")

if __name__ == "__main__":
    unittest.main(verbosity=2)
