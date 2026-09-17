# Cycle Exhaustion Detector

A cycle reaches bounded exhaustion when all currently executable independent actions have completed, failed with recorded evidence, or are blocked by an unavailable capability/authorization/dependency.

## Required end-state report

- completed actions
- failed actions and evidence
- blocked actions and friction class
- untested assumptions
- next hypotheses
- remaining external dependencies

## Rule
Exhaustion is a scope boundary, not a claim of global completion. A future cycle may resume from the preserved ledger state.
