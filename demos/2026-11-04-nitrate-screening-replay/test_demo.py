import hashlib, json, pathlib, subprocess, sys, tempfile, unittest

ROOT=pathlib.Path(__file__).resolve().parent

class ScreeningTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.dir=pathlib.Path(self.temp.name)
        self.fixture=json.loads((ROOT/"fixture.json").read_text())
    def tearDown(self): self.temp.cleanup()
    def run_producer(self, data=None, source=None, config=None, raw=None):
        inp=self.dir/"input.json"
        inp.write_text(raw if raw is not None else json.dumps(data if data is not None else self.fixture))
        out=self.dir/"out.json"
        cmd=[sys.executable,str(ROOT/"producer.py"),"--input",str(inp),"--source",str(source or ROOT/"source_excerpt.txt"),"--config",str(config or ROOT/"config.json"),"--out",str(out)]
        result=subprocess.run(cmd,capture_output=True,text=True)
        return result,out,inp
    def test_below_and_equal_and_above(self):
        r,out,_=self.run_producer()
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual([x["status"] for x in json.loads(out.read_text())["results"]],["AT_OR_BELOW","AT_OR_BELOW","REVIEW_ABOVE","HOLD"])
    def test_missing_unit(self):
        del self.fixture["samples"][0]["unit"]
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(out.read_text())["results"][0]["reason"],"UNSUPPORTED_OR_MISSING_UNIT")
    def test_missing_value(self):
        del self.fixture["samples"][0]["value"]
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(out.read_text())["results"][0]["reason"],"INVALID_OR_MISSING_VALUE")
    def test_invalid_value(self):
        self.fixture["samples"][0]["value"]="NaN"
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(out.read_text())["results"][0]["reason"],"INVALID_OR_MISSING_VALUE")
    def test_changed_source_rejected(self):
        source=self.dir/"source.txt"; source.write_text("changed")
        r,out,_=self.run_producer(source=source)
        self.assertEqual(r.returncode,2); self.assertIn("SOURCE_MISMATCH",r.stderr); self.assertFalse(out.exists())
    def test_changed_source_and_pin_accepted_is_documented_limit(self):
        source=self.dir/"source.txt"; source.write_text("changed")
        config=json.loads((ROOT/"config.json").read_text())
        config["source_sha256"]=hashlib.sha256(source.read_bytes()).hexdigest()
        path=self.dir/"config.json"; path.write_text(json.dumps(config))
        r,out,_=self.run_producer(source=source,config=path)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(out.read_text())["source_sha256"],config["source_sha256"])
    def test_malformed_json_rejected(self):
        r,out,_=self.run_producer(raw="{")
        self.assertEqual(r.returncode,2); self.assertIn("INPUT_ERROR:",r.stderr); self.assertFalse(out.exists())
    def test_missing_id_rejected(self):
        del self.fixture["samples"][0]["id"]
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,2); self.assertIn("INPUT_ERROR:",r.stderr); self.assertFalse(out.exists())
    def test_duplicate_id_rejected(self):
        self.fixture["samples"][1]["id"]="S1"
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,2); self.assertIn("INPUT_ERROR:",r.stderr); self.assertFalse(out.exists())
    def test_legitimate_input_change(self):
        self.fixture["samples"][0]["value"]="11"
        r,out,_=self.run_producer(self.fixture)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(out.read_text())["results"][0]["status"],"REVIEW_ABOVE")
    def test_checker_rejects_altered_result(self):
        r,out,inp=self.run_producer()
        self.assertEqual(r.returncode,0,r.stderr)
        result=json.loads(out.read_text()); result["results"][2]["status"]="AT_OR_BELOW"; out.write_text(json.dumps(result))
        c=subprocess.run([sys.executable,str(ROOT/"checker.py"),"--input",str(inp),"--source",str(ROOT/"source_excerpt.txt"),"--config",str(ROOT/"config.json"),"--out",str(out)],capture_output=True,text=True)
        self.assertEqual(c.returncode,1); self.assertIn("RESULT_MISMATCH",c.stderr)

    def test_checker_rejects_same_category_input_substitution(self):
        r,out,inp=self.run_producer()
        self.assertEqual(r.returncode,0,r.stderr)
        changed=json.loads(inp.read_text()); changed["samples"][0]["value"]="4.3"
        inp.write_text(json.dumps(changed))
        c=subprocess.run([sys.executable,str(ROOT/"checker.py"),"--input",str(inp),"--source",str(ROOT/"source_excerpt.txt"),"--config",str(ROOT/"config.json"),"--out",str(out)],capture_output=True,text=True)
        self.assertEqual(c.returncode,1); self.assertIn("INPUT_MISMATCH",c.stderr)

if __name__=="__main__": unittest.main(verbosity=2)
