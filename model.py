"""
Subclassing mesa.Model
"""

import mesa
import solara
from mesa.discrete_space import OrthogonalMooreGrid


class Model(mesa.Model):
    """
    Top level, holds and runs the sim
    """

    def _build_players(self, *args):
        """Populates the model"""
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
            self._build_players(*players)

        self.info = solara.reactive(self.get_info(), equals=lambda x, y: False)

    def step(self):
        agents_list = self.agents_by_type.copy()
        for _, v in agents_list.items():
            v.do("step")
        self.info.set(self.get_info())

    def get_info(self):
        return self.agents_by_type
