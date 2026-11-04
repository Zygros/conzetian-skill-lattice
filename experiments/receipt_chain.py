#!/usr/bin/env python3
"""Create and verify a hash-chained sidecar for JSONL experiment receipts.
The source receipt is never modified. Keep the manifest/head digest independently
for meaningful truncation detection; an attacker able to rewrite all files can
recompute a local chain.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

SCHEMA = "conzetian-receipt-chain/v1"

def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))

def parse_jsonl(path: Path) -> tuple[str, list[Any]]:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    records = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on line {line_number}: {exc}") from exc
    if not records:
        raise ValueError("receipt file has no JSON records")
    return sha256_bytes(raw), records

def build_chain(source: Path, chain_path: Path, manifest_path: Path) -> dict[str, Any]:
    if source.resolve() in {chain_path.resolve(), manifest_path.resolve()}:
        raise ValueError("outputs must not overwrite the source receipt")
    if chain_path.exists() or manifest_path.exists():
        raise FileExistsError("refusing to overwrite an existing chain or manifest")
    source_sha, records = parse_jsonl(source)
    envelopes = []
    previous = None
    for index, payload in enumerate(records, 1):
        payload_sha = sha256_text(canonical(payload))
        core = {"schema_version": SCHEMA, "sequence": index,
                "previous_digest": previous, "payload_sha256": payload_sha,
                "payload": payload}
        digest = sha256_text(canonical(core))
        envelopes.append({**core, "digest": digest})
        previous = digest
    chain_text = "".join(canonical(row) + "\n" for row in envelopes)
    manifest = {"schema_version": SCHEMA, "record_count": len(envelopes),
                "source_sha256": source_sha, "chain_sha256": sha256_text(chain_text),
                "head_digest": previous}
    created_chain = False
    try:
        with chain_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(chain_text)
        created_chain = True
        with manifest_path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(canonical(manifest) + "\n")
    except Exception:
        if created_chain and not manifest_path.exists():
            chain_path.unlink(missing_ok=True)
        raise
    return manifest

def verify_chain(chain_path: Path, manifest_path: Path) -> dict[str, Any]:
    try:
        chain_raw = chain_path.read_bytes()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        rows = [json.loads(line) for line in chain_raw.decode("utf-8").splitlines() if line.strip()]
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return {"verified": False, "reason": "read_or_parse_error", "detail": str(exc)}
    previous = None
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            return {"verified": False, "checked": index, "reason": "row_not_object"}
        core = {k: row.get(k) for k in ("schema_version", "sequence", "previous_digest", "payload_sha256", "payload")}
        if core["schema_version"] != SCHEMA or core["sequence"] != index:
            return {"verified": False, "checked": index, "reason": "schema_or_sequence_mismatch"}
        if core["previous_digest"] != previous:
            return {"verified": False, "checked": index, "reason": "previous_digest_mismatch"}
        if sha256_text(canonical(core["payload"])) != core["payload_sha256"]:
            return {"verified": False, "checked": index, "reason": "payload_digest_mismatch"}
        expected = sha256_text(canonical(core))
        if row.get("digest") != expected:
            return {"verified": False, "checked": index, "reason": "row_digest_mismatch"}
        previous = expected
    if manifest.get("schema_version") != SCHEMA:
        return {"verified": False, "reason": "manifest_schema_mismatch"}
    if manifest.get("record_count") != len(rows):
        return {"verified": False, "reason": "record_count_mismatch", "actual_count": len(rows)}
    if manifest.get("head_digest") != previous:
        return {"verified": False, "reason": "head_digest_mismatch"}
    if manifest.get("chain_sha256") != sha256_bytes(chain_raw):
        return {"verified": False, "reason": "chain_file_digest_mismatch"}
    return {"verified": True, "records_checked": len(rows), "head_digest": previous,
            "chain_sha256": sha256_bytes(chain_raw), "source_sha256": manifest.get("source_sha256")}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create")
    create.add_argument("--source", type=Path, required=True)
    create.add_argument("--chain", type=Path, required=True)
    create.add_argument("--manifest", type=Path, required=True)
    verify = sub.add_parser("verify")
    verify.add_argument("--chain", type=Path, required=True)
    verify.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = build_chain(args.source, args.chain, args.manifest) if args.command == "create" else verify_chain(args.chain, args.manifest)
    except (OSError, ValueError) as exc:
        print(json.dumps({"verified": False, "reason": type(exc).__name__, "detail": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if args.command == "create" or result.get("verified") else 1

if __name__ == "__main__":
    raise SystemExit(main())
