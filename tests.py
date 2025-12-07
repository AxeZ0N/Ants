""" """

import unittest

from mesa.agent import AgentSet

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

            # cell.add_agent(new_smell)

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

        my_agents = list(my_model.agents)

        self.assertEqual(len(my_agents), 9 + 1)

    def test_ant_follow_smell(self):
        """Ants should be following the oldest scent trail"""

        ant_cell = (1, 1)
        old_smell_cell = (1, 2)
        hill_cell = (1, 3)

        my_model = model.Model(
            width=3,
            height=4,
            seed=1,
            players=None,
        )

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        my_food = agents.Food(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        my_hill = agents.Hill(
            model=my_model,
            cell=my_model.grid[hill_cell],
        )

        my_ant.storage += [my_food]
        my_ant.state = my_ant.HOLDING

        for i, cell in enumerate(my_ant.cell.get_neighborhood()):
            smell = agents.Smell(model=my_model, cell=cell)
            smell.age = i

        for ag in my_model.grid[old_smell_cell].agents:
            if isinstance(ag, agents.Smell):
                ag.age = 80

        my_model.step()

        self.assertEqual(my_ant.cell, my_model.grid[old_smell_cell])

        my_model.step()

        self.assertEqual(my_ant.cell, my_model.grid[hill_cell])

    def test_ant_state_follow(self):
        """Ants follow seen_food smell trails until hitting food or turn back to wandering"""

        ant_cell = (0, 0)
        food_cell = (5, 0)

        my_model = model.Model(
            width=6,
            height=1,
            seed=1,
            players=None,
        )

        my_food = agents.Food(
            model=my_model,
            cell=my_model.grid[food_cell],
        )

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[ant_cell],
        )

        my_ant.state = my_ant.FOLLOW

        smell_cells = reversed([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])

        for i, cell in enumerate(smell_cells):
            smell = agents.Smell(
                model=my_model,
                cell=my_model.grid[cell],
            )

            smell.seen_food = True
            smell.age = i

            # print(smell)

        steps = [my_model.step() for _ in range(5)]

        self.assertEqual(my_ant.cell, my_food.cell)


class TestCellChoices(unittest.TestCase):
    """ """

    def test_init(self):
        """ """

        ant_cell = (1, 1)

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

        my_cell_choice = ant.CellChoices(my_ant)

        self.assertEqual(my_cell_choice.base_cell, my_ant.cell)
        self.assertEqual(my_cell_choice.nbr_cells, my_ant.cell.get_neighborhood())

    def test_sort_agents(self):
        """ """
        ant_cell = (1, 1)

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

        raw_smells = []

        for i, cell in enumerate(my_ant.cell.get_neighborhood()):
            smell = agents.Smell(model=my_model, cell=cell)

            smell.age = i
            raw_smells.append(smell)

        my_cell_choice = ant.CellChoices(my_ant)

        self.assertEqual(my_cell_choice.base_cell, my_ant.cell)
        self.assertEqual(my_cell_choice.nbr_cells, my_ant.cell.get_neighborhood())

        test_agents = [
            agent for cell in my_ant.cell.get_neighborhood() for agent in cell.agents
        ]

        self.assertEqual(list(my_cell_choice.all_agents), list(AgentSet(test_agents)))

        my_sorted_list = list(my_cell_choice.sort_agents_by("age"))

        self.assertEqual(my_sorted_list, raw_smells)

    def test_sort_cells(self):
        """ """
        ant_cell = (1, 1)

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

        raw_smells = []

        for i, cell in enumerate(my_ant.cell.get_neighborhood()):
            smell = agents.Smell(model=my_model, cell=cell)
            smell.age = i

            if not i % 2:
                food = agents.Food(model=my_model, cell=cell)
                food.size = i

            raw_smells.append(smell)

        my_cell_choice = ant.CellChoices(my_ant)

        self.assertEqual(my_cell_choice.base_cell, my_ant.cell)
        self.assertEqual(my_cell_choice.nbr_cells, my_ant.cell.get_neighborhood())

        type_ = agents.Food

        cells_with_agents = [
            agent.cell
            for cell in my_cell_choice.nbr_cells
            for agent in cell.agents
            if isinstance(agent, type_)
        ]

        self.assertEqual(list(my_cell_choice.sort_cells_by(type_)), cells_with_agents)


if __name__ == "__main__":
    unittest.main()
