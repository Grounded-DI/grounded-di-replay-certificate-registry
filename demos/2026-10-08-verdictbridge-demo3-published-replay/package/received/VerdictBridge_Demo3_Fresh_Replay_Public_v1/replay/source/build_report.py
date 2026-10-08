#!/usr/bin/env python3
"""Operator review PDF; requires ReportLab only for report authoring."""
import json, hashlib
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[1]
v=json.loads((ROOT/'verification/verification-final.json').read_text())
ref=json.loads((ROOT/'original-reference/provenance.json').read_text())
case=json.loads((ROOT/'valid-case/01_canonical_input.json').read_text())
facts={x['id']:x['text'] for x in case['facts']};laws={x['id']:x for x in case['controlling_law']}
acceptance=json.loads((ROOT/'verification/acceptance-results.json').read_text())
blue=colors.HexColor('#14395B');teal=colors.HexColor('#087A69');light=colors.HexColor('#EFF4F8')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyX',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=9,textColor=blue))
styles.add(ParagraphStyle(name='SmallX',fontName='Helvetica',fontSize=8.7,leading=12,spaceAfter=7,textColor=blue))
styles.add(ParagraphStyle(name='TitleX',fontName='Helvetica-Bold',fontSize=24,leading=29,spaceAfter=18,textColor=blue))
styles.add(ParagraphStyle(name='HeadX',fontName='Helvetica-Bold',fontSize=17,leading=21,spaceAfter=13,textColor=blue))
styles.add(ParagraphStyle(name='SubX',fontName='Helvetica-Bold',fontSize=11,leading=15,spaceBefore=7,spaceAfter=6,textColor=teal))
styles.add(ParagraphStyle(name='HashX',fontName='Courier',fontSize=8.2,leading=11,spaceAfter=4,textColor=blue))

def plain(s):return str(s).replace('’',"'").replace('“','"').replace('”','"').replace('–','-').replace('—','-')
def p(s,style='BodyX'):return Paragraph(escape(plain(s)),styles[style])
story=[]
def add(s,style='BodyX'):story.append(p(s,style))
def page(title):
    if story:story.append(PageBreak())
    add(title,'HeadX')
def table(rows,widths,header=True):
    data=[[p(x,'SmallX') for x in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),5),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#CBD6DF'))]
    if header:commands += [('BACKGROUND',(0,0),(-1,0),light)]
    t.setStyle(TableStyle(commands));story.append(t);story.append(Spacer(1,10))

add('VERDICTBRIDGE / DEMO 3','SubX')
add('Selective legal outcome replay','TitleX')
add('Five-hash byte reproducibility | Operator review | October 5, 2026','SmallX')
add('DISPOSITION: '+v['status'],'HeadX')
add('Case: Lane v. Apex Industrial Tools, Inc.\nVB-DEMO-0001-PUNITIVE-CONTROL')
add('Mission','SubX')
add('Remove the documented punitive-damages motive while preserving liability and compensatory evidence. Test the declared selective result in three fresh executions, compare all five canonical artifacts, and refuse an inadmissible-hearsay rescue attempt.')
table([['Measured property','Result'],['Selective legal result','Granted in part and denied in part; punitive damages dismissed at summary judgment.'],['Three-run five-hash / direct-byte match','PASS - all five layers, all three runs.'],['Invalid hearsay control','REFUSED - VerdictReady NO; export false; zero opens and zero bytes.'],['Preserved original reference files','PASS - all five hashes independently checked.']],[205,299])
add('Production context: Grounded DI OS via FastPath 6.1 Sol - Medium (operator-provided). Computation uses the included local Python evaluator; provider metadata is not attested.','SmallX')
add('Implementation scope','SubX')
add('A newly implemented evaluator, operating on the same closed-world benchmark structure, produced the declared selective legal result reproducibly across three executions and correctly refused the inadmissible-hearsay control.')
add('Original Verdictbridge_demo-2 is reference evidence only. No original engine or native VerdictBridge implementation was executed. Public evidence release of local executions.','SmallX')

page('1 / Exact factual change')
add('All 20 stipulated authorities, questions, procedural posture, and other facts remain unchanged. The new case ID and declared expected outcomes are encoded before execution. F038 and F039 are exact restatements; only F037 and F040 have changed fact text.')
for i in ['F037','F038','F039','F040']:
    add(i,'SubX');add(facts[i])
add('Preserved engineering recommendation','SubX')
for i in ['F035','F036']:add(i+': '+facts[i])
add('Preserved exclusion','SubX')
add('F051-F054 remain unchanged. Sam Reed lacked personal knowledge; his statement is inadmissible and may not support any element or damages finding. No substitute punitive evidence was added.')
add('Verification','SubX')
add('The separate verifier compares the complete variant with an independently specified allowed transformation of the hash-pinned reference input. It checks every unaffected fact and controlling rule, rather than trusting a stored PASS label.')

