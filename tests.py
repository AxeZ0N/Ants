"""
Silly little tests
"""

import unittest

from mesa import Model as Model_Class
from mesa.discrete_space import Cell, CellAgent, FixedAgent, OrthogonalMooreGrid

from model import Model
from agents import Ant, Hill, Food


class MakeTestObj:
    """Builds agents and models for testing"""

    def model(self, *args, **kwargs):
        """Provide args for kwargs['model']"""
        model = kwargs.pop("model")(*args)
        return model

    def agent(self, *args, **kwargs):
        """Provide args for kwargs['agent']"""
        agent = kwargs.pop("agent")
        return agent(*args)


m = MakeTestObj().model(10, 10, model=Model)
a = MakeTestObj().agent(m, (3, 3), agent=Ant)


class TestModel(unittest.TestCase):
    """Basic inits and such"""

    @staticmethod
    def generate_model():
        """Wrapper for model.generate_model"""
        my_model = Model(
            width=3,
            height=3,
            seed=1,
        )
        return my_model

    def test_init(self):
        """Basic stuff"""
        my_model = TestModel.generate_model()

        self.assertTrue(issubclass(type(my_model), Model_Class))
        self.assertTrue(issubclass(type(my_model.grid), OrthogonalMooreGrid))


class TestAgents(unittest.TestCase):
    """Agents get tested for model compliance"""

    @staticmethod
    def generate_ant(model, test_coord=(0, 0)):
        """Should be more generic"""
        my_ant = Ant(
            model=model,
            coords=test_coord,
        )
        return my_ant

    @staticmethod
    def generate_hill(model, test_coord=(0, 0)):
        """Should be more generic"""
        my_hill = Hill(
            model=model,
            coords=test_coord,
        )
        return my_hill

    @staticmethod
    def generate_food(model, test_coord=(0, 0)):
        """Should be more generic"""
        my_food = Food(
            model=model,
            coords=test_coord,
        )
        return my_food

    def test_ant_init(self):
        """Basic stuff"""
        test_coord = (0, 0)

        my_model = TestModel.generate_model()

        my_ant = TestAgents.generate_ant(my_model)

        self.assertTrue(
            issubclass(
                type(my_ant),
                CellAgent,
            )
        )

        self.assertTrue(
            issubclass(
                type(my_ant.cell),
                Cell,
            )
        )

        self.assertEqual(my_ant.cell.coordinate, test_coord)

    def test_hill_init(self):
        """Basic stuff"""
        test_coord = (0, 0)

        my_model = TestModel.generate_model()

        my_hill = TestAgents.generate_hill(my_model)

        self.assertTrue(
            issubclass(
                type(my_hill),
                FixedAgent,
            )
        )

        self.assertTrue(
            issubclass(
                type(my_hill.cell),
                Cell,
            )
        )

        self.assertEqual(my_hill.cell.coordinate, test_coord)

    def test_food_init(self):
        """Basic stuff"""
        test_coord = (0, 0)

        my_model = TestModel.generate_model()

        my_food = TestAgents.generate_food(my_model)

        self.assertTrue(
            issubclass(
                type(my_food),
                FixedAgent,
            )
        )

        self.assertTrue(
            issubclass(
                type(my_food.cell),
                Cell,
            )
        )

        self.assertEqual(my_food.cell.coordinate, test_coord)

    def test_ant_move(self):
        """Basic stuff"""
        test_coord = (0, 0)

        my_model = TestModel.generate_model()

        my_ant = TestAgents.generate_ant(my_model)

        self.assertEqual(
            my_ant.cell.coordinate,
            test_coord,
        )

        my_model.step()

        self.assertNotEqual(
            my_ant.cell.coordinate,
            test_coord,
        )


unittest.main()
