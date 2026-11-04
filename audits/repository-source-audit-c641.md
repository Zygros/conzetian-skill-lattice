# Repository Source Audit Addendum · C641

**Date:** 2026-10-16  
**Scope:** Targeted read-back of selected source files in two repositories, plus exact-path checks for the documented trading deployment entry points. This is a focused source review, not a complete security audit.

## 1. CONZETIAN-AI

Repository: https://github.com/Zygros/CONZETIAN-AI

| File | Retrieved blob SHA | Observation |
|---|---|---|
| src/conzetian_ai/config.py | 59f65badd4fbb5117eac5df199b41bb3d0fbec5e | Network and external tools default off; provider calls are dry-run unless credentials and allow_network are both configured. |
| src/conzetian_ai/tools.py | 64065b1a58812a963e9fed7505218b88129215ac | GitHub write tool is disabled by default and requires confirmation; can_execute also requires a handler. |
| src/conzetian_ai/providers.py | c691a63ce724ca9afda97a0af13f28e62bf7a145 | Uses urllib with a 90-second timeout and bearer credential from Settings. HTTP/provider failures become RuntimeError; response shape is accessed defensively only to a limited extent. |
| src/conzetian_ai/memory.py | da334a416a1dd3a8c70668fa82b6af014fcebd14 | Memory is JSONL append mode and filters unapproved entries by default; approval is represented by a mutable object flag and is not an independent authorization token. |
| src/conzetian_ai/dataset.py | 076a0d45a8ca737b9c6bf391ff5cd20c781448a0 (default branch) | Original implementation opened the requested dataset output with write/truncate mode, silently replacing an existing file. |
| tests/test_core.py | 614b88d4e94c83c147fcf2aa2ebe74585d8d8306 | Deterministic tests cover ingest/retrieval, memory approval flag, tool gating, dry-run orchestration, local swarm roles, and canonical-index metadata. |

### Fix opened
A separate draft PR #4 proposes a non-destructive ingestion guard and fixes the Phoenix Audit workflow to install the src-layout package before pytest collection:

https://github.com/Zygros/CONZETIAN-AI/pull/4

Branch: htc/c641-append-only-ingest-guard  
Head commit: 2e1ea91d43386e2efcad1f26e4ab3a91e0e50fe4  
State: open, draft, unmerged; hosted CI result not yet confirmed.

### Remaining source-level checks
- The mutable approved=True flag should not be treated as a secure identity or approval boundary if memory writes become remotely callable.
- Add provider response-schema validation and bounded response-body handling before relying on external adapters.
- Add source-ingestion policy tests for sensitive file patterns, symlinks, and output paths.
- Run the exact test suite through a successful CI run before merge.

## 2. ZYGROS-PRIME trading experiment

Repository: https://github.com/Zygros/ZYGROS-PRIME

| File | Retrieved blob SHA | Observation |
|---|---|---|
| README.md | 1081b8f6ffb9450154f5f744fa0938bdeade4b74 | Describes a 30-day BTC/USDT paper-trading comparison and mentions a later possible move to live capital; README claims are not a completed experiment result. |
| requirements.txt | 30a2978e15655dbae6663b3d0aada1270c8f7d99 | Includes requests, numpy, aiohttp, pandas, cryptography, pycryptodome, dotenv, YAML, and dev dependencies. |
| deploy_both.sh | dc08380fc26cee18fe5c2f53e77461bf18ef7da5 | Uses pip install with --break-system-packages; only warns when Telegram credentials are absent; starts tmux commands without checking that both processes stayed alive. |
| .gitignore | ab120c19bb300abc772f7203a53c0d31d8ccb653 | Includes common environment and secret file patterns. |

The README names root-level ghost_v24_control.py and ghost_v25_experimental.py, but fetches for those exact paths on the default branch returned 404. This means the documented root deployment path is not reproducible from those paths at the inspected revision. The missing paths could exist elsewhere; a complete tree inventory is still required.

### Operational decision
Do not launch the trading scripts or connect Telegram/exchange credentials based on this README alone. Before any run, locate the actual entry points, remove the need for --break-system-packages by using an isolated virtual environment, add strict credential preflight, confirm paper mode and order execution are disabled, and test kill-switch/backpressure behavior. No live trade, payment, or financial result was performed in this audit.

## 3. K50 / HTC implications

- AG_01 / AG_38: the non-destructive dataset guard is now a concrete additive fix proposal, pending CI and review.
- AG_14: Termux commands are documented in C641 but no Android device execution has occurred.
- AG_18 / AG_37: repository references do not prove live cross-node routing.
- AG_27: storefront and revenue remain unverified without a public product/checkout receipt.
- AG_29: no ARC-AGI benchmark was executed.
- AG_48: local digests and sidecar chaining need an independently retained or externally anchored head for stronger provenance.
- AG_50: finite cycle completion is not proof that every system opportunity is complete.

## Cause → effect

Targeted source read-back → concrete overwrite and deployment-friction findings → additive patch proposal and regression test → CI/review gate before merge.

## Signature

Conzetian Sovereign Framework / Phoenix  
Repository Source Audit C641
