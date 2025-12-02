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

        my_model = model.Model(
            width=3,
            height=3,
            seed=1,
            players=None,
        )

        my_hill = agents.Hill(model=my_model, cell=my_model.grid[(1, 0)], spawn=ant.Ant)

        my_ant = ant.Ant(
            model=my_model,
            cell=my_model.grid[(1, 1)],
        )


if __name__ == "__main__":
    unittest.main()
