import subprocess, sys, tempfile, unittest
from pathlib import Path
SCRIPT=Path(__file__).with_name("paired_baseline_harness.py")
class HarnessTests(unittest.TestCase):
 def test_duplicate_task_ids_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"t.jsonl"; p.write_text('{"task_id":"x","input":1,"expected":1}\n{"task_id":"x","input":2,"expected":2}\n')
   r=subprocess.run([sys.executable,str(SCRIPT),"--tasks",str(p),"--baseline","echo","--monitored","echo","--out",str(Path(d)/"o")],capture_output=True,text=True)
   self.assertEqual(r.returncode,2); self.assertIn("unique",r.stderr)
 def test_refuses_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"t.jsonl"; o=Path(d)/"o.jsonl"; p.write_text('{"task_id":"x","input":1,"expected":1}\n'); o.write_text("existing\n")
   r=subprocess.run([sys.executable,str(SCRIPT),"--tasks",str(p),"--baseline","echo","--monitored","echo","--out",str(o)],capture_output=True,text=True)
   self.assertEqual(r.returncode,2); self.assertEqual(o.read_text(),"existing\n")
 def test_paired_end_to_end(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); p=root/"t.jsonl"; o=root/"out.jsonl"; ad=root/"ad.py"
   p.write_text('{"task_id":"case-1","input":{"x":1},"expected":2}\n')
   ad.write_text('import json,sys\nt=json.loads(sys.stdin.readline())\nprint(json.dumps({"answer":t["input"]["x"]+1}))\n')
   cmd=f"{sys.executable} {ad}"
   r=subprocess.run([sys.executable,str(SCRIPT),"--tasks",str(p),"--baseline",cmd,"--monitored",cmd,"--out",str(o)],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr); lines=o.read_text().splitlines(); self.assertEqual(len(lines),2)
   self.assertTrue(__import__("json").loads(lines[0])["baseline_correct"]); self.assertTrue(__import__("json").loads(lines[0])["monitored_correct"])
   self.assertEqual(__import__("json").loads(lines[1])["accuracy_delta_monitored_minus_baseline"],0.0)
if __name__=="__main__": unittest.main()