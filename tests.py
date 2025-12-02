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

    def test_ant_wander(self):
        """Ants should prefer food and avoid smells in state wander"""

        hill_cell = (1, 1)
        food_cell = (2, 1)

        my_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        my_hill = agents.Hill(
            model=my_model,
            cell=my_model.grid[hill_cell],
            spawn=ant.Ant,
        )

        my_food = agents.Food(
            model=my_model,
            cell=my_model.grid[food_cell],
        )

        my_ant = my_hill.spawn(1)[0]

        self.assertEqual(my_ant.cell, my_hill.cell)

        my_model.step()

        self.assertEqual(my_ant.cell, my_food.cell)

    def test_hill_spawn(self):
        """Hills should spawn an ant on request. Ant has default attributes"""

        hill_cell = (0, 0)

        my_model = model.Model(
            width=1,
            height=1,
            seed=1,
            players=None,
        )

        my_hill = agents.Hill(
            model=my_model,
            cell=my_model.grid[hill_cell],
            spawn=ant.Ant,
        )

        my_ant = my_hill.spawn(1)[0]

        self.assertEqual(my_ant.cell, my_hill.cell)
        self.assertEqual(my_ant.state, ant.Ant.DEFAULT_STATE)
        self.assertEqual(my_ant.storage, [])
        self.assertEqual(my_ant.history, [(0, 0)])


if __name__ == "__main__":
    unittest.main()
