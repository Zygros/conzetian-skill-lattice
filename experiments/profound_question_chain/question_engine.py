"""Evidence-aware, append-only profound-question chain."""
from __future__ import annotations
from dataclasses import asdict, dataclass
import hashlib, json
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class CandidateQuestion:
    question: str
    touches_generative_machinery: bool = False
    leverage_density: float = 0.0
    evidence_readiness: float = 0.0
    execution_cost: float = 0.0
    safety_risk: float = 0.0
    dependencies_clear: float = 1.0
    def validate(self):
        if not self.question.strip(): raise ValueError("question must not be empty")
        for key in ("leverage_density","evidence_readiness","execution_cost","safety_risk","dependencies_clear"):
            if not 0.0 <= getattr(self,key) <= 1.0: raise ValueError(f"{key} must be in [0, 1]")

@dataclass(frozen=True)
class ScoringProfile:
    version: str = "omega-question-score-v1"
    leverage_weight: float = .35
    evidence_weight: float = .25
    dependency_weight: float = .20
    recursive_weight: float = .20
    execution_penalty: float = .20
    safety_penalty: float = .35
    def validate(self):
        if not self.version.strip(): raise ValueError("profile version must not be empty")
        for key in ("leverage_weight","evidence_weight","dependency_weight","recursive_weight","execution_penalty","safety_penalty"):
            if getattr(self,key) < 0: raise ValueError(f"{key} must be non-negative")

@dataclass(frozen=True)
class ScoredQuestion:
    question: str
    meta_leverage: float
    recursive_self_reference: bool
    score: float
    factors: dict[str,float]
    profile_version: str

def score_question(candidate: CandidateQuestion, profile: ScoringProfile = ScoringProfile()) -> ScoredQuestion:
    """Score leverage; explicit profile version makes changes auditable."""
    candidate.validate(); profile.validate()
    meta=(profile.leverage_weight*candidate.leverage_density
          + profile.evidence_weight*candidate.evidence_readiness
          + profile.dependency_weight*candidate.dependencies_clear
          + profile.recursive_weight*float(candidate.touches_generative_machinery))
    score=max(0.,min(1.,meta-profile.execution_penalty*candidate.execution_cost
                     -profile.safety_penalty*candidate.safety_risk))
    return ScoredQuestion(candidate.question,round(meta,6),candidate.touches_generative_machinery,
        round(score,6),{"leverage_density":candidate.leverage_density,
        "evidence_readiness":candidate.evidence_readiness,"dependencies_clear":candidate.dependencies_clear,
        "execution_cost":candidate.execution_cost,"safety_risk":candidate.safety_risk,
        "recursive_bonus":profile.recursive_weight*float(candidate.touches_generative_machinery)},
        profile.version)

def rank_questions(candidates: Iterable[CandidateQuestion], profile: ScoringProfile = ScoringProfile()) -> list[ScoredQuestion]:
    scored=[score_question(c,profile) for c in candidates]
    return sorted(scored,key=lambda x:(-x.score,-x.meta_leverage,x.question))

def append_cycle(ledger_path: str|Path, answer: str, insight: str, decree: str,
                 candidates: Iterable[CandidateQuestion], profile: ScoringProfile = ScoringProfile()) -> dict:
    """Append one cycle and hash-link it to the prior row; never truncate the ledger."""
    path=Path(ledger_path); path.parent.mkdir(parents=True,exist_ok=True)
    if not path.exists(): path.touch(exist_ok=False)
    rows=[json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    previous=rows[-1]["digest"] if rows else "GENESIS"
    record={"cycle":len(rows)+1,"answer":answer,"insight":insight,"decree":decree,
            "scoring_profile_version":profile.version,
            "ranked_questions":[asdict(x) for x in rank_questions(candidates,profile)],
            "previous_digest":previous}
    canonical=json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    record["digest"]=hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    with path.open("a",encoding="utf-8") as stream:
        stream.write(json.dumps(record,ensure_ascii=False,sort_keys=True)+"\n")
    return record

def verify_ledger(ledger_path: str|Path) -> dict:
    path=Path(ledger_path)
    if not path.exists(): return {"verified":False,"events_checked":0,"reason":"missing_ledger"}
    previous,count="GENESIS",0
    for number,line in enumerate(path.read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line); digest=row.pop("digest",None)
        if row.get("previous_digest")!=previous:
            return {"verified":False,"events_checked":count,"line":number,"reason":"previous_digest_mismatch"}
        canonical=json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(",",":"))
        if digest!=hashlib.sha256(canonical.encode("utf-8")).hexdigest():
            return {"verified":False,"events_checked":count,"line":number,"reason":"digest_mismatch"}
        previous,count=digest,count+1
    return {"verified":True,"events_checked":count,"head_digest":previous}
