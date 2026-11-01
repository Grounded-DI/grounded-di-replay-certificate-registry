import unittest,tempfile,json,hashlib
from pathlib import Path
from demo import generate,encode
class DeadlineTests(unittest.TestCase):
 def run_case(self,cases):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'run';generate({'cases':cases},p);return {x.name:x.read_bytes() for x in p.iterdir()}
 def test_expected_and_missing_ambiguous(self):
  x=self.run_case(json.loads(Path('input.json').read_text())['cases']);self.assertEqual(json.loads(x['06_decisions.json']),[{'id':'A','status':'READY','deadline':'2026-11-16'},{'id':'B','status':'HOLD','deadline':None},{'id':'C','status':'HOLD','deadline':None}])
 def test_weekend(self):
  x=self.run_case([{'id':'A','service_dates':['2026-11-05']}]);self.assertEqual(json.loads(x['04_raw.json'])[0]['raw'],'2026-11-15');self.assertEqual(json.loads(x['06_decisions.json'])[0]['deadline'],'2026-11-16')
 def test_altered_input(self):
  x=self.run_case([{'id':'A','service_dates':['2026-11-10']}]);self.assertEqual(json.loads(x['06_decisions.json'])[0]['deadline'],'2026-11-20')
 def test_altered_output(self):
  x=self.run_case([{'id':'A','service_dates':['2026-11-06']}]);h=json.loads(x['07_commitment.json']);self.assertNotEqual(hashlib.sha256(x['06_decisions.json']+b' ').hexdigest(),h['06_decisions.json'])
 def test_coherent_wrong_result(self):
  x=self.run_case([{'id':'A','service_dates':['2026-11-06']}]);wrong=encode([{'id':'A','status':'READY','deadline':'2026-11-17'}]);h=json.loads(x['07_commitment.json']);h['06_decisions.json']=hashlib.sha256(wrong).hexdigest();self.assertEqual(hashlib.sha256(wrong).hexdigest(),h['06_decisions.json']);self.assertNotEqual(json.loads(wrong)[0]['deadline'],'2026-11-16')
if __name__=='__main__':unittest.main()
