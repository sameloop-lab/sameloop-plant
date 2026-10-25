import math
import unittest
from sameloop_plant import Plant

class ModelTests(unittest.TestCase):
    def test_off_matches_analytic_thermal_solution(self):
        p=Plant(); p.step(10,0)
        self.assertAlmostEqual(p.temperature,32+(32.4-32)*math.exp(-.015*10),places=9)
        self.assertEqual(p.applied,0)
    def test_fan_matches_exact_cascade(self):
        p=Plant();p.step(1,100)
        a,b=math.exp(-1/.6),math.exp(-1/.8)
        self.assertAlmostEqual(p.applied,100*(1-a),places=6)
        self.assertAlmostEqual(p.rpm,4000-4000*b+40*(-100)*.6/(.6-.8)*(a-b),places=5)
    def test_partition_invariance(self):
        a,b=Plant(),Plant();a.step(1,63)
        for _ in range(10):b.step(.1,63)
        for k in ['temperature','applied','rpm']:self.assertAlmostEqual(getattr(a,k),getattr(b,k),places=10)
    def test_bad_input_does_not_mutate(self):
        for kw in [{'dt':float('nan')},{'dt':-1},{'dt':61},{'dt':.1,'demand':101},{'dt':.1,'demand':True},{'dt':.1,'heat':float('inf')}]:
            p=Plant();before=p.snapshot()
            with self.assertRaises(ValueError):p.step(**kw)
            self.assertEqual(before,p.snapshot())
    def test_cooling_and_inertia(self):
        p=Plant();p.step(10,100);self.assertLess(p.temperature,25)
        rpm=p.rpm;p.step(.1,0);self.assertGreater(p.rpm,0);self.assertLess(p.rpm,rpm)
    def test_zero_step(self):
        p=Plant();self.assertEqual(p.step(0),p.snapshot())
if __name__=='__main__':unittest.main()
