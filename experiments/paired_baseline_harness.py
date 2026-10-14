#!/usr/bin/env python3
"""Reproducible paired baseline-vs-process-monitoring experiment harness."""
from __future__ import annotations
import argparse, hashlib, json, random, shlex, subprocess, sys, time
from pathlib import Path
from typing import Any
SCHEMA = "macd-paired-run/v1"
def canonical(v: Any) -> str: return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def digest(s: str) -> str: return hashlib.sha256(s.encode("utf-8")).hexdigest()
def load_tasks(path: Path) -> list[dict[str, Any]]:
    tasks=[]
    for n,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip() or line.lstrip().startswith("#"): continue
        try: item=json.loads(line)
        except json.JSONDecodeError as e: raise ValueError(f"Invalid JSONL at line {n}: {e}") from e
        if not isinstance(item,dict) or not isinstance(item.get("task_id"),str) or "input" not in item or "expected" not in item: raise ValueError(f"Line {n} requires task_id (string), input, and expected")
        tasks.append(item)
    if not tasks: raise ValueError("Task file contains no usable cases")
    ids=[t["task_id"] for t in tasks]
    if len(ids)!=len(set(ids)): raise ValueError("task_id values must be unique")
    return tasks
def run_adapter(command: str, task: dict[str,Any], timeout: float) -> dict[str,Any]:
    start=time.monotonic()
    try:
        p=subprocess.run(shlex.split(command),input=canonical(task)+"\n",text=True,capture_output=True,timeout=timeout,check=False); ms=round((time.monotonic()-start)*1000,3)
        if p.returncode: return {"ok":False,"error":"adapter_nonzero_exit","returncode":p.returncode,"stderr":p.stderr[-2000:],"elapsed_ms":ms}
        try: result=json.loads(p.stdout)
        except json.JSONDecodeError: return {"ok":False,"error":"adapter_invalid_json","stdout":p.stdout[-2000:],"elapsed_ms":ms}
        if not isinstance(result,dict) or "answer" not in result: return {"ok":False,"error":"adapter_missing_answer","output":result,"elapsed_ms":ms}
        return {"ok":True,"answer":result["answer"],"metadata":result.get("metadata",{}),"elapsed_ms":ms}
    except subprocess.TimeoutExpired: return {"ok":False,"error":"adapter_timeout","timeout_seconds":timeout,"elapsed_ms":round((time.monotonic()-start)*1000,3)}
    except FileNotFoundError as e: return {"ok":False,"error":"adapter_not_found","detail":str(e),"elapsed_ms":round((time.monotonic()-start)*1000,3)}
def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--tasks",required=True,type=Path); ap.add_argument("--baseline",required=True); ap.add_argument("--monitored",required=True); ap.add_argument("--out",required=True,type=Path); ap.add_argument("--seed",type=int,default=420); ap.add_argument("--timeout",type=float,default=30); a=ap.parse_args()
    if a.out.exists(): print(f"Refusing to overwrite existing receipt file: {a.out}",file=sys.stderr); return 2
    if a.timeout<=0: print("--timeout must be positive",file=sys.stderr); return 2
    try: tasks=load_tasks(a.tasks)
    except (OSError,ValueError) as e: print(str(e),file=sys.stderr); return 2
    raw=a.tasks.read_text(encoding="utf-8"); rng=random.Random(a.seed); rows=[]; totals={"baseline_correct":0,"monitored_correct":0,"pairs_complete":0,"baseline_errors":0,"monitored_errors":0}
    for task in tasks:
        arms=[("baseline",a.baseline),("monitored",a.monitored)]; rng.shuffle(arms); outcomes={}
        for name,cmd in arms: outcomes[name]=run_adapter(cmd,task,a.timeout)
        row={"schema_version":SCHEMA,"task_id":task["task_id"],"task_sha256":digest(canonical(task)),"arm_order_seed":a.seed,"outcomes":outcomes}
        for name in ("baseline","monitored"):
            o=outcomes[name]; correct=bool(o.get("ok")) and canonical(o.get("answer"))==canonical(task["expected"]); row[name+"_correct"]=correct; row[name+"_error"]=not o.get("ok",False); totals[name+"_correct"]+=int(correct); totals[name+"_errors"]+=int(not o.get("ok",False))
        totals["pairs_complete"]+=int(outcomes["baseline"].get("ok",False) and outcomes["monitored"].get("ok",False)); rows.append(row)
    summary={"schema_version":SCHEMA,"record_type":"experiment_summary","created_unix":int(time.time()),"task_file":str(a.tasks),"task_file_sha256":digest(raw),"task_count":len(tasks),"baseline_command":a.baseline,"monitored_command":a.monitored,"seed":a.seed,"timeout_seconds":a.timeout,"totals":totals,"baseline_accuracy":totals["baseline_correct"]/len(tasks),"monitored_accuracy":totals["monitored_correct"]/len(tasks),"accuracy_delta_monitored_minus_baseline":(totals["monitored_correct"]-totals["baseline_correct"])/len(tasks),"interpretation_boundary":"Exact-match result on supplied cases only; not proof of general intelligence or causation without controlled adapter equivalence and task validity."}
    a.out.parent.mkdir(parents=True,exist_ok=True)
    with a.out.open("x",encoding="utf-8") as f:
        for row in rows: f.write(canonical(row)+"\n")
        f.write(canonical(summary)+"\n")
    print(json.dumps(summary,indent=2,ensure_ascii=False)); return 0
if __name__=="__main__": raise SystemExit(main())