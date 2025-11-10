"""
Silly little tests
"""

import unittest

from mesa import Model as Model_Class
from mesa.discrete_space import CellAgent, FixedAgent, OrthogonalMooreGrid

from model import Model

import agents


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
    BLACKLIST = [
        "Agent",
        "CellAgent",
        "FixedAgent",
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


unittest.main()
