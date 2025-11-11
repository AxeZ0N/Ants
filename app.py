"""
Serves the Solara server my model
"""

import solara
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

import model
import agents


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
    if type(agents_by_type) is dict: 
        for k,v in agents_by_type.items():
            for ag in v:
                solara.Info(f"{k.__name__}: {ag.storage}")


players = [
    agents.Ant,
    agents.Hill,
    agents.Food,
]

my_model = model.Model(players=players)

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
