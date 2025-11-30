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
        my_model = model.Model(width=1, height=10, seed=1)
        my_ant = ant.Ant(my_model, cell=my_model.grid[(0, 0)])
        my_hill = agents.Hill(my_model, cell=my_model.grid[(0, 1)])
        my_food = agents.Food(my_model, cell=my_model.grid[(0, 2)])
        my_smell = agents.Smell(my_model, cell=my_model.grid[(0, 3)])

        self.assertEqual(my_ant.cell.coordinate, (0, 0))
        self.assertEqual(my_hill.cell.coordinate, (0, 1))
        self.assertEqual(my_food.cell.coordinate, (0, 2))
        self.assertEqual(my_smell.cell.coordinate, (0, 3))

        # Testing a single step
        my_model.step()

        self.assertNotEqual(my_ant.cell.coordinate, (0, 0))
        self.assertEqual(my_hill.cell.coordinate, (0, 1))
        self.assertEqual(my_food.cell.coordinate, (0, 2))
        self.assertEqual(my_smell.cell.coordinate, (0, 3))

        # Testing tracked attrs
        self.assertEqual(my_ant.history, [(0, 1)])

        # Assert ant lef scent behind
        self.assertEqual(len(my_model.grid[(0,0)].agents), 1)
        self.assertEqual(my_model.grid[(0,0)].agents[0].age, 1)


if __name__ == "__main__":
    unittest.main()
