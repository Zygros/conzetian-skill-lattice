"""CUCB v0.1 reference gateway. Mock adapter only; no real device control."""
from __future__ import annotations
import hashlib, json, os, secrets, threading, time, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

VERSION = "0.1.0"
ACTIONS = {"click", "type_text", "key_press", "scroll", "navigate", "read_text", "screenshot", "wait", "open_app"}
READ_TOOLS = {"computer.describe", "computer.observe", "computer.approvals", "computer.audit"}
WRITE_SCOPES = {
    "click": "computer.click", "type_text": "computer.type", "key_press": "computer.key",
    "scroll": "computer.scroll", "navigate": "browser.navigate", "open_app": "desktop.open_app"
}
SENSITIVE = ("password", "passwd", "token", "secret", "authorization", "cookie", "api_key")

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()

def redact(value):
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if any(s in k.lower() for s in SENSITIVE) else redact(v)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        # Avoid leaking common bearer-token values in textual mock observations.
        return value[:20000]
    return value

class MockAdapter:
    """Deterministic test adapter; never interacts with a real OS or browser."""
    def __init__(self):
        self.state = {"screen": "CUCB mock ready", "click_count": 0, "text": ""}
        self.observation_counter = 0
    def describe(self):
        return {"platform": "mock", "adapter": "MockAdapter", "adapter_status": "ready",
                "capabilities": ["computer.observe", "computer.click", "computer.type",
                                 "computer.scroll", "browser.navigate"],
                "real_device_access": False}
    def observe(self, target):
        self.observation_counter += 1
        return {"target": target, "observation_id": f"mock-obs-{self.observation_counter}",
                "timestamp": time.time(), "state": dict(self.state)}
    def act(self, action, args):
        if action == "click":
            self.state["click_count"] += 1
            self.state["screen"] = "Success" if args.get("element_id") == "test-button" else "Clicked"
        elif action == "type_text":
            self.state["text"] = args["text"]
        elif action == "scroll":
            self.state["screen"] = "Scrolled"
        elif action == "navigate":
            url = args["url"]
            if not url.startswith("https://example.test/") and url != "https://example.test":
                raise PermissionError("mock adapter permits only https://example.test")
            self.state["screen"] = "Navigated to " + url
        elif action in {"read_text", "screenshot"}:
            return {"state": dict(self.state)}
        else:
            raise NotImplementedError(f"mock adapter does not implement {action}")
        return {"state": dict(self.state)}

