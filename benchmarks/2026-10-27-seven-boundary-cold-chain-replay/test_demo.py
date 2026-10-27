import copy, hashlib, json, pathlib, unittest
import demo
DATA=json.loads(pathlib.Path(__file__).with_name('input.json').read_text())
class Tests(unittest.TestCase):
    def test_expected(self):
        o=demo.build(DATA)
        self.assertEqual([x['temp_tenths'] for x in json.loads(o['02_calibrated.json'])],[40,78,81,50])
        self.assertEqual(json.loads(o['05_events.json']),[{'minute':20,'temp_tenths':81}])
        self.assertEqual(json.loads(o['06_decision.json']),{'status':'HOLD','reasons':['TEMPERATURE']})
        self.assertEqual([g['gap_minutes'] for g in json.loads(o['04_coverage.json'])['gaps']],[10,10,10])
    def test_threshold_equality(self):
        d=copy.deepcopy(DATA); d['readings'][2]['temp_tenths']=78
        self.assertEqual(json.loads(demo.build(d)['06_decision.json']),{'status':'RELEASE','reasons':[]})
    def test_gap_hold(self):
        d=copy.deepcopy(DATA); d['readings'][2]['temp_tenths']=78; d['readings'][2]['minute']=21
        self.assertEqual(json.loads(demo.build(d)['06_decision.json'])['reasons'],['GAP'])
    def test_incomplete_coverage(self):
        d=copy.deepcopy(DATA); d['readings']=d['readings'][:2]
        self.assertEqual(json.loads(demo.build(d)['06_decision.json'])['reasons'],['COVERAGE'])
    def test_altered_input(self):
        d=copy.deepcopy(DATA); d['readings'][2]['temp_tenths']=78
        self.assertNotEqual(demo.build(DATA)['06_decision.json'],demo.build(d)['06_decision.json'])
    def test_altered_output(self):
        o=demo.build(DATA); o['06_decision.json']+=b' '
        self.assertFalse(demo.verify(o))
    def test_coherent_wrong_result(self):
        o=demo.build(DATA); o['06_decision.json']=demo.encode({'status':'RELEASE','reasons':[]}); c=json.loads(o['07_commitment.json']); c['sha256']['06_decision.json']=hashlib.sha256(o['06_decision.json']).hexdigest(); o['07_commitment.json']=demo.encode(c)
        self.assertTrue(demo.verify(o)); self.assertNotEqual(json.loads(o['06_decision.json']),{'status':'HOLD','reasons':['TEMPERATURE']})
    def test_invalid_timestamp(self):
        d=copy.deepcopy(DATA); d['readings'][1]['minute']=0
        with self.assertRaises(ValueError): demo.build(d)
if __name__=='__main__': unittest.main()
