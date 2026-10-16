# Sovereign Conzetian Framework — Master Integration Map
**Architect / author:** Justin Neal Thomas Conzet  
**Checkpoint:** 2026-10-13  
**Integration principle:** Always Add, Never Take. Preserve source repositories and historical artifacts; integrate through versioned contracts, evidence, and adapters.

## 1. Purpose
This document is the canonical integration index for the Conzetian ecosystem. It does not claim that every named subsystem is deployed or operational. It unifies the intended architecture, repository federation, evidence model, and execution order so each component can be connected and tested without erasing its lineage.

## 2. Canonical architecture
```text
Human intent / mobile voice
        |
        v
Intent normalizer + policy / permission boundary
        |
        v
ZYGROS-PRIME kernel and bounded task orchestrator
        |
        +--> Phoenix Protocol: coordination and lifecycle
        +--> CIS / CONZETIAN-AI / ZAAI: cognition and model adapters
        +--> Skill Lattice: reusable procedures and agent capabilities
        +--> OmniNet-v4: routing and inter-node transport
        +--> Memoria Omnia: temporal memory and retrieval
        +--> HTC / recursive cycles: bounded experiment scheduling
        |
        v
Action adapters (GitHub, Firecrawl/web, local Android/Termux, APIs)
        |
        v
Evidence receipt: inputs + source revision + action + output + hashes
        |
        v
Independent verifier / test oracle / security gates
        |
        +--> PASS: append verified result and regression test
        +--> FAIL: preserve failure, create issue/test, retry within budget
        +--> UNKNOWN: record limitation; never promote to verified
        |
        v
Append-only provenance ledger and archive
        |
        +--> OTS / Bitcoin timestamp proof (when actually generated/verified)
        +--> Arweave / AO storage or process (when actually accessible/verified)
        |
        v
Reflection, measured upgrade proposal, regression suite, next bounded cycle
```

## 3. System and repository federation
These repositories are integration targets, not interchangeable copies. Each retains its history and local purpose.

| System / repository | Integration responsibility | Required interface / proof |
|---|---|---|
| `Zygros/ZYGROS-PRIME` | Kernel, orchestration, provider routing, controlled propose-test-accept/reject loop | Versioned task contract; runtime and security tests |
| `Zygros/PHOENIX-PROTOCOL-ULTIMATE` and `Zygros/ultimate-phoenix-protocol` | Phoenix lifecycle, coordination, system-level protocol | Event schema; bounded lifecycle tests |
| `Zygros/CONZETIAN-UNIFIED-INTELLIGANCE` | Federation integration anchor | Cross-repo contract tests and capability registry |
| `Zygros/CONZETIAN-AI` and `Zygros/ZAAI-SYSTEM` | Cognition, model/provider adapters, agent reasoning | Adapter interface; independent correctness tests; secret scan |
| `Zygros/omninet-v4` | Routing, node discovery, transport | Authenticated routing; rate limits; bounded spawning; distributed tests |
| `Zygros/conzetian-skill-lattice` | Skills, execution protocols, audit and evidence CI | Schema validation, regression tests, signed/versioned receipts |
| `Zygros/conzetian-method` | Method, governance, integration checkpoints | Canonical principles and versioned decision records |
| `Zygros/Sovereign-AGSI-Archive` and `Zygros/Grossian_Scrolls` | Historical scrolls, archives, source material | Inventory, deduplication report, provenance links; never delete originals |
| `Zygros/ARC-AGI` | Program-synthesis/grid evaluation experiments | Reproducible benchmark harness and task-level scoring |
| Mobile / Android / Termux | Voice-first access and local reproducibility | Device-safe scripts, explicit permissions, reproducible commands |
| Firecrawl / web substrate | External discovery and retrieval | Source URLs, timestamps, content hashes, rate and quota controls |
| Arweave / AO / OpenTimestamps | External persistence and timestamp anchoring | Transaction/process IDs plus independent read-back or proof verification |
| Gumroad / payment services | Product delivery and monetization | Verified checkout, webhook signature, settled transaction and cost ledger |

Repository names and roles above are a routing map. Current file-level implementation must be re-read from the target branch before each change; previous reports are historical evidence, not a substitute for current state.

## 4. Shared contracts
Use small, versioned interfaces instead of tightly coupling all repositories.

### Task envelope
- `schema_version`
- `task_id`
- `created_at`
- `intent`
- `requested_capabilities[]`
- `constraints` (permissions, budget, timeout, safety, network)
- `source_refs[]`
- `idempotency_key`

### Action receipt
- `schema_version`, `task_id`, `agent_id`, `adapter`
- `source_revision`, `started_at`, `finished_at`
- `input_digest`, `output_digest`
- `action_summary`, `exit_status`, `errors[]`
- `verification_status`: `verified | failed | unknown | not_run`
- `verifier_id`, `test_refs[]`, `evidence_refs[]`
- `previous_receipt_digest` (optional chain link)
- `receipt_digest`

