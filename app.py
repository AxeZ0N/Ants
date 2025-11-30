import solara
import mesa
import model
import agents

from mesa.discrete_space import Cell
from mesa.visualization import SolaraViz, SpaceRenderer, make_plot_component
from mesa.visualization.components import AgentPortrayalStyle

AgentPortrayal = lambda agent: AgentPortrayalStyle(size=agent.size, color=agent.color)

@solara.component()
def AgentInfo(model):
    ants = model.agents_by_type[Ant]
    if not len(ants): return
    solara.Info(f'Info goes here!')

players = [
        agents.Ant,
        agents.Hill,
        agents.Food,
        ]


model_params = {
        'width':10,
        'height':10,
        'seed':1,
        'players':players,
        }

model = model.Model(**model_params)

plot_comp = make_plot_component("encoding", page=1)

space_renderer = SpaceRenderer(
        model = model, 
        backend = "matplotlib"
        )

renderer = space_renderer.render(
        agent_portrayal = AgentPortrayal
        )

comp = [ ]

page = SolaraViz(
        model,
        renderer,
        components = comp,
        model_params = model_params,
        name = 'Ants with tests!'
        )

