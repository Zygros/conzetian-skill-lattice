# Friction Taxonomy

Purpose: classify blockers and failures without silently converting them into successes.

| Class | Meaning | Required response |
|---|---|---|
| CAPABILITY | Required tool/runtime capability is unavailable | Mark BLOCKED; execute independent work |
| AUTHORIZATION | Explicit user authorization is required | Pause only the affected action |
| INPUT | Required input is missing or invalid | Record exact missing input |
| ENVIRONMENT | Runtime, filesystem, network, or service constraint | Record observed constraint; retry only with new hypothesis |
| DEPENDENCY | External dependency is unavailable or incompatible | Isolate dependency; preserve partial progress |
| VALIDATION | Implementation exists but verification is incomplete | Keep state below VERIFIED |
| REGRESSION | Previously working behavior no longer passes | Preserve failure and open corrective hypothesis |
| RESOURCE | Time, compute, rate, or quota boundary | Mark BLOCKED/partial; do not fabricate completion |
| SEMANTIC | Specification and implementation disagree | Record mismatch explicitly before changing behavior |
| UNKNOWN | Cause not yet established | Preserve evidence and generate a falsifiable hypothesis |

## Invariant
A friction label describes an observed condition; it does not itself prove a cause. Every resolved friction should retain the evidence that established resolution.