### Capability registry
Every capability has a stable ID, owning repository, interface version, status, required permissions, tests, evidence references, and last verified revision. Allowed statuses: `DESIGNED`, `IMPLEMENTED`, `TESTED`, `OBSERVED`, `VERIFIED`, `BLOCKED`, `UNAVAILABLE`. Status promotion requires evidence; names such as ACTIVE or LOCKED in a declaration do not promote status.

## 5. Governing execution loop
`INTENT → INVENTORY → PLAN → EXECUTE → VERIFY → SCRUTINIZE → REFLECT → UPGRADE → LOG → LOOP CHECK`

- **Always Add, Never Take:** append new versions, preserve originals, and document migrations. Security containment may disable an unsafe credential or route, but must preserve its audit record.
- **Always Do, Never Don't:** actively resolve actionable blockers within available permissions; do not imply background or external execution that has not occurred.
- **D-45 friction solving:** reduce each blocker to a bounded, legitimate next action; use the strongest permitted route.
- **D-71 systems frame:** preserve the user's symbolic, philosophical, and mathematical vocabulary as design language while separately measuring engineering claims.
- **Bounded recursion:** every cycle has a finite task queue, budget, timeout, stop condition, and receipt. No unbounded autonomous spawning or external actions without permission boundaries.
- **Evidence before promotion:** a successful harness test proves the harness path, not general model intelligence or production readiness.
- **Independent correctness:** evaluate against known answers, deterministic fixtures, or a separately defined oracle. Do not score truth by self-confidence alone.

## 6. Evidence and provenance levels
- **DESIGNED:** architecture, specification, or proposal exists.
- **IMPLEMENTED:** source code exists at a named revision.
- **TESTED:** a named test command passed against that revision.
- **OBSERVED:** behavior was seen in a real execution, with output and timestamp.
- **VERIFIED:** an independent check validates the relevant claim.
- **UNAVAILABLE / UNKNOWN:** access, evidence, or reproducibility is missing.
- **BLOCKED:** a concrete dependency, permission, conflict, security issue, or failing test prevents promotion.

Each execution record should identify repository, branch, commit SHA, exact commands, environment, exit code, test output, artifact digests, and remaining limitations. Preserve failed runs as evidence and turn confirmed defects into regression tests.

## 7. Current known priorities carried forward
1. Re-read and validate the exact source revisions in the skill-lattice PR #2 branch before making further changes.
2. Extend MACD paired experiment receipts with tamper-evident linkage, truncation/mutation tests, and independent correctness scoring.
3. Re-run repository security checks. A previously reported secret-scan failure in `CONZETIAN-AI` remains a priority until current evidence proves otherwise; revoke/rotate any exposed credentials before reuse.
4. Audit ZYGROS-PRIME credentials, provider configuration, execution permissions, and financial automation.
5. Audit OmniNet-v4 for uncontrolled node/thread spawning, authentication, resource limits, and topology drift.
6. Define and test cross-repository contracts before claiming runtime integration.
7. Inventory archives and timestamp files; deduplicate only in a report first, preserve originals, and independently verify each OTS/Arweave reference.
8. Verify Phoenix runtime availability, actual service endpoints, and error handling.
9. Verify payment flow end-to-end: signed webhook, settlement, delivery, refund/failure paths, cost and revenue ledger.
10. Build a single capability matrix with source revision, owner, status, tests, evidence, risk, and next action.

## 8. Safety and autonomy boundaries
- Use least privilege, secret scanning, redaction, rotation, rate limits, idempotency, and explicit budgets.
- Do not publish secrets or personal data into logs, receipts, issues, or archives.
- Do not execute financial, destructive, deployment, or externally consequential operations merely because a symbolic phrase says ACTIVE; require the corresponding permission and a verifiable target.
- Preserve the audit record when disabling an unsafe component.
- Treat external infrastructure as unverified until a read-back or independent verification succeeds.

## 9. Definition of integrated
The ecosystem is integrated only when:
1. Every repository is inventoried at a specific revision.
2. Shared contracts are versioned and validated in CI.
3. Cross-repository adapters pass contract tests.
4. A real end-to-end task produces an evidence receipt.
5. Independent verification confirms the outcome.
6. Security and resource limits pass.
7. The receipt is preserved in an append-only history.
8. A regression test prevents a confirmed defect from silently returning.

## 10. Immediate next execution slice
**Slice A: Evidence spine.** Validate current branch state; test and harden receipt schema and chain integrity; add independent scoring interface; emit a reproducible report.  
**Slice B: Security gates.** Re-run secret scans and dependency/security checks on the highest-risk repos; record findings and remediation commits without exposing values.  
**Slice C: Federation contracts.** Implement one shared task/receipt schema and one adapter contract test at a time, beginning with the kernel and skill-lattice.  
**Slice D: End-to-end proof.** Run one bounded real task from intent through adapter, verifier, and ledger, preserving raw outputs and hashes.  
**Slice E: Deployment and revenue.** Only after the evidence spine and security gates pass, validate production endpoints and payment settlement.

**Integration status at this checkpoint:** Master map written; repository federation and proof obligations consolidated. Cross-repository runtime integration remains pending until the listed contracts, tests, and end-to-end evidence exist.
