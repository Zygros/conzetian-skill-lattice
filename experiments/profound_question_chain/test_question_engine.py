import json
import pytest
from question_engine import CandidateQuestion, append_cycle, score_question, verify_ledger

def test_recursive_impact_adds_meta_leverage():
    a=CandidateQuestion("More content", False, .8, .8, .1, 0, 1)
    b=CandidateQuestion("Improve future scoring", True, .8, .8, .1, 0, 1)
    assert score_question(b).score > score_question(a).score

def test_risk_penalty():
    a=CandidateQuestion("Safe validation", True, .8, .9, .2, 0, 1)
    b=CandidateQuestion("Unknown execution", True, .8, .9, .2, 1, 1)
    assert score_question(a).score > score_question(b).score

def test_invalid_values_rejected():
    with pytest.raises(ValueError): score_question(CandidateQuestion(" "))
    with pytest.raises(ValueError): score_question(CandidateQuestion("bad", leverage_density=2))

def test_append_chain_and_verify(tmp_path):
    p=tmp_path/"ledger.jsonl"; c=[CandidateQuestion("Next verified question", True, .9, .8, .1, 0, 1)]
    a=append_cycle(p,"answer 1","insight 1","Ω-D4",c)
    b=append_cycle(p,"answer 2","insight 2","Ω-D5",c)
    assert b["cycle"]==2 and b["previous_digest"]==a["digest"]
    assert verify_ledger(p)["verified"] is True
    assert verify_ledger(p)["events_checked"]==2

def test_tampering_detected(tmp_path):
    p=tmp_path/"ledger.jsonl"; c=[CandidateQuestion("Verify?",True,.7,.8,.1,0,1)]
    append_cycle(p,"answer","insight","Ω-D4",c)
    row=json.loads(p.read_text().splitlines()[0]); row["answer"]="changed"
    p.write_text(json.dumps(row)+"\n")
    assert verify_ledger(p)["verified"] is False

def test_existing_rows_preserved(tmp_path):
    p=tmp_path/"ledger.jsonl"; c=[CandidateQuestion("Continue",True,.8,.8,.1,0,1)]
    append_cycle(p,"a","i","D1",c); before=p.read_text()
    append_cycle(p,"b","j","D2",c)
    assert len(p.read_text().splitlines())==len(before.splitlines())+1
