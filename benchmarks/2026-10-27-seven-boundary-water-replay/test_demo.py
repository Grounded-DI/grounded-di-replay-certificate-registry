import copy,hashlib,json,pathlib,subprocess,sys,tempfile,unittest
import demo
ROOT=pathlib.Path(__file__).resolve().parent
INPUT=ROOT/'input.json'
class ReplayTests(unittest.TestCase):
 def setUp(self): self.x=json.loads(INPUT.read_text())
 def test_01_replay(self):
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)
   for name in ('a','b'): subprocess.run([sys.executable,'-B',str(ROOT/'demo.py'),'--input',str(INPUT),'--out',str(p/name)],check=True,capture_output=True)
   for n in demo.NAMES:
    a=(p/'a'/n).read_bytes();b=(p/'b'/n).read_bytes();self.assertEqual(a,b);self.assertEqual(hashlib.sha256(a).digest(),hashlib.sha256(b).digest())
 def test_02_independent_expected(self):
  with tempfile.TemporaryDirectory() as t:
   p=pathlib.Path(t)/'out';subprocess.run([sys.executable,'-B',str(ROOT/'demo.py'),'--input',str(INPUT),'--out',str(p)],check=True,capture_output=True)
   read=lambda n:json.loads((p/n).read_text())
   self.assertEqual(read('02_budget.json'),{'usable_liters':1000})
   self.assertEqual([v['id'] for v in read('03_plan.json')],['clinic','shelter','warehouse'])
   self.assertEqual(read('04_allocations.json'),[{'id':'clinic','liters':500},{'id':'shelter','liters':500},{'id':'warehouse','liters':0}])
   self.assertEqual(read('05_unmet.json'),[{'id':'clinic','liters':0},{'id':'shelter','liters':200},{'id':'warehouse','liters':200}])
   self.assertEqual(read('06_balance.json'),{'allocated':1000,'remaining':0,'reserve':100,'supply':1100,'unmet':400})
   self.assertEqual(read('07_decision.json'),{'status':'SHORTFALL','unmet_liters':400})
 def test_03_altered_output(self):
  a=(ROOT/'run1'/'04_allocations.json').read_bytes(); mutated=a.replace(b'500',b'501',1);self.assertNotEqual(a,mutated);self.assertNotEqual(hashlib.sha256(a).digest(),hashlib.sha256(mutated).digest())
 def test_04_altered_input(self):
  x=copy.deepcopy(self.x);x['supply']=1099;self.assertNotEqual(demo.canon(x),INPUT.read_bytes());self.assertNotEqual(demo.generate(x)[3],demo.generate(self.x)[3])
 def test_05_zero_budget(self):
  x=copy.deepcopy(self.x);x['supply']=100;self.assertEqual([a['liters'] for a in demo.generate(x)[3]],[0,0,0])
 def test_06_exact_demand(self):
  x=copy.deepcopy(self.x);x['supply']=1500;out=demo.generate(x);self.assertEqual(out[6],{'status':'SATISFIED','unmet_liters':0});self.assertEqual(out[5]['remaining'],0)
 def test_07_bad_inputs(self):
  variations=[]
  x=copy.deepcopy(self.x);x['supply']=True;variations.append(x)
  x=copy.deepcopy(self.x);x['reserve']=1101;variations.append(x)
  x=copy.deepcopy(self.x);x['sites'][0]['demand']=-1;variations.append(x)
  x=copy.deepcopy(self.x);x['sites'][0]['id']=x['sites'][1]['id'];variations.append(x)
  x=copy.deepcopy(self.x);x['sites'][0]['priority']=x['sites'][1]['priority'];variations.append(x)
  for x in variations:
   with self.subTest(x=x):
    with self.assertRaises(ValueError):demo.generate(x)
if __name__=='__main__':unittest.main(verbosity=2)
