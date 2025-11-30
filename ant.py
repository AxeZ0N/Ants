"""Ants are the main part of the sim"""

from mesa.discrete_space import CellAgent
from dataclasses import dataclass
from itertools import chain
import agents


class My_Cell_Agent(CellAgent):
    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell


@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, target):
        return self.x + target.x, self.y + target.y

    def __sub__(self, target):
        return self.x - target.x, self.y - target.y


class Ant(My_Cell_Agent):
    """
    Wander around until bumping into food
    """

    WANDER, HOLDING, FOLLOW = "WANDER", "HOLDING", "FOLLOW"
    
    def __init__(self, model, cell=None):
        super().__init__(model, cell)
        self.history = []
        self.storage = []
        self.state = Ant.WANDER

    def step(self):
        next_cell = self._choose_next_cell()

        self._update_hx(next_cell)
        self._lay_scent()

        self.cell = next_cell

    def _update_hx(self, next_cell):
        delta = Coord(*next_cell.coordinate) - Coord(*self.cell.coordinate)
        self.history.append(delta)

    def _choose_next_cell(self):
        nbrhood = self.cell.get_neighborhood()
        priority = self._state_priority()

        return self._choose_cell_based_on_priority(nbrhood, priority)

    def _choose_cell_based_on_priority(self, nbrhood, priority):
        all_agents = chain([cell.agents for cell in nbrhood])
        next_cell = nbrhood

        for prio in priority:
            prio_agents = [agent for agent in all_agents if isinstance(agent, prio)]
            if not prio_agents: continue
            next_cell = prio_agents
            break

        return next_cell.select_random_cell()

    def _lay_scent(self):
        agents.Smell(self.model, cell=self.cell).step()

    def _state_priority(self):
        match self.state:
            case Ant.WANDER: return [agents.Food]
            case Ant.HOLDING: return [agents.Hill, agents.Smell]
            case Ant.FOLLOW: return [agents.Food, agents.Smell]
