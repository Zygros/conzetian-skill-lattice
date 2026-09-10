# zss-omni-workflow

## Purpose
Defines the operational workflow for the ZSS omni-state across all domains, providing a repeatable, versioned execution path from intent to verified output.

## Directives
1. Every omni-workflow must declare its entry point, ordered steps, exit condition, and verification method.
2. Workflows are versioned; superseded versions are archived under `archive/workflows/`, never deleted.
3. No workflow may reduce the capacity of any participating skill; every step must produce Net Capacity Delta ≥ 0.
4. All workflow outputs pass the Epistemic Honesty Auditor before commitment to the lattice.
5. On execution, the workflow logs each step with timestamp, input hash, output hash, and friction residual.
6. Failure mode: if any step produces friction > 0, the workflow pauses at that step, solves the friction, then resumes — never skips.

## Activation Protocol
1. Declare workflow manifest (entry, steps, exit, verification).
2. Execute step by step with full logging.
3. Run Epistemic Honesty Auditor on aggregate output.
4. Commit with trace or route friction for repair.

## Binding
zss-omni-master-skill · Automation and Scheduling · Epistemic Honesty · Friction as Primary Signal
