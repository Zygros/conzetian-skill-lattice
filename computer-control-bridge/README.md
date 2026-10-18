# CUCB: setup and implementation plan

The Conzetian Universal Computer-Control Bridge (CUCB) is the execution layer for the existing `conzetian-computer-operator` skill. This folder defines the shared contract; platform adapters are installed separately and must pass local conformance tests before being advertised as available.

## Current implementation status

- [x] Portable standard and architecture
- [x] JSON Schema contracts for describe, observe, act, approvals, and audit
- [x] Action vocabulary and argument schemas
- [x] Permission boundaries, failure semantics, and conformance levels
- [ ] Runnable gateway implementation
- [ ] Android adapter
- [ ] Desktop adapter
- [ ] Browser adapter
- [ ] End-to-end device tests

This repository addition is a specification package, not a running service. It has not accessed or controlled a device.

## Setup order

### 1. Choose a host, then install the bridge there

Run the bridge on the machine you want the AI to control. For Android, that can be the phone itself; for desktop, run it in the logged-in user session; for browser-only control, run a browser adapter with a dedicated profile. Do not run a public internet listener as a first setup.

### 2. Start observe-only

Create a local policy with no write scopes. Allow only `computer.describe` and `computer.observe`. Verify platform, adapter version, target allowlist, and scopes before enabling actions.

### 3. Add narrowly scoped actions

Grant one target and one action at a time. Begin with harmless actions such as opening a test page or scrolling a local test page. Use `confirm_writes` for all mutations until the approval and audit paths have passed tests.

### 4. Connect an AI client

Expose the same tool contracts through the client's supported tool transport, preferably MCP. For local-only HTTP, bind to loopback and require an unpredictable bearer token stored outside prompts/logs. For remote access, use an authenticated private tunnel; never port-forward an unauthenticated controller.

### 5. Verify, then advertise capabilities

Run the conformance cases in `conformance-tests.json`. An adapter must not advertise a capability until the harmless test action and post-action observation both succeed. Report the actual platform and level achieved.

## Platform-specific setup notes

### Android / Termux
- Install Termux from a trusted source and keep packages updated.
- Use a local Android AccessibilityService companion app for UI interaction, or use ADB over USB for a developer-owned device. Termux alone does not automatically gain Android UI-control privileges.
- Accessibility must be enabled explicitly by the device owner in Android Settings. Show a persistent notification while control is active and provide an immediate stop switch.
- Bind local APIs to `127.0.0.1` by default. Do not expose the bridge to Wi-Fi until authentication, firewall rules, and pairing are implemented and tested.
- Validate on a harmless test screen before allowing navigation or typing into real apps.

### Windows / macOS / Linux
- Run as the signed-in user, never root/Administrator for ordinary UI control.
- Use an OS accessibility API or a UI automation adapter. Keep allowed app IDs and filesystem roots explicit.
- Start with a disposable test application/window. Require confirmation before deletion, overwrites, external submissions, purchases, or permission changes.

### Browser
- Use a dedicated browser profile and Playwright/WebDriver/CDP adapter.
- Restrict allowed origins. Do not export browser cookies or passwords to the AI.
- Test on a local fixture page first. Public posts, messages, checkout, and account/security changes require explicit confirmation.

## Suggested repo layout for the runnable gateway

```text
cucb/
  gateway/            # schema validation, auth, rate limits, policy
  adapters/
    android/           # accessibility bridge or ADB adapter
    desktop/           # OS accessibility/UI automation
    browser/           # Playwright/WebDriver
    mock/              # deterministic test adapter
  policy/
    example-policy.json
  tests/
    conformance-tests.json
  audit/
    append-only JSONL, redacted
```

## Security minimums before remote operation

1. Default deny and explicit per-action scopes.
2. Local pairing plus authentication; never rely on obscurity.
3. Short-lived, single-use approvals bound to the exact target and action payload.
4. Request IDs, idempotency keys, stale-observation checks, and rate limits.
5. Append-only audit events with secret redaction.
6. Stop button and session expiry.
7. No generic shell tool in the baseline.
8. Do not retry a potentially submitted action until observing whether it already occurred.

See [SPEC.md](SPEC.md), [tool-schemas.json](tool-schemas.json), and [conformance-tests.json](conformance-tests.json).
