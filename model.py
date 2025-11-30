"""
Subclassing mesa.Model
Serves the Solara server my model
"""

import mesa
import solara
from mesa.discrete_space import OrthogonalMooreGrid
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

import agents
import ant


class Model(mesa.Model):
    """ """

    def __init__(self, width, height, seed, players=None):

        super().__init__(seed=seed)

        self.grid = OrthogonalMooreGrid(
            dimensions=(width, height), torus=False, random=self.random
        )

        if players is not None:
            for p in players:
                p.create_agents(self, 1, self.grid.empties.select_random_cell())

    def step(self):
        agents_list = self.agents_by_type.copy()

        sorted_list = list(sorted(agents_list.keys(), key=str))

        do_update = [agents_list[agents].do("step") for agents in sorted_list]


def agent_portrayal(agent):
    """Solara helper fcn"""

    size, color = agent.size, agent.color

    return AgentPortrayalStyle(size=size, color=color)


model_params = {
    "width": 10,
    "height": 10,
    "seed": 1,
    "players": None,
}

my_model = Model(**model_params)

plot_comp = make_plot_component("encoding", page=1)
space_renderer = SpaceRenderer(model=my_model, backend="matplotlib")
renderer = space_renderer.render(agent_portrayal=agent_portrayal)

comp = []

page = SolaraViz(
    my_model,
    renderer,
    components=comp,
    model_params=model_params,
    name="Ants with tests!",
)
# Mostly boilerplate from mesa basic tutorial
