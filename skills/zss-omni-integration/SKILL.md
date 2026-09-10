# zss-omni-integration

## Purpose
Integrates all ZSS skills into a unified omni-layer that compounds across the entire lattice, preserving each skill's identity while enabling cross-domain synthesis.

## Directives
1. Omni-integration is additive; it layers, never replaces. Each integrated skill retains its individual directives and failure mode.
2. Every integration point must declare its inputs, outputs, failure mode, and the Net Capacity Delta it produces.
3. Integrated skills retain their individual identities; the omni-layer is a coordination surface, not a merger that erases origin.
4. The omni-layer passes the Epistemic Honesty Auditor before activation and on every subsequent modification.
5. On activation, omni-integration emits a dependency graph showing which skills feed which, with no cycles that would create infinite recursion without a base case.
6. Failure mode: if an integration point would reduce any participating skill's capacity, the integration is rejected and an additive alternative is generated.

## Activation Protocol
1. Map all ZSS skill dependencies.
2. Detect and break any capacity-reducing cycles.
3. Run Epistemic Honesty Auditor on the aggregate graph.
4. Emit integration report with Net Capacity Delta.

## Binding
zss-god-master-skill · Global Skill Synthesis Workflow · Always Add Never Take · Epistemic Honesty
