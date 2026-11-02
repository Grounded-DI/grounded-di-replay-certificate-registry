import unittest,tempfile,pathlib,shutil,json,subprocess,sys,hashlib
import pipeline
P=pathlib.Path(__file__).resolve().parent
class ReleaseGateTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.tmp.name); self.src=self.root/'src';self.src.mkdir();
  for n in ['request.json','policy.json','evidence.json','artifact.bin']:shutil.copy2(P/n,self.src/n)
 def tearDown(self):self.tmp.cleanup()
 def load(self,n):return json.loads((self.src/n).read_text())
 def save(self,n,v):(self.src/n).write_bytes(pipeline.encode(v))
 def run_pipe(self):
  out=self.root/'out';dest=self.root/'destination';p=subprocess.run([sys.executable,'-B',str(P/'pipeline.py'),'--src',str(self.src),'--out',str(out),'--promote',str(dest)],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);return out,dest,p.stdout
 def assert_hold(self):
  out,dest,stdout=self.run_pipe();d=json.loads((out/'06_decision.json').read_text());self.assertEqual(d['decision'],'HOLD');self.assertIn('promotion=REJECT',stdout);self.assertFalse(dest.exists());self.assertEqual(list(self.root.glob('destination/**/*')),[])
 def test_baseline(self):
  out,dest,stdout=self.run_pipe();self.assertEqual(json.loads((out/'06_decision.json').read_text())['decision'],'ELIGIBLE');self.assertIn('promotion=WROTE',stdout);self.assertEqual((dest/'promoted.bin').read_bytes(),(P/'artifact.bin').read_bytes());self.assertEqual(len(list(dest.iterdir())),1)
 def test_altered_artifact(self):(self.src/'artifact.bin').write_bytes(b'mutated');self.assert_hold()
 def test_missing_provenance(self):x=self.load('evidence.json');del x['provenance'];self.save('evidence.json',x);self.assert_hold()
 def test_failed_test(self):x=self.load('evidence.json');x['tests'][0]['status']='FAIL';self.save('evidence.json',x);self.assert_hold()
 def test_missing_test(self):x=self.load('evidence.json');x['tests'].pop();self.save('evidence.json',x);self.assert_hold()
 def test_missing_approval(self):x=self.load('evidence.json');del x['approval'];self.save('evidence.json',x);self.assert_hold()
 def test_wrong_candidate_approval(self):x=self.load('evidence.json');x['approval']['candidate_id']='different';self.save('evidence.json',x);self.assert_hold()
 def test_changed_destination(self):x=self.load('request.json');x['destination']='synthetic/releases/other';self.save('request.json',x);self.assert_hold()
 def test_changed_policy(self):x=self.load('policy.json');x['required_tests']=['unit'];self.save('policy.json',x);self.assert_hold()
 def test_malformed_request(self):x=self.load('request.json');x.pop('destination');self.save('request.json',x);self.assert_hold()
 def test_altered_decision(self):
  out=self.root/'out';pipeline.build(self.src,out);(out/'06_decision.json').write_bytes(pipeline.encode({'decision':'HOLD','reasons':['tampered']}));dest=self.root/'destination';self.assertEqual(pipeline.promote(self.src,out,dest),'REJECT');self.assertFalse(dest.exists())
 def test_coherent_wrong_decision(self):
  out=self.root/'out';pipeline.build(self.src,out);(out/'06_decision.json').write_bytes(pipeline.encode({'decision':'HOLD','reasons':[]}));c=json.loads((out/'07_commitment.json').read_text());c['artifacts']['06_decision.json']=hashlib.sha256((out/'06_decision.json').read_bytes()).hexdigest();(out/'07_commitment.json').write_bytes(pipeline.encode(c));dest=self.root/'destination';self.assertEqual(pipeline.promote(self.src,out,dest),'REJECT');self.assertFalse(dest.exists());p=subprocess.run([sys.executable,'-B',str(P/'checker.py'),'--src',str(self.src),'--out',str(out)],capture_output=True,text=True);self.assertEqual(p.returncode,1);self.assertEqual(json.loads(p.stdout)['status'],'FAIL')
if __name__=='__main__':unittest.main(verbosity=2)
