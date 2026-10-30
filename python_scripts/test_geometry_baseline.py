"""Guard geometry partitioning, training-only fitting and metric definitions."""
import copy
import unittest
from baseline_geometry import evaluate, partition, score, TARGETS


class GeometryBaselineTests(unittest.TestCase):
    def setUp(self):
        self.rows = [{'Spacer_Design_Label': label, 'Case_UID': str(i),
                      TARGETS[0]: value, TARGETS[1]: value/10}
                     for i,(label,value) in enumerate([('train',1.),('train',3.),('held',5.),('held',7.)])]

    def test_exact_geometry_partition(self):
        rows = self.rows + [{'Spacer_Design_Label': 'held_extra'}]
        train,test = partition(rows,'held')
        self.assertEqual(len(test),2)
        self.assertIn('held_extra',[r['Spacer_Design_Label'] for r in train])

    def test_test_targets_do_not_change_fitted_constants(self):
        original,_ = evaluate(self.rows,'held')
        changed = copy.deepcopy(self.rows)
        for row in changed[2:]:
            for target in TARGETS:
                row[target] *= 1000
        perturbed,_ = evaluate(changed,'held')
        for target in TARGETS:
            for name in ('train_mean','train_median'):
                self.assertEqual(original['targets'][target][name]['constant'],
                                 perturbed['targets'][target][name]['constant'])

    def test_metrics(self):
        self.assertEqual(score([1.,3.],[2.,2.]),{'mae':1.,'rmse':1.,'r2':0.})
        self.assertIsNone(score([1.,1.],[1.,1.])['r2'])

    def test_empty_holdout_rejected(self):
        with self.assertRaises(ValueError):
            partition(self.rows,'missing')


if __name__ == '__main__':
    unittest.main()
