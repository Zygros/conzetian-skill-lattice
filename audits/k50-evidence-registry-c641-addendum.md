# K50 Evidence Registry Addendum · C641

This addendum supplements, and does not replace, the original 50-agent declaration registry.

| K50 item | Additive evidence | Current status | Still required |
|---|---|---|---|
| AG_01 / AG_38 STATE_LOCK | Phoenix Manifestation Core has SQLite WAL and SHA-256 hash-chained audit events; concurrent read-link-write serialization is covered by regression and 100-write stress tests in the C641 package. | TESTED locally in bounded runtime | Independent external head anchor; Termux reproduction; broader corruption/recovery tests |
| AG_04 HTC | C641 execution cycle, local compile/test record, package, and GitHub CI workflow have been created. | IMPLEMENTED; local tests PASS; hosted CI status must be checked per commit | Device-level HTC, repeatable workload/throughput measurements, finite resource bounds |
| AG_09 OTS / AG_48 PROVENANCE | Receipt-chain sidecar records source hash, payload hashes, sequence linkage, terminal head, and manifest count. | IMPLEMENTED; 4 local tests PASS | Real OTS proof and independent verification of the exact digest |
| AG_14 TERMUX / AG_13 MOBILE | Termux commands and test procedure documented. | DOCUMENTED, NOT DEVICE-TESTED | Run on the actual Samsung Galaxy A17 and capture environment/version output |
| AG_18 OMNINET / AG_37 AUTO_ROUTE | No live multi-node route was exercised in this cycle. | NOT VERIFIED HERE | Authorized node inventory, route traces, timeout/failure tests |
| AG_21 MITOSIS | Concurrent writes tested at 100 requests / 8 workers; no agent swarm was spawned. | BOUNDED CONCURRENCY TEST ONLY | Resource-limited worker lifecycle, cancellation, shutdown and backpressure tests |
| AG_27 GUMROAD | Existing storefront concept is retained as a separate pending business task. | NOT VERIFIED HERE | Public product URL and end-to-end checkout test |
| AG_29 ARC_AGI | No ARC-AGI benchmark was run. | NOT VERIFIED HERE | Dataset/version, held-out task set, scoring, reproducible run receipt |
| AG_45 VALENCE | The name is retained as architecture vocabulary, not evidence of subjective consciousness. | HYPOTHESIS / NOT OPERATIONALIZED | Operational definition and reproducible observables |
| AG_50 OMEGA | Finite test lists close individual cycles; they do not establish terminal completion of every system opportunity. | CYCLE-LOCAL COMPLETION ONLY | Explicit finite acceptance criteria per future cycle |

## Cross-cycle gates carried forward
- The C641 GitHub Actions workflow is in progress/awaiting final status at time of this addendum; do not label it passing until the hosted run concludes successfully.
- PR #2 in conzetian-skill-lattice remains open and unmerged. The repository's prior report says initial evidence CI and audit runs passed; this new change requires a fresh run.
- Seven-repository triage remains README-level only. Source-level audits, secret scanning, licensing review, and runtime reproduction are still outstanding.
- Revenue, live provider API, live Android/Termux, external anchors, and cross-node mesh remain separate evidence gates.

The register distinguishes a tested local primitive from the much larger capability named by each K50 label.
