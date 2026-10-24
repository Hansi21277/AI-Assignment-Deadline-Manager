import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import tools

class TestTools(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = patch.object(tools,'DATA_FILE',Path(self.tmp.name)/'data.json')
        self.patch.start()
    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()
    def test_add_and_list(self):
        item = tools.add_assignment('Report','2099-01-01','high',3)
        self.assertEqual(item['id'],1)
        self.assertEqual(len(tools.list_assignments()),1)
    def test_invalid_date(self):
        with self.assertRaises(ValueError): tools.add_assignment('Bad','tomorrow')
    def test_update(self):
        item = tools.add_assignment('Report','2099-01-01')
        self.assertEqual(tools.update_status(item['id'],'completed')['status'],'completed')
    def test_plan(self):
        tools.add_assignment('Report','2099-01-01',estimated_hours=3)
        plan = tools.create_study_plan(2,2)
        self.assertEqual(sum(s['hours'] for d in plan['plan'] for s in d['sessions']),3)
    def test_deadlines(self):
        from datetime import date
        tools.add_assignment('Today',date.today().isoformat())
        self.assertEqual(len(tools.check_deadlines(0)),1)

if __name__=='__main__': unittest.main()
