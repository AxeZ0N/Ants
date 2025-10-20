import unittest

from mesa import Model as Model_Class
from mesa.discrete_space import OrthogonalMooreGrid, CellAgent, Cell

from model import Model
from agents import Ant


class TestModel(unittest.TestCase):
    @staticmethod
    def generate_model():
        my_model = Model(
                width = 10,
                height = 10,
                seed = 1,
                )
        return my_model

    def test_init(self):

        my_model = TestModel.generate_model()

        self.assertTrue(
                issubclass(
                    type(my_model),
                    Model_Class
                    )
                )
        self.assertTrue(
                issubclass(
                    type(my_model.grid),
                    OrthogonalMooreGrid
                    )
                )

class TestAgents(unittest.TestCase):
    @staticmethod
    def generate_ant():
        test_coord = (0,0)
        my_ant = Ant(
                coords = test_coord,
                )
        return my_ant
        
    def test_ant(self):
        test_coord = (0,0)

        my_model = TestModel.generate_model()

        my_ant = Ant(
                model = my_model,
                coords = test_coord,
                )

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

        self.assertEqual(
                my_ant.cell.coordinate,
                test_coord
                )

unittest.main()
