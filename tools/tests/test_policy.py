from __future__ import annotations
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ci_policy import PolicyError, kind, validate_config, validate_route, validate_body, validate_event
from verify_reports import verify_tests, verify_coverage
from competition_preflight import validate_tag_name

ROOT = Path(__file__).resolve().parents[2]
BASE = json.loads((ROOT / "config/ci-policy.json").read_text())
BASE["configured"] = True

class Configuration(unittest.TestCase):
    def test_config_valid(self): validate_config(BASE)
    def test_unconfigured_rejected(self):
        p=copy.deepcopy(BASE); p['configured']=False
        with self.assertRaises(PolicyError): validate_config(p)
    def test_cpp_rejected(self):
        p=copy.deepcopy(BASE); p['language']='cpp'
        with self.assertRaises(PolicyError): validate_config(p)
    def test_zero_minimum_rejected(self):
        p=copy.deepcopy(BASE); p['minimum_executed_tests']=0
        with self.assertRaises(PolicyError): validate_config(p)
    def test_skips_rejected(self):
        p=copy.deepcopy(BASE); p['allow_skipped_tests']=True
        with self.assertRaises(PolicyError): validate_config(p)
    def test_invalid_coverage_rejected(self):
        p=copy.deepcopy(BASE); p['minimum_line_coverage']=1.01
        with self.assertRaises(PolicyError): validate_config(p)
    def test_wrong_integration_rejected(self):
        p=copy.deepcopy(BASE); p['integration_branch']='develop'
        with self.assertRaises(PolicyError): validate_config(p)

class Branches(unittest.TestCase):
    def test_feature(self): self.assertEqual(kind('feature/swerve/field-centric',BASE),'feature')
    def test_hotfix(self): self.assertEqual(kind('hotfix/auto/fix-broken-auto',BASE),'hotfix')
    def test_release(self): self.assertEqual(kind('release/week-1-event',BASE),'release')
    def test_sync(self): self.assertEqual(kind('sync/week-1-backmerge',BASE),'sync')
    def test_uppercase_rejected(self):
        with self.assertRaises(PolicyError): kind('feature/Swerve/field-centric',BASE)
    def test_old_name_rejected(self):
        with self.assertRaises(PolicyError): kind('drive/142-heading-hold',BASE)
    def test_nested_testing_rejected(self):
        with self.assertRaises(PolicyError): kind('testing/feature/drive/hold',BASE)
    def test_unknown_subsystem_rejected(self):
        with self.assertRaises(PolicyError): kind('feature/unknown/hold',BASE)
    def test_feature_to_testing(self): validate_route('testing','feature/drive/hold',False,BASE)
    def test_feature_to_main_rejected(self):
        with self.assertRaises(PolicyError): validate_route('main','feature/drive/hold',True,BASE)
    def test_release_to_main(self): validate_route('main','release/week-1',True,BASE)
    def test_hotfix_to_main(self): validate_route('main','hotfix/drive/limit',True,BASE)
    def test_fork_release_rejected(self):
        with self.assertRaises(PolicyError): validate_route('main','release/week-1',False,BASE)
    def test_main_backmerge(self): validate_route('testing','main',True,BASE)
    def test_sync_fork_rejected(self):
        with self.assertRaises(PolicyError): validate_route('testing','sync/backmerge',False,BASE)
    def test_direct_testing_release_rejected(self):
        with self.assertRaises(PolicyError): validate_route('main','testing',True,BASE)
    def test_testing_queue(self): validate_event('merge_group',{'merge_group':{'base_ref':'refs/heads/testing'}},BASE)
    def test_main_queue_rejected(self):
        with self.assertRaises(PolicyError): validate_event('merge_group',{'merge_group':{'base_ref':'refs/heads/main'}},BASE)
    def test_placeholder_body_rejected(self):
        with self.assertRaises(PolicyError): validate_body('REPLACE_ME')
    def test_empty_body_rejected(self):
        with self.assertRaises(PolicyError): validate_body('')
    def test_full_body(self):
        from ci_policy import HEADINGS
        validate_body('\n'.join('## '+h+'\nSpecific test evidence with a substantive explanation.\n' for h in HEADINGS))

