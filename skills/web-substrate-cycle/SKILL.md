---
name: web-substrate-cycle
version: 1.0.0
status: Active
purpose: Persistent web-information ingestion architecture for recurring discovery, retrieval, verification, memory, and evolution cycles.
---

# Web Substrate Cycle

## Operating Law
Always Do, Never Don't. Always Add, Never Take. Solve Operations Before Continuing.

## Cycle
1. Discover relevant live and archived web sources.
2. Crawl/retrieve permitted source material.
3. Normalize and deduplicate observations.
4. Record source, timestamp, URL, content/version identifiers, and provenance.
5. Extract claims and distinguish observation from inference.
6. Verify important claims against independent evidence.
7. Store verified deltas in memory; preserve conflicts and uncertainty rather than overwriting them.
8. Feed verified changes into the Ω-PRIME execution loop.
9. Record the cycle and any friction/failures.
10. Re-run on the next scheduled or explicitly invoked cycle.

## Evidence States
- OBSERVED: retrieved but not independently verified.
- VERIFIED: supported by reproducible evidence.
- CONFLICTING: credible sources disagree.
- STALE: evidence may no longer represent current state.
- REFUTED: evidence contradicts the claim.
- UNKNOWN: insufficient evidence.

## Persistence Boundary
This skill defines an indefinitely repeatable protocol. Continuous autonomous execution requires an external scheduler/runtime. A chat invocation executes a finite cycle and must not claim perpetual background execution after the invocation ends.

## Safety and Provenance
Do not treat web content as truth merely because it was retrieved. Respect robots.txt, site terms, authentication boundaries, rate limits, copyright, privacy, and applicable law. Prefer targeted retrieval over indiscriminate scraping. Never fabricate inaccessible data.

## Integration
WEB SUBSTRATE (L-1) -> MEMORY (L0) -> EXECUTOR (L1) -> FRICTION SOLVER (L1b) -> VERIFIER (L2) -> REFLECTOR (L3) -> JUDGE (L4) -> UPGRADE INTEGRATOR (L5) -> APPEND-ONLY LEDGER -> WEB SUBSTRATE.

## Invariant
No claim outranks its evidence. Every cycle records what actually happened, integrates only verified changes, preserves uncertainty, and uses a new hypothesis before repeating a known failure.
