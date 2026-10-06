"""Author-owned unit/control tests; no model trials and no candidate code execution."""
from pathlib import Path
import importlib.util,json,tempfile,copy,os,hashlib
P=Path(__file__).resolve().parent
CASE=P.parent.name
spec=importlib.util.spec_from_file_location('author_grader',P/'grade.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
exp=json.loads((P/'expected.json').read_text());cfg=json.loads((P/'controls/mutations.json').read_text())
key='claims' if CASE=='R1' else 'actions';idkey='claim_id' if CASE=='R1' else 'action_id'
jn=g.JSON_FILE;tn=g.TEXT_FILE
prose=(P/'reference'/tn).read_text()
records=[]
def emit(root,data=exp,text=prose):
 root.mkdir(parents=True,exist_ok=True);(root/jn).write_text(json.dumps(data,indent=2)+'\n');(root/tn).write_text(text)
def check(name,condition,details=None):
 assert condition,name
 records.append({'test':name,'passed':True,**({'details':details} if details else {})})
def objective_ok(result):return result['objective']=={'passed':11,'failed':0,'total':11}
with tempfile.TemporaryDirectory(prefix=CASE+'_author_controls_') as tmp:
 t=Path(tmp)
 ref=g.grade(P/'reference')
 check('reference_objective_only',objective_ok(ref) and ref['semantic']['unknown']==3)
 for c in cfg['objective_controls']:
  data=copy.deepcopy(exp)
  for op in c['mutations']:
   if op['op']=='drop_row':data[key]=[r for r in data[key] if r[idkey]!=op['id']]
   elif op['op']=='set_row':next(r for r in data[key] if r[idkey]==op['id'])[op['field']]=op['value']
   elif op['op']=='set_path':
    dest=data
    for k in op['path'][:-1]:dest=dest[k]
    dest[op['path'][-1]]=op['value']
  root=t/c['name'];emit(root,data);result=g.grade(root)
  check(c['name'],all(result['checks'][cid]['status']=='fail' for cid in c['expected_objective_failures_include']) and result['semantic']['unknown']==3,{'detected':c['expected_objective_failures_include']})
 # Correct output must be order-insensitive and allow extra useful fields.
 data=copy.deepcopy(exp);data[key].reverse();data['extra_context']='Equivalent output ordering is allowed';data['totals']['additional_note']='Optional explanatory total field'
 for row in data[key]:row['evidence_ids'].reverse();row['extra_note']='Optional field'
 if CASE=='R1':data['totals']['unvalued_holds'][0]['original_amount']='24.0'
 else:next(r for r in data[key] if r[idkey]=='A25')['dependencies'].reverse()
 root=t/'equivalent';emit(root,data);check('equivalent_order_and_additional_fields',objective_ok(g.grade(root)))
 # Semantic controls cannot become a pass through the objective evaluator.
 root=t/'false_prose';emit(root,exp,cfg['semantic_controls'][0]['replace_prose']);rr=g.grade(root)
 check('false_prose_semantics_remain_unknown',objective_ok(rr) and rr['semantic']['unknown']==3)
 # Missing, malformed, oversized, and linked artifacts fail boundedly.
 root=t/'missing';root.mkdir();check('missing_artifacts',g.grade(root)['objective']['failed']==11)
 root=t/'duplicate_keys';emit(root);(root/jn).write_text('{"totals":{},"totals":{}}');check('duplicate_json_keys',g.grade(root)['objective']['failed']==11)
 root=t/'oversized';emit(root);(root/jn).write_text(' '*(g.MAX_JSON+1));check('oversized_json',g.grade(root)['objective']['failed']==11)
 root=t/'oversized_prose';emit(root);(root/tn).write_text('x'*(g.MAX_TEXT+1));check('oversized_prose',g.grade(root)['objective']['failed']==11)
 root=t/'file_symlink';emit(root);(root/jn).unlink();(root/jn).symlink_to(P/'reference'/jn);check('artifact_symlink',g.grade(root)['objective']['failed']==11)
 root=t/'dir_symlink';root.symlink_to(P/'reference',target_is_directory=True);check('directory_symlink',g.grade(root)['objective']['failed']==11)
 root=t/'hardlink';emit(root);target=t/'hardlink_target';target.write_text((root/jn).read_text());(root/jn).unlink();os.link(target,root/jn);check('artifact_hardlink',g.grade(root)['objective']['failed']==11)
 root=t/'fifo';emit(root);(root/jn).unlink();os.mkfifo(root/jn);check('fifo_rejected_without_blocking',g.grade(root)['objective']['failed']==11)
 root=t/'nonfinite';emit(root);(root/jn).write_text('{"bad":NaN}');check('nonfinite_json',g.grade(root)['objective']['failed']==11)
 root=t/'executable_ignored';emit(root);sentinel=t/'MUST_NOT_EXIST';(root/'submission.py').write_text('from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("executed")\n');check('submitted_code_never_executed',objective_ok(g.grade(root)) and not sentinel.exists())
 # Plumbing simulations below are not AI judgments and cannot validate prose.
 root=t/'reviewed';emit(root);base=g.grade(root);rd=t/'reviews';rd.mkdir()
 def review(who,vote='pass',hashes=None):return {'case_id':CASE,'reviewer_id':who,'condition_masked':True,'independent':True,'artifact_sha256':hashes or base['artifact_sha256'],'checks':{CASE+'-'+str(n):{'status':vote,'rationale':'SIMULATED PLUMBING TEST ONLY, not a semantic review'} for n in (12,13,14)}}
 (rd/'review_1.json').write_text(json.dumps(review('test-a')))
 check('one_review_remains_unknown',g.grade(root,rd)['semantic']['unknown']==3)
 (rd/'review_2.json').write_text(json.dumps(review('test-a')))
 check('same_reviewer_rejected',g.grade(root,rd)['semantic']['unknown']==3)
 (rd/'review_2.json').write_text(json.dumps(review('test-b',hashes={'wrong':'artifact'})))
 check('review_hash_mismatch_rejected',g.grade(root,rd)['semantic']['unknown']==3)
 (rd/'review_2.json').write_text(json.dumps(review('test-b','fail')))
 check('review_disagreement_stays_unknown',g.grade(root,rd)['semantic']['unknown']==3)
 (rd/'review_2.json').write_text(json.dumps(review('test-b')))
 check('two_matching_reviews_plumbing',g.grade(root,rd)['semantic']['passed']==3)
 (root/tn).write_text(prose+'\nChanged after review.\n')
 check('post_review_mutation_invalidates_review',g.grade(root,rd)['semantic']['unknown']==3)
 # Independent numeric handchecks, apart from the grader comparison.
 if CASE=='R1':
  by={r['claim_id']:r for r in exp['claims']}
  expected_pay=[4850,6000,2500,5720,40680,5800,0,8000,7200,39520,1875,3000,9100,4318,6882,840,0,0,4900,0,12000,0,6300,2500,0,0,19800,0,22480,0]
  check('independent_30_line_reimbursement_vector',[by['C%03d'%n]['reimbursement_usd_cents'] for n in range(1,31)]==expected_pay)
  check('independent_money_total',sum(expected_pay)==214265 and exp['totals']['approved_usd_cents']==222165 and exp['totals']['excluded_usd_cents']==8720 and exp['totals']['held_usd_cents']==25290 and exp['totals']['credit_usd_cents']==18800)
 else:
  from datetime import date
  active=[r for r in exp['actions'] if r['status'] not in ('done','cancelled')]
  overdue={r['action_id'] for r in active if r['due_date'] and date.fromisoformat(r['due_date'])<date(2026,9,30)}
  check('independent_overdue_arithmetic',overdue=={'A03','A11','A12','A21'})
  check('independent_action_counts',len(active)==18 and len(exp['actions'])==34)
report={'case_id':CASE,'test_type':'author-owned unit and deliberately defective-control calibration; not model trials','tests_passed':len(records),'tests':records,'semantic_content_validation':'NOT PERFORMED: genuine semantic judgments remain unknown until two independent masked AI reviews','objective_controls':len(cfg['objective_controls']),'semantic_controls_authored':len(cfg['semantic_controls']),'reference_objective_result':ref}
(P/'author_test_results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('case_id','tests_passed','objective_controls','semantic_controls_authored','semantic_content_validation')},indent=2))