class Gateway:
    def __init__(self, policy=None, adapter=None, audit_path=None):
        self.policy = policy or {"mode": "observe_only", "scopes": ["computer.describe", "computer.observe"],
            "targets": ["mock:test"], "approval_required_for": ["type_text", "navigate", "open_app"],
            "max_actions_per_minute": 30, "session_seconds": 3600}
        self.adapter = adapter or MockAdapter()
        self.audit_path = Path(audit_path or os.environ.get("CUCB_AUDIT_PATH", "cucb-audit.jsonl"))
        self.started = time.time()
        self.lock = threading.Lock()
        self.events = []
        self.approvals = {}
        self.idempotency = {}
        self.last_action_times = []
        self.observation_ids = {}
        self.stopped = False
    def _audit(self, event):
        row = {"event_id": str(uuid.uuid4()), "timestamp": time.time(), **redact(event)}
        with self.lock:
            self.events.append(row)
            self.audit_path.parent.mkdir(parents=True, exist_ok=True)
            with self.audit_path.open("a", encoding="utf-8") as f:
                f.write(canonical(row) + "\n")
        return row
    def _target(self, target):
        return isinstance(target, str) and target in self.policy.get("targets", [])
    def _scope(self, scope):
        return scope in self.policy.get("scopes", [])
    def _rate_limit(self):
        now = time.time()
        self.last_action_times = [t for t in self.last_action_times if now - t < 60]
        if len(self.last_action_times) >= int(self.policy.get("max_actions_per_minute", 30)):
            return False
        self.last_action_times.append(now)
        return True
    def handle(self, tool, args):
        if self.stopped or time.time() - self.started > int(self.policy.get("session_seconds", 3600)):
            return {"status": "denied", "error": {"code": "SESSION_STOPPED_OR_EXPIRED"}}
        if not isinstance(args, dict):
            return {"status": "denied", "error": {"code": "INVALID_ARGS"}}
        if tool == "computer.describe":
            result = {"version": VERSION, **self.adapter.describe(),
                "mode": self.policy.get("mode", "observe_only"),
                "scopes": self.policy.get("scopes", []),
                "targets": self.policy.get("targets", []),
                "session_expires_in_seconds": max(0, int(self.policy.get("session_seconds", 3600) - (time.time()-self.started)))}
            self._audit({"tool": tool, "status": "succeeded"})
            return result
        if tool == "computer.observe":
            target = args.get("target")
            if not self._scope("computer.observe") or not self._target(target):
                self._audit({"tool": tool, "target": target, "status": "denied"})
                return {"status": "denied", "error": {"code": "SCOPE_OR_TARGET_DENIED"}}
            result = self.adapter.observe(target)
            self.observation_ids[target] = result["observation_id"]
            self._audit({"tool": tool, "target": target, "status": "succeeded", "observation_id": result["observation_id"]})
            return redact(result)
        if tool == "computer.approvals":
            return {"items": list(self.approvals.values())[-100:]}
        if tool == "computer.audit":
            limit = max(1, min(100, int(args.get("limit", 20))))
            return {"events": self.events[-limit:]}
        if tool != "computer.act":
            return {"status": "denied", "error": {"code": "UNKNOWN_TOOL"}}
        request_id, target, action, payload = args.get("request_id"), args.get("target"), args.get("action"), args.get("args")
        if not isinstance(request_id, str) or len(request_id) < 8 or not self._target(target) or action not in ACTIONS or not isinstance(payload, dict):
            self._audit({"tool": tool, "status": "denied", "reason": "invalid request"})
            return {"status": "denied", "error": {"code": "INVALID_REQUEST"}}
        idem = args.get("idempotency_key")
        if idem and idem in self.idempotency:
            return self.idempotency[idem]
        if self.policy.get("mode", "observe_only") == "observe_only":
            result = {"action_id": str(uuid.uuid4()), "status": "denied", "error": {"code": "OBSERVE_ONLY"}}
        elif self.stopped or not self._rate_limit():
            result = {"action_id": str(uuid.uuid4()), "status": "denied", "error": {"code": "RATE_LIMIT_OR_STOP"}}
        elif action in WRITE_SCOPES and not self._scope(WRITE_SCOPES[action]):
            result = {"action_id": str(uuid.uuid4()), "status": "denied", "error": {"code": "MISSING_SCOPE"}}
        elif action in self.policy.get("approval_required_for", []):
            approval_id = str(uuid.uuid4())
            approval = {"approval_id": approval_id, "request_id": request_id, "target": target,
                "action": action, "payload_sha256": digest(payload), "status": "pending",
                "expires_at": time.time() + 120}
            self.approvals[approval_id] = approval
            result = {"action_id": str(uuid.uuid4()), "status": "needs_approval", "approval_id": approval_id}
        elif args.get("observation_id") and args["observation_id"] != self.observation_ids.get(target):
            result = {"action_id": str(uuid.uuid4()), "status": "denied", "error": {"code": "STALE_OBSERVATION"}}
        else:
            try:
                before = self.adapter.observe(target)
                observed = self.adapter.act(action, payload)
                after = self.adapter.observe(target)
                expected = args.get("expected_state")
                state_text = canonical(after.get("state", {}))
                verified = not expected or expected in state_text
                result = {"action_id": str(uuid.uuid4()), "status": "succeeded" if verified else "uncertain",
                          "observed_state": after, "evidence": [{"before_observation": before["observation_id"],
                          "after_observation": after["observation_id"], "expected_state": expected}]}
                if not verified:
                    result["error"] = {"code": "POSTCONDITION_NOT_OBSERVED"}
            except (PermissionError, NotImplementedError, KeyError, ValueError) as exc:
                result = {"action_id": str(uuid.uuid4()), "status": "denied" if isinstance(exc, PermissionError) else "unsupported",
                          "error": {"code": type(exc).__name__.upper(), "message": str(exc)[:300]}}
        self._audit({"tool": tool, "request_id": request_id, "target": target, "action": action,
                     "status": result["status"], "result": result})
        if idem:
            self.idempotency[idem] = result
        return result

def load_policy(path):
    if not path:
        return None
    with open(path, encoding="utf-8") as f:
        policy = json.load(f)
    if policy.get("mode") not in {"observe_only", "confirm_writes", "preapproved_allowlist"}:
        raise ValueError("invalid policy mode")
    if not isinstance(policy.get("scopes"), list) or not isinstance(policy.get("targets"), list):
        raise ValueError("policy scopes and targets must be lists")
    return policy

def serve():
    token = os.environ.get("CUCB_TOKEN")
    if not token or len(token) < 32:
        raise SystemExit("Set CUCB_TOKEN to a random secret of at least 32 characters.")
    host = os.environ.get("CUCB_HOST", "127.0.0.1")
    if host not in {"127.0.0.1", "::1", "localhost"}:
        raise SystemExit("Reference gateway only permits loopback binding.")
    policy = load_policy(os.environ.get("CUCB_POLICY"))
    gateway = Gateway(policy=policy)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def do_GET(self):
            if not secrets.compare_digest(self.headers.get("Authorization", ""), "Bearer " + token):
                self.send_error(401); return
            parsed = urlparse(self.path)
            if parsed.path == "/health":
                body = {"status": "ok", "version": VERSION, "adapter": gateway.adapter.describe()}
            elif parsed.path == "/tools":
                body = {"tools": sorted(READ_TOOLS | {"computer.act"})}
            else:
                self.send_error(404); return
            self._send(200, body)
        def do_POST(self):
            if not secrets.compare_digest(self.headers.get("Authorization", ""), "Bearer " + token):
                self.send_error(401); return
            if self.path != "/call":
                self.send_error(404); return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > 65536:
                    self._send(413, {"error": "body must be 1..65536 bytes"}); return
                req = json.loads(self.rfile.read(size))
                if set(req) != {"tool", "arguments"}:
                    self._send(400, {"error": "expected exactly tool and arguments"}); return
                self._send(200, gateway.handle(req["tool"], req["arguments"]))
            except (ValueError, json.JSONDecodeError):
                self._send(400, {"error": "invalid JSON"})
        def _send(self, status, body):
            raw = json.dumps(body).encode()
            self.send_response(status); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)
    server = ThreadingHTTPServer((host, int(os.environ.get("CUCB_PORT", "8765"))), Handler)
    print(f"CUCB {VERSION} listening on {host}:{server.server_port}; adapter=mock; device access=false")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == "__main__":
    serve()
