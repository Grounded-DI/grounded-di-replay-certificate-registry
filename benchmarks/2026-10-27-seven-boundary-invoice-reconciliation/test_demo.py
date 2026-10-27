import copy, json, pathlib, unittest
import demo

DATA=json.loads(pathlib.Path(__file__).with_name('input.json').read_text())
class Checks(unittest.TestCase):
    def test_expected(self):
        o=demo.build(DATA); d=json.loads(o['05_dispositions.json']); l=json.loads(o['06_ledger.json'])
        self.assertEqual([x['status'] for x in d],['PAY','PAY','HOLD_DUPLICATE','HOLD_LIMIT'])
        self.assertEqual([x['amount_cents'] for x in d],[3600,5000,3600,4000])
        self.assertEqual(l,{'payable_cents':8600,'held_cents':7600,'total_cents':16200})
    def test_limit_equality(self):
        self.assertEqual(json.loads(demo.build(DATA)['05_dispositions.json'])[1]['status'],'PAY')
    def test_altered_input(self):
        d=copy.deepcopy(DATA); d['invoices'][0]['unit_cents']=1300
        self.assertNotEqual(demo.build(DATA)['02_amounts.json'],demo.build(d)['02_amounts.json'])
    def test_altered_output(self):
        o=demo.build(DATA); o['05_dispositions.json']+=b' '
        self.assertFalse(demo.verify(o))
    def test_coherent_wrong_result(self):
        o=demo.build(DATA); ledger=json.loads(o['06_ledger.json']); ledger['payable_cents']=8700; o['06_ledger.json']=demo.encode(ledger)
        import hashlib
        c=json.loads(o['07_commitment.json']); c['ledger']=ledger; c['sha256']['06_ledger.json']=hashlib.sha256(o['06_ledger.json']).hexdigest(); o['07_commitment.json']=demo.encode(c)
        self.assertTrue(demo.verify(o))
        self.assertNotEqual(json.loads(o['06_ledger.json'])['payable_cents'],8600)
if __name__=='__main__': unittest.main()
