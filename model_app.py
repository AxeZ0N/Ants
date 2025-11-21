"""
Subclassing mesa.Model
Serves the Solara server my model
"""

import mesa
import solara
from mesa.discrete_space import OrthogonalMooreGrid


import solara
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

import agents, ant


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


def agent_portrayal(agent):
    """Solara helper fcn"""
    return AgentPortrayalStyle(
        size=agent.size,
        color=agent.color,
    )


@solara.component()
def agent_info(model_data):
    """Solara display fcn"""
    agents_by_type = model_data.info.value
    if isinstance(agents_by_type, dict):
        for k, v in agents_by_type.items():
            for ag in v:
                solara.Info(f"{k.__name__}: {ag.storage}")


players = [
    ant.Ant,
    # agents.Ant,
    # agents.Ant,
    agents.Hill,
    agents.Food,
]

my_model = Model(players=players)

model_params = {
    "width": 10,
    "height": 10,
    "seed": 1,
    "players": players,
}

plot_comp = make_plot_component("encoding", page=1)
space_renderer = SpaceRenderer(model=my_model, backend="matplotlib")
renderer = space_renderer.render(agent_portrayal=agent_portrayal)

comp = [agent_info]

page = SolaraViz(
    my_model,
    renderer,
    components=comp,
    model_params=model_params,
    name="Ants with tests!",
)
