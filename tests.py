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

    def test_ant_prefer_food(self):
        """Move onto food if possible"""

        ant_cell = (1, 1)
        food_cell = (2, 1)

        my_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        my_food = agents.Food(
            model=my_model,
            cell=my_model.grid[food_cell],
        )

        my_model.step()

        self.assertEqual(my_ant.cell, my_food.cell)

    def test_ant_avoid_smell(self):
        """Don't move onto smell if possible"""

        ant_cell = (1, 1)
        empty_cell = (2, 1)

        my_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        # Fill all the neighbors with smells
        for cell in my_ant.cell.get_neighborhood():
            new_smell = agents.Smell(
                model=my_model,
                cell=cell,
            )

            cell.add_agent(new_smell)

        # Remove all the agents from the cell I want empty
        clear_cell = [x.remove() for x in my_model.grid[empty_cell].agents]

        my_model.step()

        self.assertEqual(my_ant.cell, my_model.grid[empty_cell])

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
        self.assertEqual(my_ant.history, [])

    def test_ant_smell_trail(self):
        """Test ant leaves a trail of smells wherever it walks"""

        ant_cell = (0, 0)

        my_model = model.Model(
            width=12,
            height=1,
            seed=1,
            players=None,
        )

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        steps = [my_model.step() for _ in range(9)]

        agents = list(my_model.agents)

        self.assertEqual(len(agents), 9 + 1)

    def test_ant_follow_smell(self):
        """Ants should be following the oldest scent trail"""
        pass


if __name__ == "__main__":
    unittest.main()
