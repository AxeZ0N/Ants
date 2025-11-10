"""
Subclassing mesa.Model
"""

import mesa
from mesa.discrete_space import OrthogonalMooreGrid


class Model(mesa.Model):
    """
    Top level, holds and runs the sim
    """

    def generate_test_state(self, *args):
        """Plops out a model state"""
        for player in args:
            player.create_agents(
                self,
                1,
                self.grid.empties.select_random_cell().coordinate,
            )

    def __init__(self, width=10, height=10, seed=1, players=None):

        super().__init__(seed=seed)

        self.grid = OrthogonalMooreGrid(
            dimensions=(width, height),
            random=self.random,
        )

        if players is not None:
            self.generate_test_state(*players)

    def step(self):
        agents_list = self.agents_by_type.copy()
        for _, v in agents_list.items():
            v.do("step")
