import unittest
import agents
import model
import ant


class TestAgent(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_agent_spawns(self):
        # All the stuff that can be spawned
        my_model = model.Model(width=1, height=10, seed=1, players=None)
        my_ant = ant.Ant(my_model)
        my_hill = agents.Hill(my_model, cell=my_model.grid[(0, 0)])

        # Setting base attrs if needed
        my_ant.cell = my_model.grid[(0, 0)]

        self.assertEqual(my_ant.cell.coordinate, (0, 0))
        self.assertEqual(my_hill.cell.coordinate, (0, 0))

        # Testing a single step
        my_model.step()

        self.assertNotEqual(my_ant.cell.coordinate, (0, 0))
        self.assertEqual(my_hill.cell.coordinate, (0, 0))


if __name__ == "__main__":
    unittest.main()