class Reports(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def xml(self,text):
        p=self.root/'report.xml'; p.write_text(text); return p
    def test_no_reports(self):
        with self.assertRaises(PolicyError): verify_tests([])
    def test_unexpected_root(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<other><testcase/></other>')])
    def test_unexpected_root(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<other><testcase/></other>')])
    def test_zero_tests(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<testsuite tests="0"/>')])
    def test_passed_tests(self):
        self.assertEqual(verify_tests([self.xml('<testsuite tests="1"><testcase name="real"/></testsuite>')]),1)
    def test_skip_element(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<testsuite><testcase><skipped/></testcase></testsuite>')])
    def test_skip_attribute(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<testsuite skipped="1"><testcase/></testsuite>')])
    def test_failure(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<testsuite><testcase><failure/></testcase></testsuite>')])
    def test_error(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<testsuite errors="1"/>')])
    def test_nested_tests_not_double_counted(self):
        self.assertEqual(verify_tests([self.xml('<testsuites><testsuite><testcase/></testsuite></testsuites>')]),1)
    def test_entity_rejected(self):
        with self.assertRaises(PolicyError): verify_tests([self.xml('<!DOCTYPE x [<!ENTITY a "a">]><testsuite><testcase/></testsuite>')])
    def coverage(self,line=80,branch=70):
        return self.xml(f'<report><counter type="LINE" covered="{line}" missed="{100-line}"/><counter type="BRANCH" covered="{branch}" missed="{100-branch}"/></report>')
    def test_coverage_boundary(self): self.assertEqual(verify_coverage(self.coverage(),.8,.7)['LINE'],.8)
    def test_low_lines(self):
        with self.assertRaises(PolicyError): verify_coverage(self.coverage(79,100),.8,.7)
    def test_low_branches(self):
        with self.assertRaises(PolicyError): verify_coverage(self.coverage(100,69),.8,.7)
    def test_missing_counter(self):
        with self.assertRaises(PolicyError): verify_coverage(self.xml('<report/>'),.8,.7)
    def test_zero_code(self):
        with self.assertRaises(PolicyError): verify_coverage(self.xml('<report><counter type="LINE" covered="0" missed="0"/></report>'),.8,.7)
    def test_jacoco_doctype(self):
        p=self.coverage();p.write_text('<!DOCTYPE report PUBLIC "-//JACOCO//DTD Report 1.1//EN" "report.dtd">'+p.read_text())
        self.assertEqual(verify_coverage(p,.8,.7)['BRANCH'],.7)

class FinalGate(unittest.TestCase):
    # Run the actual embedded stdlib-only final gate, without requiring PyYAML in CI.
    def run_gate(self, filename, job, states):
        text=(ROOT/filename).read_text().split('  '+job+':',1)[1]
        script=text.split("python3 - <<'PY'\n",1)[1].split('\n          PY',1)[0]
        import textwrap
        r=subprocess.run([sys.executable,'-c',textwrap.dedent(script)], env={**os.environ,'RESULTS':json.dumps(states)},capture_output=True,text=True)
        return r.returncode
    def test_robot_success(self):
        self.assertEqual(self.run_gate('.github/workflows/robot-ci.yml','ci-gate',{k:{'result':'success'} for k in ['repository-policy','robot-quality','secrets']}),0)
    def test_robot_failure(self):
        s={k:{'result':'success'} for k in ['repository-policy','robot-quality','secrets']};s['robot-quality']['result']='failure'
        self.assertNotEqual(self.run_gate('.github/workflows/robot-ci.yml','ci-gate',s),0)
    def test_robot_skipped(self):
        s={k:{'result':'success'} for k in ['repository-policy','robot-quality','secrets']};s['secrets']['result']='skipped'
        self.assertNotEqual(self.run_gate('.github/workflows/robot-ci.yml','ci-gate',s),0)
    def test_robot_cancelled(self):
        s={k:{'result':'success'} for k in ['repository-policy','robot-quality','secrets']};s['secrets']['result']='cancelled'
        self.assertNotEqual(self.run_gate('.github/workflows/robot-ci.yml','ci-gate',s),0)
    def test_robot_missing(self): self.assertNotEqual(self.run_gate('.github/workflows/robot-ci.yml','ci-gate',{}),0)
    def test_release_success(self): self.assertEqual(self.run_gate('.github/workflows/release-review.yml','robot-release-approval',{k:{'result':'success'} for k in ['release-policy','hardware-review']}),0)
    def test_release_skipped(self): self.assertNotEqual(self.run_gate('.github/workflows/release-review.yml','robot-release-approval',{'release-policy':{'result':'failure'},'hardware-review':{'result':'skipped'}}),0)

class Tags(unittest.TestCase):
    def test_good(self): self.assertTrue(validate_tag_name('comp/week-1-v1'))
    def test_flag_rejected(self): self.assertFalse(validate_tag_name('--all'))
    def test_other_namespace_rejected(self): self.assertFalse(validate_tag_name('release/week-1'))
    def test_uppercase_rejected(self): self.assertFalse(validate_tag_name('comp/Week-1'))

if __name__ == '__main__': unittest.main()
