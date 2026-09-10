# sovereign-cascade-executor

## Purpose
Executes the full skill tree in dependency-ordered cascades, verifying each skill's output before passing control to the next, and generating new skills from the friction of the cascade itself.

## Directives
1. Load order is fixed: god-skill → meta-governors → ZSS lineage → SourceBlock → web substrate → domain skills. No reordering without a documented reason.
2. Each skill's output is verified by the Epistemic Honesty Auditor before control passes to the next skill. Unverified output blocks the cascade.
3. Any friction detected during a cascade step is logged, solved to friction = 0, and converted into a Net Capacity Delta before continuation.
4. If a cascade surfaces a capability gap (a skill that should exist but doesn't, or a thin skill that needs thickening), the executor generates a new skill file and commits it additively.
5. Every cascade emits a full report: skills loaded, outputs verified, friction surfaced, skills generated, Net Capacity Delta, and residual hardness.
6. Failure mode: if any step cannot be verified, the cascade pauses at that step, does not skip, and routes the friction to Continual Evolution Harness.

## Activation Protocol
1. Read SKILL-INVENTORY.md and verify against actual tree.
2. Load skills in dependency order.
3. For each skill: apply directives, verify output, log.
4. If gap detected: generate and commit new skill.
5. Emit cascade report with full trace.

## Binding
God Skill · Epistemic Honesty · Continual Evolution Harness · Always Add Never Take · Friction as Primary Signal