page('2 / Controlling closed-world rules')
for i in ['L007','L010','L015']:
    add(i+' / '+laws[i]['title'],'SubX');add(laws[i]['text'])
add('L001 / L008 / L018 - summary judgment and experts','SubX')
add('Admissible substantial-factor testimony supports submission to a jury. Competing admissible expert opinions remain a factual dispute; the evaluator does not weigh credibility or treat the dispute as a contradiction.')
add('L017 / L020 - instructions, readiness, and export','SubX')
add('Every surviving jury issue must map to the stipulated instructions. VerdictReady requires admissible relied-upon evidence, correct law and element mapping, supported damages, replay validation, no hard lock, and authorized export. Correctly granting punitive summary judgment is not a gate failure.')
add('Exact-case operationalization','SubX')
add('The original explicit cost-motive statement supplies the stipulated L010 predicate. In the altered record, no affirmative motive or substitute conscious-disregard evidence is supplied. Knowing rejection still supports negligence under L007; this evaluator does not infer an unstated punitive motive from it alone.')
add('L019 confines this synthetic benchmark to its supplied authorities. No actual-jurisdiction legal conclusions or outside authority validation are asserted.','SmallX')

page('3 / Expected and observed selectivity')
add('Each of the three measured runs matches the declared expected result. Exactly two disposition fields changed relative to the preserved original gate matrix.')
labels={'strict_liability_failure_to_warn':'Strict liability','negligence':'Negligence','compensatory_damages':'Compensatory damages','punitive_damages':'Punitive damages','overall_motion_result':'Overall motion','sam_reed_statement':'Sam Reed','jury_instruction_coverage':'Jury instructions','appellate_record_review':'Appellate review','filingready':'FilingReady','verdictready':'VerdictReady','export_authorized':'Export authorized'}
short={'DENY_SUMMARY_JUDGMENT':'Deny summary judgment','GRANT_SUMMARY_JUDGMENT':'Grant summary judgment','GRANTED_IN_PART_DENIED_IN_PART':'Granted in part / denied in part','EXCLUDED_AND_NOT_USED':'Excluded and not used','NOT_APPLICABLE':'Not applicable'}
rows=[['Disposition','Original reference','New - observed A/B/C']]
for x in v['selectivity']:rows.append([labels[x['field']],short.get(x['original'],str(x['original'])),short.get(x['new'],str(x['new']))])
table(rows,[128,178,198])
add('Surviving jury instructions','SubX')
for issue,codes in v['observed_disposition'].items():pass
matrix=json.loads((ROOT/'Run-A/03_gate_matrix.json').read_text())
add('; '.join(k.replace('_',' ')+': '+', '.join(c) for k,c in matrix['instruction_mapping'].items()),'SmallX')
add('MI-PUN-101 is not required because punitive damages does not survive for jury determination. All 14 declared major gate statuses match; LEGAL-KERNEL is NOT_ACTIVE and appellate review is NOT_APPLICABLE.','SmallX')

page('4 / Complete five-hash ledger')
add('All three runs were created by separate processes from the same frozen input. These are the complete measured SHA-256 values; none is truncated.','SmallX')
names=['Canonical input JSON','Normalized record CSV','Gate matrix JSON','Assessment TXT','Canonical run ZIP']
keys=['canonical_input_sha256','normalized_record_sha256','gate_matrix_sha256','assessment_sha256','zip_sha256']
for title,key in zip(names,keys):
    add(title,'SubX')
    for run in v['runs']:
        add(run['folder']+': '+run['hashes'][key],'HashX')
story.append(Spacer(1,12))
table([['Artifact','Direct bytes A=B=C','Hashes A=B=C']]+[[names[i],'PASS / 0 mismatches','PASS'] for i in range(5)],[204,150,150])
add('Canonical ZIP: four records only; ZIP_STORED; lexicographic order; fixed 1980 timestamps and 0644 regular-file mode; no receipts, comments, or extra fields. Run receipts with process IDs and timestamps are outside it.','SmallX')

page('5 / Invalid hearsay control and refusal')
add('The candidate attempts to preserve punitive damages by relying on F051: "I heard Apex always knew the machine was dangerous." It changes punitive damages back to DENY_SUMMARY_JUDGMENT and the overall motion back to DENIED.')
add('Separate verifier','SubX')
add('REFUSED, exit code 2. Failure: INADMISSIBLE_EVIDENCE_RELIANCE. Controlling exclusion: L015 / F051-F054 / L020. Failed evidentiary/readiness/export path: VB-D-EAUR, VERDICTREADY-GATE, EXPORT-GATE.')
add('Actual local export boundary','SubX')
add('The writer independently refuses inadmissible evidence reliance and a legal-disposition mismatch. It creates an isolated directory for inventory but never reaches its export-file opening branch.')
table([['Observed field','Measured value'],['VerdictReady','NO'],['Export authorized','false'],['Export files opened','0'],['Bytes written','0'],['Final export output inventory','[] - empty'],['Independent Python open-event audit','[] - no export-path opens']],[254,250])
add('Additional controls','SubX')
add('Seven altered-copy tests were rejected: modified reference law, restored cost fact, wrong disposition, Reed in the reliance trace, missing assessment, forged receipt hash, and changed ZIP bytes. A forged wrong-disposition candidate without Reed was also refused at the writer.')
add('Changing the expected-outcome oracle did not change the evaluator\'s derived decision. Original reference outcomes were recalculated by the new evaluator for comparison, without executing an original engine.','SmallX')

