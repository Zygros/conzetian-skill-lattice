# CUCB: setup and implementation

The Conzetian Universal Computer-Control Bridge (CUCB) is the execution layer for the `conzetian-computer-operator` skill.

## Cascading implementation status

- [x] **Phase 0: Standard** — architecture, tool contracts, permission boundaries and failure semantics.
- [x] **Phase 1: Reference gateway** — local HTTP gateway, bearer-token authentication, loopback-only binding, policy checks, action allowlist, rate limit, session expiry, append-only JSONL audit, idempotency handling and a mock adapter.
- [x] **Phase 2: Mock verification suite written** — executable unit tests for observe-only denial, scopes, target allowlist, approvals-needed response, postcondition mismatch, idempotency, audit and stale observations.
- [x] **Phase 2b: CI wired** — GitHub Actions workflow compiles the Python and runs the unit tests on push, pull request and manual dispatch.
- [x] **Phase 2c: CI tests executed** — GitHub Actions run [39163517135](https://github.com/Zygros/conzetian-skill-lattice/actions/runs/39163517135) completed successfully. Python compilation and the mock-adapter unit test suite both passed.
- [ ] **Phase 3: Browser adapter** — not implemented.
- [ ] **Phase 4: Desktop adapter** — not implemented.
- [ ] **Phase 5: Android adapter** — not implemented.
- [ ] **Phase 6: Live end-to-end verification** — not run; no device access claimed.

The current gateway uses `MockAdapter` only. Its own describe response explicitly says `real_device_access: false`. It is a local reference implementation, not yet a production-hardened bridge. Human approval resolution and MCP transport still need to be implemented before consequential real actions.

## Run locally

Requires Python 3.10+ and no third-party packages.

```sh
cd computer-control-bridge
python -m py_compile gateway.py test_gateway.py
python -m unittest -v
```

Start the mock gateway on loopback only. Set a unique token outside prompts and source control:

```sh
export CUCB_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
python gateway.py
```

In another terminal, use the token to inspect the mock-only gateway:

```sh
curl -H "Authorization: Bearer $CUCB_TOKEN" http://127.0.0.1:8765/health
curl -H "Authorization: Bearer $CUCB_TOKEN" http://127.0.0.1:8765/tools
curl -X POST -H "Authorization: Bearer $CUCB_TOKEN" -H "Content-Type: application/json" \
  -d '{"tool":"computer.describe","arguments":{}}' http://127.0.0.1:8765/call
```

Expected description includes `"platform":"mock"` and `"real_device_access":false`. Do not expose this reference server beyond loopback. The bearer token is an initial local guard, not a complete remote pairing or production authentication design.

## Platform integration order

### Browser
Use a dedicated browser profile and a Playwright/WebDriver/CDP adapter. Restrict origins and keep cookies/passwords out of AI output. Test on a local fixture page. Confirm public posts, messages, checkout and account/security changes.

### Desktop
Run as the signed-in user, not root/Administrator. Use OS accessibility/UI automation and allowlisted applications/filesystem roots. Test with a disposable window.

### Android / Termux
Termux does not inherently have full Android UI control. Use a companion app with a user-enabled AccessibilityService or developer-owned ADB access. Keep the bridge local-only, show an active-session indicator and provide a stop switch.

## Required security invariants

1. Default deny; explicit scopes and target allowlists.
2. Observe first; stale observations cannot authorize coordinate actions.
3. Approval must be bound to the exact action/payload, expire, and be single-use.
4. Idempotency keys prevent accidental duplicate non-idempotent actions.
5. Verify postconditions; report `uncertain` when an outcome cannot be proven.
6. Redact secrets; append audit events instead of silently rewriting them.
7. No generic shell tool in the baseline.
8. Do not retry an action that may have submitted until observing whether it already happened.

See [SPEC.md](SPEC.md), [tool-schemas.json](tool-schemas.json), [policy.observe-only.example.json](policy.observe-only.example.json), and [conformance-tests.json](conformance-tests.json).
