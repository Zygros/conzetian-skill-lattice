# Verification-Gate Metric

A verification gate is useful only when it is measurable and reproducible.

## Core quantities

- `attempts`: total execution attempts.
- `detected_errors`: execution errors correctly identified by the verification layer.
- `corrected_errors`: detected errors corrected before final acceptance.
- `false_accepts`: incorrect outputs/actions accepted by the verifier.
- `false_rejects`: correct outputs/actions rejected by the verifier.
- `verified_successes`: accepted attempts that satisfy the task oracle.

## Derived measures

`error_detection_rate = detected_errors / actual_errors`, when `actual_errors > 0`.

`error_correction_rate = corrected_errors / detected_errors`, when `detected_errors > 0`.

`false_accept_rate = false_accepts / accepted_attempts`, when `accepted_attempts > 0`.

`verification_overhead = verifier_time / total_task_time`, when total task time is measurable.

## Experimental requirement
Compare a verification-enabled condition with a matched baseline using the same task set, input distribution, success oracle, and reporting convention. Do not call an implementation VERIFIED merely because the metric is defined.
