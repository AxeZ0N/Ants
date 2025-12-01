""" """

import unittest
import agents
import model
import ant


class TestAgent(unittest.TestCase):
    """ """

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        """ """
        pass

    def test_agent_spawns(self):
        """ """
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
        self.assertEqual(len(my_model.grid[(0, 0)].agents), 1)
        self.assertEqual(type(my_model.grid[(0, 0)].agents[0]), agents.Smell)
        self.assertEqual(my_model.grid[(0, 0)].agents[0].age, 1)

    def test_ant_trails(self):
        my_model = model.Model(width=10, height=10, seed=1)

        my_ant = ant.Ant(my_model, cell=my_model.grid[(4,4)])

        steps = [my_model.step() for _ in range(10)]
        print(my_ant.history)
        print(my_ant.cell.coordinate)

        ant.retrace_ant_steps(my_ant)



if __name__ == "__main__":
    unittest.main()
