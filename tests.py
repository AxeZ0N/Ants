""" """

import unittest

from mesa.agent import AgentSet

import agents
import model
import ant


class TestAntWander(unittest.TestCase):
    def setUp(self):
        """Ant arena! 3x3, ant in the middle"""
        self.ant_pos = (1, 1)

        self.test_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        self.test_ant = ant.Ant(
            model=self.test_model,
            cell=self.test_model.grid[self.ant_pos],
        )

        self.test_ant.state = self.test_ant.WANDER

    def tearDown(self):
        """Leave no survivors"""
        self.test_model = None
        self.test_ant = None

    def test_prefer_food(self):
        """Ants prefer adjacent food in state: WANDER"""

        # Surround ant with tempting smells
        smells = []

        food_pos = (1, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                coord = (i, j)
                if coord in (self.ant_pos, food_pos):
                    continue

                smell = agents.Smell(
                    model=self.test_model,
                    cell=self.test_model.grid[coord],
                )

                smells += [smell]

        # Replace one smell with food
        food = agents.Food(
            model=self.test_model,
            cell=self.test_model.grid[food_pos],
        )

        self.assertEqual(self.test_ant.cell.coordinate, self.ant_pos)

        self.test_model.step()

        self.assertEqual(self.test_ant.cell.coordinate, food_pos)

    def test_avoid_smell(self):
        """Ants prefer unvisited cells in state: WANDER"""

        # Surround ant with tempting smells
        smells = []

        nothing_pos = (1, 0)

        for i in range(0, 3):
            for j in range(0, 3):
                coord = (i, j)
                if coord in (self.ant_pos, nothing_pos):
                    continue

                smell = agents.Smell(
                    model=self.test_model,
                    cell=self.test_model.grid[coord],
                )

                smells += [smell]

        # Replace one smell with NOTHING
        self.assertEqual(self.test_ant.cell.coordinate, self.ant_pos)

        self.test_model.step()

        self.assertEqual(self.test_ant.cell.coordinate, nothing_pos)


class TestAntHold(unittest.TestCase):
    def setUp(self):
        """Ant arena! 3x3, ant in the middle"""
        self.ant_pos = (1, 1)

        self.test_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        self.test_ant = ant.Ant(
            model=self.test_model,
            cell=self.test_model.grid[self.ant_pos],
        )

        self.test_ant.state = self.test_ant.HOLD

    def tearDown(self):
        """Leave no survivors"""
        self.test_model = None
        self.test_ant = None

    def test_follow_trail(self):
        """Ants"""

        # Surround ant with a spiral of aged smells
        smells = []

        start_pos, end_pos = self.ant_pos, (2, 2)

        age = 0

        for i in range(0, 3):
            for j in range(0, 3):
                coord = (i, j)
                if coord in (self.ant_pos):
                    continue

                smell = agents.Smell(
                    model=self.test_model,
                    cell=self.test_model.grid[coord],
                )
                age += 1

                smell.age = age

                smells += [smell]

        # Step 7 times and see if the ant makes it around
        self.assertEqual(self.test_ant.cell.coordinate, start_pos)

        for _ in range(10):
            self.test_model.step()
            print(self.test_ant.cell.coordinate)

        print(f"Readout for smell ages:")
        for ag in self.test_model.agents:
            print(f"Type: {type(ag)}, Age {ag.age}, Location: {ag.cell.coordinate}")

        self.assertEqual(self.test_ant.cell.coordinate, end_pos)

    def test_prefer_hill(self):
        """Ants ultimately drop off food at home when they find it"""

        # Surround ant with a spiral of aged smells
        smells = []

        hill_pos = (1, 2)

        age = 0

        for i in range(0, 3):
            for j in range(0, 3):
                coord = (i, j)
                if coord in (self.ant_pos):
                    continue

                smell = agents.Smell(
                    model=self.test_model,
                    cell=self.test_model.grid[coord],
                )
                age += 1

                smell.age = age

                smells += [smell]

        # Replace one smell with Hill
        hill = agents.Hill(
            model=self.test_model,
            cell=self.test_model.grid[hill_pos],
        )

        self.test_model.step()

        self.assertEqual(self.test_ant.cell.coordinate, hill_pos)


class TestAgent(unittest.TestCase):
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
        my_ant.state = my_ant.HOLD

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
