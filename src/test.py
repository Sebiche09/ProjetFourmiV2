from io import StringIO
import sys
import unittest
from simulation.colony import AntColony

class TestAntColony(unittest.TestCase):
    def setUp(self):
        self.ant_colony = AntColony()

    def test_simulate_time_passing_one_ant(self):
        # Test 1
        self.ant_colony.simulate_time_passing(1)
        ant_count = self.ant_colony.get_ant_count()
        expected_min = 0
        expected_max = 10
        self.assertAlmostEqual(ant_count, expected_min, delta=expected_max)

    def test_simulate_time_passing_five_ant(self):
        # Test 2
        self.ant_colony.simulate_time_passing(5)
        ant_count = self.ant_colony.get_ant_count()
        expected_min = 0
        expected_max = 50
        self.assertAlmostEqual(ant_count, expected_min, delta=expected_max)

    def test_simulate_time_passing_one_larva(self):
        # Test 1
        self.ant_colony.simulate_time_passing(1)
        ant_count = self.ant_colony.get_ant_count()
        expected_min = 0
        expected_max = 10
        self.assertAlmostEqual(ant_count, expected_min, delta=expected_max)

    def test_simulate_time_passing_five_larva(self):
        # Test 1
        self.ant_colony.simulate_time_passing(1)
        larva_count = self.ant_colony.get_larva_count()
        expected_min = 0
        expected_max = 10
        self.assertAlmostEqual(larva_count, expected_min, delta=expected_max)



if name == 'main':
    unittest.main()
