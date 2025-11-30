"""
Subclassing mesa.Model
Serves the Solara server my model
"""

import mesa
import solara
from mesa.discrete_space import OrthogonalMooreGrid
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

    def __init__(self, width, height, seed, players=None):

        super().__init__(seed=seed)

        self.grid = OrthogonalMooreGrid(
            dimensions=(width, height),
            random=self.random,
        )

        if players is not None:
            self._build_players(*players)

        self.info = solara.reactive(self.get_info(), equals=lambda x, y: False)

        self.relocate_ants()

    def step(self):
        agents_list = self.agents_by_type.copy()
        for _, v in agents_list.items():
            v.do("step")
        self.info.set(self.get_info())

    def get_info(self):
        """Used by solara viz"""
        return self.agents_by_type

    def relocate_ants(self):
        """Ants should spawn at home"""

        agents_list = self.agents_by_type
        if agents.Hill not in agents_list: return

        hill = agents_list[agents.Hill][0]
        ants = agents_list[ant.Ant]

        for my_ant in ants:
            my_ant.cell = hill.cell

toggle_states = [True, False]
curr_toggle_state = solara.reactive(False)


def agent_portrayal(agent):
    """Solara helper fcn"""

    size, color = agent.size, agent.color

    return AgentPortrayalStyle(size=size, color=color)


@solara.component()
def toggle_smells(model_data):

    def update_smell_display_callback(value):
        my_agents = model_data.agents_by_type

        if not value:
            size, color = 1, "white"
        else:
            size, color = 10, "green"

        agents.Smell.size, agents.Smell.color = size, color

        if agents.Smell in my_agents.keys():
            for agent in my_agents[agents.Smell]:
                agent.update_display(color, size)

    solara.ToggleButtonsSingle(
        value=curr_toggle_state,
        values=toggle_states,
        on_value=update_smell_display_callback,
    )


@solara.component()
def agent_info(model_data):
    """Solara display fcn"""
    agents_by_type = model_data.info.value
    if isinstance(agents_by_type, dict):
        for k, v in agents_by_type.items():
            for ag in v:
                solara.Info(f"{k.__name__}: {ag.storage}")


# Mostly boilerplate from mesa basic tutorial
players = [
    ant.Ant,
    # agents.Ant,
    # agents.Ant,
    agents.Hill,
    agents.Food,
]


model_params = {
    "width": 10,
    "height": 10,
    "seed": 1,
    "players": players,
}

my_model = Model(**model_params)

plot_comp = make_plot_component("encoding", page=1)
space_renderer = SpaceRenderer(model=my_model, backend="matplotlib")
renderer = space_renderer.render(agent_portrayal=agent_portrayal)

comp = [agent_info, toggle_smells]

page = SolaraViz(
    my_model,
    renderer,
    components=comp,
    model_params=model_params,
    name="Ants with tests!",
)
# Mostly boilerplate from mesa basic tutorial
