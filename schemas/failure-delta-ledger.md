# Failure-Delta Ledger

Append-only record for observed execution failures and the next hypothesis.

Each entry should preserve:

1. cycle identifier
2. execution identifier
3. timestamp
4. intended operation
5. observed outcome
6. friction class
7. evidence references
8. causal hypothesis
9. corrective action
10. verification result
11. next hypothesis
12. content hash or commit identifier when available

## Rule
A failure is learning state, not erased state. A subsequent attempt may supersede an interpretation, but must not delete the original observation.
