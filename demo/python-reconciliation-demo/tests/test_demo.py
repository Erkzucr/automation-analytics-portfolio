import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]));from run_demo import reconcile
class T(unittest.TestCase):
 def test_ok(self):self.assertEqual(len(reconcile({'R':{'value_amount':'10'}},{'R':{'value_amount':'8'}},5)[0]),1)
 def test_variance(self):self.assertEqual(len(reconcile({'R':{'value_amount':'10'}},{'R':{'value_amount':'1'}},5)[1]),1)
 def test_unmatched(self):self.assertEqual(reconcile({'R':{'value_amount':'10'}},{},5)[1][0][1],'ONLY_A')
if __name__=='__main__':unittest.main()