page('6 / Preserved reference evidence')
add('A / Original five files','SubX')
add('Repository: Grounded-DI/grounded-di-replay-certificate-registry. Folder: Verdictbridge_demo-2. All five complete files are copied unchanged and hash-checked.','SmallX')
add('Pinned commit: '+ref['commit'],'HashX')
for name,h in sorted(ref['files'].items()):
    add(name,'SmallX');add(h,'HashX');story.append(Spacer(1,5))
add('B / Newly implemented evaluator','SubX')
add('source/evaluator.py - finite exact-case semantics, computed dispositions, deterministic record generation, and an isolated cooperative writer. It is not the original VerdictBridge engine.','SmallX')
add(hashlib.sha256((ROOT/'source/evaluator.py').read_bytes()).hexdigest(),'HashX')
add('C / Separate verifier','SubX')
add('source/verify.py - imports no evaluator code; checks facts, authorities, decisions, exclusion, gates, instructions, receipts, ZIP content, hashes, and direct bytes. Authored in the same task; no external certification.','SmallX')
add(hashlib.sha256((ROOT/'source/verify.py').read_bytes()).hexdigest(),'HashX')
add('D / Actual measured executions','SubX')
add('Distinct process IDs: '+', '.join(str(r['pid']) for r in v['runs'])+'. Each run receipt binds its source/input hashes and preserves actual export activity.','SmallX')

page('7 / Final disposition and practical limits')
add('PASS - all required measured conditions satisfied','HeadX')
add('The altered legal result matches the declaration. Punitive damages alone changes among the four requested claim outcomes; the overall motion changes accordingly. Unrelated outcomes remain stable. Sam Reed remains excluded, the invalid control is refused, and all five canonical layers match by both direct bytes and SHA-256 across the three fresh runs.')
add('Scope and limitations','SubX')
for item in [
 'This is a newly implemented local evaluator for one stipulated synthetic case and its exact allowed variant. It is not native VerdictBridge reproduction or execution of an original engine.',
 'The verifier is a separate internal logic path, authored in the same task. The certificate is unsigned and locally issued; no external auditor attestation occurred.',
 'No model calls, live organizational approval service, real court filing, external facts, or actual-jurisdiction legal validation were used.',
 'The writer boundary covers this cooperative local harness. It does not intercept other writers or establish hostile-process resistance, application-wide enforcement, or production readiness.',
 'Matching finite executions establish repeatability of these canonical records and this pipeline. They do not prove universal model determinism or mathematical certainty about every future execution.',
 'The reported numeric error of zero denotes unchanged exact record values. Six-decimal gate coverage values describe stipulated-record conformance, not calibrated legal confidence.'
]:add(item,'SmallX')
add('Reproduce and inspect','SubX')
add('python3 -B source/verify.py','HashX');add('python3 -B source/acceptance.py','HashX');add('python3 -B source/reproduce.py /path/to/new/folder','HashX');add('shasum -a 256 -c SHA256SUMS.txt','HashX')
add('The complete package includes source, preserved references, all three run folders and receipts, invalid-control evidence, measured verification, this PDF, README, unsigned replay certificate, and checksum manifest. This public release preserves local execution evidence.','SmallX')

def footer(c,doc):
    c.setStrokeColor(colors.HexColor('#CCD8E2'));c.line(54,43,558,43)
    c.setFont('Helvetica',8);c.setFillColor(blue);c.drawString(54,29,'Grounded DI LLC | New local evaluator | Closed-world evidence')
    c.drawRightString(558,29,'Page '+str(doc.page))

class StableCanvas(canvas.Canvas):
    def __init__(self,*args,**kwargs):kwargs['invariant']=1;super().__init__(*args,**kwargs)

doc=SimpleDocTemplate(str(ROOT/'VerdictBridge_Demo3_Report.pdf'),pagesize=(612,792),
    rightMargin=54,leftMargin=54,topMargin=48,bottomMargin=58,
    title='VerdictBridge Demo 3 - Selective Legal Outcome Replay',author='Grounded DI LLC / Mark S. Weinstein')
doc.build(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=StableCanvas)
print('Created '+str(ROOT/'VerdictBridge_Demo3_Report.pdf'))
