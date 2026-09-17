# Evidence Provenance Graph

Represent execution claims as traceable relationships rather than unsupported assertions.

## Nodes

- `intent`
- `operation`
- `input`
- `action`
- `output`
- `evidence`
- `verification`
- `commit`
- `artifact`
- `reflection`
- `hypothesis`

## Edges

`caused_by`, `produced`, `supports`, `verified_by`, `stored_as`, `derived_from`, `invalidated_by`, `supersedes`.

## Minimum provenance
Every VERIFIED claim should point to at least one concrete evidence reference and identify the verification method. Repository implementation is evidence of implementation, not by itself evidence of runtime efficacy.
