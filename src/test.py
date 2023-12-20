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

    def test_kill_ant_by_type(self):
        self.ant_colony.simulate_time_passing(1)
        ant_count_before = self.ant_colony.get_ant_count()
        ant_type_to_kill = self.ant_colony.generated_ant_types[0]
        num_to_kill = 1
        if ant_type_to_kill in self.ant_colony.generated_ant_types:
            self.ant_colony.generated_ant_types.remove(ant_type_to_kill)
        self.ant_colony.kill_ant_by_type(ant_type_to_kill, num_to_kill)
        ant_count_after = self.ant_colony.get_ant_count()
        self.assertLess(ant_count_after, ant_count_before)


    def test_zero_time_passed(self):
        ant_count_before = self.ant_colony.get_ant_count()
        self.ant_colony.simulate_time_passing(0)
        ant_count_after = self.ant_colony.get_ant_count()
        self.assertEqual(ant_count_after, ant_count_before)

    def test_negative_time_passed(self):
        with self.assertRaises(ValueError):
            self.ant_colony.simulate_time_passing(-1)



if __name__ == 'main':
    unittest.main()
