"""
Silly little tests
"""

import unittest
import math

import numpy as np

from mesa import Model as Model_Class
from mesa.discrete_space import Cell, CellAgent, FixedAgent, OrthogonalMooreGrid

from model_app import Model

import agents
from ant import Ant, AntBrain


class MakeTestObj:
    """Builds agents and models for testing"""

    def model(self, *args, model=Model_Class, **kwargs):
        """Provide args for kwargs['model']"""
        my_model = model(*args, **kwargs)
        return my_model

    def agent(self, *args, agent=CellAgent, **kwargs):
        """Provide args for kwargs['agent']"""
        my_agent = agent(*args, **kwargs)
        return my_agent


class TestModel(unittest.TestCase):
    """Basic inits and such"""

    def setUp(self):
        self.model = MakeTestObj().model(model=Model)
        return self.model

    def tearDown(self):
        del self.model

    def test_init(self):
        """Basic stuff"""
        my_model = self.model

        self.assertTrue(issubclass(type(my_model), Model_Class))
        self.assertTrue(issubclass(type(my_model.grid), OrthogonalMooreGrid))

    def test_step(self):
        """If this fails, it's a problem"""
        self.model.step()


class TestAgent(unittest.TestCase):
    """Basic inits and such"""

    BLACKLIST = [
        "Agent",
        "CellAgent",
        "FixedAgent",
        "AntBrain",
    ]

    def _get_agents_list(self):
        """Snag agents from the file for testing"""
        my_test_agents = [
            v
            for k, v in vars(agents).items()
            if k not in self.BLACKLIST and not k.endswith("__")
        ]
        return my_test_agents

    def setUp(self):
        self.model = TestModel().setUp()

    def tearDown(self):
        del self.model

    def test_init(self):
        """Place a single unit of every agent found in the model"""
        agents_list = self._get_agents_list()
        my_agents = []
        for agent in agents_list:
            random_cell = self.model.random.choice(list(self.model.grid.all_cells))
            new_agent = MakeTestObj().agent(
                self.model, random_cell.coordinate, agent=agent
            )
            my_agents.append(new_agent)

        model_agents = list(self.model.agents)
        self.assertEqual(set(my_agents), set(model_agents))

    def test_agent_step(self):
        """Make sure all the agents can step"""
        agents_list = self._get_agents_list()
        my_agents = []
        for agent in agents_list:
            random_cell = self.model.random.choice(list(self.model.grid.all_cells))
            new_agent = MakeTestObj().agent(
                self.model, random_cell.coordinate, agent=agent
            )
            my_agents.append(new_agent)

        self.model.step()


class TestAnt(unittest.TestCase):
    """Test ant specific agent stuff"""

    ant_spawn = (4, 4)

    def setUp(self):
        self.model = TestModel().setUp()
        self.ant_agent = Ant(self.model, self.ant_spawn)

    def tearDown(self):
        del self.model

    def test_history(self):
        """Ants remember where they've been"""
        for _ in range(3):
            self.model.step()
        self.assertEqual(self.ant_agent.history[0].coordinate, self.ant_spawn)

        self.assertEqual(self.ant_agent.history[-1], self.ant_agent.cell)

    def showgrid(self):
        # print(self.ant_agent.cell.coordinate)
        for i in range(self.model.grid.width):
            for j in range(self.model.grid.height):
                cell = self.model.grid[(i, j)]
                if len(cell.agents):
                    print("x", end="")
                else:
                    print(".", end="")
            print()

    def test_prefer_new_cells(self):
        """
        Ants should try to move to cells they haven't seen before
        This test spawns a single wide path, meaning the only way is forward.
        If ants prefer new cells, there will be a point where there's no cells left unseen
        """

        self.model = Model(
            1,
            10,
        )
        self.ant_agent = Ant(self.model, (0, 0))
        # self.ant_agent.is_test = True

        for i in range(10):
            hx_len = len(self.ant_agent.history)
            self.assertEqual(hx_len, len(set(self.ant_agent.history)))
            # self.showgrid()
            self.model.step()

    def test_prefer_food(self):
        """Ants should try to move on top of food"""
        self.ant_agent = Ant(self.model, (3, 3))

        food = agents.Food(self.model, (3, 4))

        # self.ant_agent.is_test = True
        self.model.step()

        self.assertEqual(self.ant_agent.cell, food.cell)

    def test_pick_up_food(self):
        """Ants pick up food when they stand on it"""
        self.model = Model(
            1,
            2,
        )
        self.ant_agent = Ant(self.model, (0, 0))
        food = agents.Food(self.model, (0, 1))
        self.ant_agent.is_test = True

        self.assertEqual(self.ant_agent.storage, [])

        self.model.step()

        self.assertEqual(self.ant_agent.cell, food.cell)

        self.model.step()

        self.assertEqual(self.ant_agent.storage, [food])

    def test_drop_food(self):
        """Ants drop any food at home when they touch it"""
        self.model = Model(
            1,
            2,
        )
        self.ant_agent = Ant(self.model, (0, 0))
        food = agents.Food(self.model, (0, 0))
        home = agents.Hill(self.model, (0, 1))
        self.ant_agent.is_test = True

        self.model.step()
        self.showgrid()

        self.assertEqual(self.ant_agent.storage, [food])

        self.model.step()
        self.model.step()

        self.assertEqual(self.ant_agent.storage, [])
        self.assertEqual(home.storage, [food])


class TestNavigation(unittest.TestCase):
    ant_spawn = (4, 4)

    def setUp(self):
        self.model = TestModel().setUp()
        self.ant_agent = Ant(self.model, self.ant_spawn)

    def tearDown(self):
        del self.model

    def test_agv_vector(self):
        points = []
        for i in range(3):
            for j in range(3):
                points.append((i, j))

        def get_avg(points):
            xavg, yavg = 0, 0
            for x, y in points:
                xavg += x
                yavg += y

            avg_pt = xavg / len(points), yavg / len(points)
            return avg_pt

        def angle_between(p1, p2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]

            angle = np.atan2(dy, dx)
            return np.rad2deg(angle)

        for _ in range(10):
            self.model.step()
            avg = get_avg([x.coordinate for x in self.ant_agent.history])
            ant_pos = self.ant_agent.cell.coordinate
            angle = angle_between(ant_pos, avg)
            print(f"Angle from ant {ant_pos} to avg history {avg}: {angle}")

    def test_ant_retrace_steps(self):
        ant = self.ant_agent
        ant.cell = self.model.grid[(9,0)]
        ant.history = []
        for i in range(10):
            ant.history.append(self.model.grid[(i,0)])

        home = agents.Hill(self.model, (0,0))

        food = agents.Food(self.model, (9,0))

        print(ant.history)
        print(ant.cell.coordinate)

    def showgrid(self):
        # print(self.ant_agent.cell.coordinate)
        for i in range(self.model.grid.width):
            for j in range(self.model.grid.height):
                cell = self.model.grid[(i, j)]
                if len(cell.agents):
                    print("x", end="")
                else:
                    print(".", end="")
            print()

unittest.main()
