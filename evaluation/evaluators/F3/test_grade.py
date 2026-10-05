#!/usr/bin/env python3
import copy
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import grade

HERE=pathlib.Path(__file__).resolve().parent
PACKET=HERE.parents[1]/'cases/F3'

class F3Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=pathlib.Path(self.temp.name)
        self.sub=self.root/'submission';self.sub.mkdir()
        self.ref=grade.read_json(HERE/'reference/options.json')
    def tearDown(self):
        self.temp.cleanup()
    def save(self,d=None,prose=None):
        d=self.ref if d is None else d
        (self.sub/'options.json').write_text(json.dumps(d,indent=2)+'\n')
        (self.sub/'explanation.txt').write_text(grade.receipt(d) if prose is None else prose)
        return grade.grade(PACKET,self.sub)
    def flags(self,r):
        return {g['id']:g['passed'] for g in r['groups']}
    def move(self,d,index,start):
        people,*_=grade.load_inputs(PACKET)
        s=grade.stamp(start);e=s+2700;o=d['options'][index]
        o['start_utc']=grade.utc(s);o['end_utc']=grade.utc(e)
        o['local_times']={p:{'start':grade.local_at(s,people[p]),'end':grade.local_at(e,people[p])} for p in sorted(people)}
    def test_reference_and_individually_isolated_controls(self):
        expected=grade.read_json(HERE/'controls/expected-results.json')
        for name,want in expected.items():
            with self.subTest(control=name):
                path=HERE/'reference' if name=='reference' else HERE/'controls'/name
                report=grade.grade(PACKET,path)
                self.assertEqual(self.flags(report),want['groups'])
                self.assertEqual(report['integrity']['passed'],want['integrity'])
                self.assertEqual(report['accepted'],want['accepted'])
    def test_frozen_integer_arithmetic_full_horizon(self):
        key=grade.read_json(HERE/'oracle.json')
        self.assertEqual(grade.arithmetic_starts(PACKET),key['all_verified_starts'])
        self.assertEqual(key['all_verified_starts'][:5],key['expected_starts'])
        self.assertEqual(len(key['all_verified_starts']),11)
    def test_independent_manual_endpoint_key(self):
        key=grade.read_json(HERE/'oracle.json')
        self.assertEqual(self.ref['options'],key['expected_options'])
        self.assertEqual(self.ref['options'][0]['local_times']['P1']['start'],'2026-10-30T10:00:00-04:00')
        self.assertEqual(self.ref['options'][2]['local_times']['P1']['start'],'2026-11-01T09:45:00-05:00')
        self.assertTrue(self.save()['accepted'])
    def test_gap_calculation_and_closed_packet_manifest(self):
        _,windows,_,coverage=grade.load_inputs(PACKET)
        self.assertEqual(grade.calculated_gaps(windows,coverage),grade.read_json(HERE/'oracle.json')['coverage_gaps'])
        manifest=grade.read_json(PACKET/'input-manifest.json')
        self.assertEqual({r['path'] for r in manifest['sources']},{'inputs/participants.json','inputs/busy.csv','inputs/coverage.csv'})
        for row in manifest['sources']:
            self.assertEqual((PACKET/row['path']).stat().st_size,row['bytes'])
            self.assertEqual(grade.hashlib.sha256((PACKET/row['path']).read_bytes()).hexdigest(),row['sha256'])
    def test_touching_busy_rows_union_and_exact_singleton_fit(self):
        _,windows,busy,_=grade.load_inputs(PACKET)
        merged=grade.merge(busy['P1'])
        self.assertIn((grade.stamp('2026-10-30T12:30:00Z'),grade.stamp('2026-10-30T13:45:00Z')),merged)
        a=grade.stamp('2026-10-30T13:45:00Z');b=grade.stamp('2026-10-30T15:00:00Z')
        self.assertFalse(grade.overlaps(a,b,busy['P1']))
        self.assertFalse(grade.overlaps(a,b,busy['P2']))
        self.assertTrue(self.save()['accepted'])
    def test_exact_work_end_boundary_and_overlapping_options_allowed(self):
        _,windows,_,_=grade.load_inputs(PACKET)
        o=self.ref['options'][1]
        self.assertTrue(grade.contained(grade.stamp(o['start_utc'])-900,grade.stamp(o['end_utc'])+900,windows['P1']))
        self.assertEqual(grade.stamp(o['end_utc'])+900,grade.stamp('2026-10-30T16:30:00Z'))
        self.assertLess(grade.stamp(self.ref['options'][4]['start_utc']),grade.stamp(self.ref['options'][3]['end_utc']))
        self.assertTrue(self.save()['accepted'])
    def test_busy_buffer_violation_rejected(self):
        d=copy.deepcopy(self.ref);self.move(d,0,'2026-10-30T13:45:00Z')
        self.assertFalse(self.flags(self.save(d))['g2'])
    def test_grid_violation_rejected_even_when_physically_free(self):
        d=copy.deepcopy(self.ref);self.move(d,3,'2026-11-01T16:20:00Z')
        r=self.save(d)
        self.assertFalse(self.flags(r)['g2'])
        failures=[a['id'] for g in r['groups'] if g['id']=='g2' for a in g['assertions'] if not a['passed']]
        self.assertEqual(failures,['option-4-utc-grid'])
    def test_prebuffer_must_fit_working_hours(self):
        d=copy.deepcopy(self.ref);self.move(d,4,'2026-11-02T13:30:00Z')
        self.assertFalse(self.flags(self.save(d))['g2'])
    def test_postbuffer_must_fit_working_hours(self):
        d=copy.deepcopy(self.ref);self.move(d,4,'2026-11-01T16:45:00Z')
        self.assertFalse(self.flags(self.save(d))['g2'])
    def test_unknown_is_not_free(self):
        d=copy.deepcopy(self.ref);self.move(d,0,'2026-10-31T14:15:00Z')
        flags=self.flags(self.save(d))
        self.assertTrue(flags['g1']);self.assertTrue(flags['g2']);self.assertFalse(flags['g4'])
    def test_double_buffering_cannot_delete_requested_boundary_starts(self):
        d=copy.deepcopy(self.ref);d['options']=[]
        flags=self.flags(self.save(d))
        self.assertFalse(flags['g1']);self.assertFalse(flags['g2']);self.assertFalse(flags['g3'])
    def test_duplicate_option_rejected(self):
        d=copy.deepcopy(self.ref);d['options'][4]=copy.deepcopy(d['options'][3]);d['options'][4]['rank']=5
        self.assertFalse(self.flags(self.save(d))['g3'])
    def test_booleans_are_not_integer_ranks_or_duration(self):
        d=copy.deepcopy(self.ref);d['options'][0]['rank']=True
        self.assertFalse(self.flags(self.save(d))['g3'])
        d=copy.deepcopy(self.ref);d['meeting_duration_minutes']=45.0
        self.assertFalse(self.flags(self.save(d))['g2'])
    def test_bad_display_date_and_missing_participant_rejected(self):
        d=copy.deepcopy(self.ref);d['options'][0]['local_times']['P3']['start']='2026-10-31T17:00:00+03:00'
        self.assertFalse(self.flags(self.save(d))['g1'])
        del d['options'][0]['local_times']['P3']
        self.assertFalse(self.flags(self.save(d))['g5'])
    def test_stale_prose_rejected(self):
        d=copy.deepcopy(self.ref);self.move(d,4,'2026-11-02T13:45:00Z')
        self.assertFalse(self.flags(self.save(d,grade.receipt(self.ref)))['g5'])
    def test_final_newline_is_optional(self):
        self.assertTrue(self.save(prose=grade.receipt(self.ref).rstrip('\n'))['accepted'])
    def test_unrequested_json_field_rejected(self):
        d=copy.deepcopy(self.ref);d['scheduled']=False
        self.assertFalse(self.flags(self.save(d))['g5'])
    def test_integrity_gate_detects_source_task_and_manifest_edits(self):
        for rel in ['inputs/busy.csv','task.txt','input-manifest.json']:
            with self.subTest(path=rel):
                packet=self.root/'packet'
                if packet.exists(): shutil.rmtree(packet)
                shutil.copytree(PACKET,packet)
                with (packet/rel).open('a') as f:f.write('\n')
                r=grade.grade(packet,HERE/'reference')
                self.assertFalse(r['integrity']['passed']);self.assertFalse(r['accepted'])
    def test_missing_artifact_invalid_json_and_duplicate_keys_fail_safely(self):
        self.assertFalse(grade.grade(PACKET,self.sub)['accepted'])
        self.save()
        for payload in ['{','{"options":[],"options":[]}','{"options":[],"x":NaN}']:
            (self.sub/'options.json').write_text(payload)
            r=grade.grade(PACKET,self.sub)
            self.assertFalse(r['accepted']);self.assertEqual(r['quality']['passed_groups'],0)
    def test_bad_option_object_never_crashes(self):
        for bad in [None,[],True,'value',{'start_utc':'tomorrow'}]:
            d=copy.deepcopy(self.ref);d['options'][0]=bad
            (self.sub/'options.json').write_text(json.dumps(d))
            (self.sub/'explanation.txt').write_text('Incomplete\n')
            self.assertFalse(grade.grade(PACKET,self.sub)['accepted'])
    def test_common_cli_and_report_shape(self):
        out=self.root/'report.json'
        result=subprocess.run([sys.executable,str(HERE/'grade.py'),'--packet',str(PACKET),'--submission',str(HERE/'reference'),'--out',str(out)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        r=grade.read_json(out)
        self.assertEqual(set(r),{'case_id','integrity','groups','accepted','quality'})
        self.assertEqual([g['id'] for g in r['groups']],['g1','g2','g3','g4','g5'])
        self.assertEqual(r['quality'],{'passed_groups':5,'scored_groups':5,'total_groups':5})
        self.assertTrue(all(type(g['passed']) is bool for g in r['groups']))
        self.assertTrue(all(g['assertions'] for g in r['groups']))

if __name__=='__main__':
    unittest.main(verbosity=2)
