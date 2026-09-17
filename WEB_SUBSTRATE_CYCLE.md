# 🌐 Web Substrate Cycle

The Conzetian architecture treats the web as an external information substrate, not as an authority.

**Cycle:** Discover → Retrieve → Normalize → Deduplicate → Timestamp → Extract Claims → Verify → Memory → Evolve → Repeat.

**Evidence boundary:** Retrieved content is OBSERVED until independently verified. Conflicts, stale information, uncertainty, and refutations are preserved rather than silently overwritten.

**Persistence boundary:** The protocol is designed for indefinite recurrence, but continuous background execution requires an external scheduler/runtime. Individual ChatGPT invocations are finite.

**Operations-before-continuation:** failures, rate limits, inaccessible sources, parser errors, provenance gaps, and verification conflicts are recorded and resolved or bounded before the affected pipeline continues.

**Invariant:** Always Do, Never Don't. Always Add, Never Take. No claim outranks its evidence.
