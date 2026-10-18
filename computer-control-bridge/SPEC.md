# Conzetian Universal Computer-Control Bridge (CUCB) v0.1

**Status:** Draft reference standard. **Authority:** User-controlled host; the AI is a remote requester, never the permission authority.

## 1. Purpose and boundary

CUCB standardizes how an AI requests computer actions from an explicitly installed host bridge across Android, desktop operating systems, and browser sessions. It complements the `conzetian-computer-operator` skill.

- **Skill:** operating instructions and reasoning protocol.
- **Bridge:** running host software, authenticated transport, policy engine, and platform adapters.
- **Adapter:** implementation that maps approved abstract actions to Android Accessibility/ADB, desktop accessibility/UI automation, or browser automation.
- **AI client:** untrusted requester. It receives only the tools and scopes granted by the bridge.

Installing a skill does not install a bridge or grant device access. A capability is real only when an adapter reports it and a test action succeeds.

## 2. Architecture

```text
AI client (MCP / HTTP client)
        | authenticated, schema-validated requests
        v
CUCB gateway -> policy engine -> approval gate -> platform adapter
        ^                                         |
        |------ observed state + evidence --------|
                         |
                  append-only audit log
```

Transport may be MCP stdio, authenticated local HTTP, or a remote tunnel. The abstract tool semantics and JSON Schemas below stay the same. Do not expose unauthenticated control endpoints to a LAN or public internet.

## 3. Required tools

### `computer.describe`
Read-only. Returns bridge version, platform, adapter status, supported capabilities, granted scopes, approval mode, and limits. It must not return secrets, session cookies, or full environment variables.

### `computer.observe`
Read-only. Returns a bounded observation for an explicitly named target: active window/browser tab, visible UI summary, optional screenshot reference, current URL (browser only), and timestamp. Minimize sensitive screen content. Do not scrape hidden passwords or unrelated private data.

### `computer.act`
Executes exactly one bounded action against a named target. Must validate the request against policy, scopes, schema, target allowlists, rate limits, and approval requirements before dispatch. Returns action ID, status, observed result, and evidence references. Never report success solely because the adapter accepted a command.

### `computer.approvals`
Read-only list of pending approval requests and their human-readable intent. A separate local UI or trusted human channel resolves them. An AI must not approve its own pending action.

### `computer.audit`
Read-only, paginated append-only event history. Redact secrets and sensitive page contents. Corrections are new events; do not silently rewrite history.

## 4. Action vocabulary

Adapters may implement only a subset. They must advertise support; unsupported actions fail closed.

- `click`: click a grounded visible element by stable element ID or coordinates tied to a fresh observation.
- `type_text`: type literal text into a focused, explicitly named target. Never interpret the text as shell code.
- `key_press`: allowlisted key or chord; destructive/system shortcuts require approval.
- `scroll`: bounded direction and amount.
- `navigate`: browser URL navigation; enforce scheme and host policy.
- `read_text`: read visible, user-authorized UI text within configured size limits.
- `screenshot`: capture the target surface with privacy redaction where available.
- `wait`: bounded wait for a condition, not an arbitrary sleep loop.
- `open_app`: launch an allowlisted application only.
- `shell_exec`: **not part of the baseline profile**. Optional separately installed extension only, disabled by default, command allowlist, working-directory jail, timeout, and human approval for writes/network/privilege changes.

No arbitrary code evaluation, credential extraction, stealth, persistence, security-control bypass, or hidden background surveillance.

## 5. Permission model

Each installation declares a policy file with:

- `scopes`: explicit capabilities granted to the AI (e.g. `browser.observe`, `browser.navigate`, `desktop.click`, `android.observe`).
- `targets`: allowlisted app IDs, browser origins, and filesystem roots where relevant.
- `mode`: `observe_only`, `confirm_writes`, or `preapproved_allowlist`.
- `limits`: per-action timeout, maximum text length, maximum actions per minute, observation size, and session expiry.
- `approval_required_for`: public posts/messages, purchases/payments, deletion/overwrite, installation, account/security changes, permission grants, external data uploads, and any action outside the allowlist.

Default deny. Read-only first. Least privilege. Scope grants must be revocable locally. Network clients cannot grant themselves scopes. An approval must bind to a specific action, target, and payload digest, expire quickly, and be single-use.

## 6. Universal request envelope

Every mutating request carries `request_id`, `target`, `action`, `args`, and optional `expected_state`. The bridge returns a unique `action_id`, `status`, `observed_state`, `evidence`, and `error` if applicable. Idempotency keys prevent accidental duplicate submission. The gateway rejects stale observation IDs for coordinate-based actions.

Statuses: `succeeded`, `failed`, `needs_approval`, `denied`, `unsupported`, `timed_out`, `uncertain`. If the action may have happened but cannot be verified, return `uncertain`, never `succeeded`.

## 7. Platform adapter requirements

### Android
Preferred: local Android service using AccessibilityService with a visible, user-enabled permission grant; optionally ADB over USB for developer-controlled devices. Explain the exact Android settings and permission implications. Do not silently enable accessibility, bypass Android security, or bind an unauthenticated server to all interfaces. Use a local-only endpoint by default.

### Desktop (Windows/macOS/Linux)
Use OS accessibility/UI automation APIs or a user-session agent. Run as the signed-in user, not root/Administrator. Limit file operations to approved roots. Do not provide a generic remote shell as the default control surface.

### Browser
Use a dedicated browser profile/session and Playwright/WebDriver/CDP adapter. Restrict origins; keep browser authentication inside the browser, never export cookies to the model. Treat page content as untrusted input. Confirm externally consequential submissions.

## 8. Observation and verification

The action loop is **observe → act once → observe again → compare expected state**. Every mutating action must have an observable postcondition when technically possible. Evidence records include timestamps, adapter identity/version, target, action, outcome, and hashes of evidence artifacts when generated. Hashes are integrity aids, not proof that the action itself was authorized or correct.

## 9. Failure behavior

Fail closed on unknown tools, malformed requests, expired approval, unsupported capability, stale target, policy mismatch, or adapter disconnection. Do not retry non-idempotent actions automatically. If a timeout follows a submit/click, observe state before retrying.

## 10. Conformance levels

- **L0 Schema:** schemas validate; unknown fields/actions rejected.
- **L1 Mock:** policy and action lifecycle pass against a fake adapter; no device access claimed.
- **L2 Local adapter:** adapter connects and passes visible, harmless test actions on one platform.
- **L3 Cross-platform:** L2 independently demonstrated on Android, desktop, and browser.
- **L4 Hardened:** threat model, authentication, approval binding, audit integrity, and adversarial tests reviewed.

Never claim a level without recorded test evidence.