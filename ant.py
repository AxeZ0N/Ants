"""Ants are the main part of the sim"""

from dataclasses import dataclass
from itertools import chain
from mesa.discrete_space import CellAgent
import agents


class MyCellAgent(CellAgent):
    """ """

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell


@dataclass
class Coord:
    """ """

    x: int
    y: int

    def __add__(self, target):
        return self.x + target.x, self.y + target.y

    def __sub__(self, target):
        return self.x - target.x, self.y - target.y

def retrace_ant_steps(ant):
    start_cell = ant.cell.coordinate
    curr_cell = start_cell
    ret = []
    for delta in reversed(ant.history):
        print(f"Curr cell: {curr_cell}")
        print(f"Next delta: {delta}")

        curr_cell = Coord(*curr_cell) + Coord(*delta)

        ret.append(curr_cell)

        
    return 


class Ant(MyCellAgent):
    """
    Wander around until bumping into food
    """

    color, size = "red", 20
    WANDER, HOLDING, FOLLOW = "WANDER", "HOLDING", "FOLLOW"

    def __init__(self, model, cell=None):
        """ """
        super().__init__(model, cell)
        self.history = [(0,0)]
        self.storage = []
        self.state = Ant.WANDER

    def step(self):
        """ """
        next_cell = self._choose_next_cell()

        self._lay_scent()
        self._update_hx(next_cell)

        self.cell = next_cell

    def _update_hx(self, next_cell):
        """ """
        delta = Coord(*self.cell.coordinate) - Coord(*next_cell.coordinate)
        self.history.append(delta)

    def _choose_next_cell(self):
        """ """
        nbrhood = self.cell.get_neighborhood()
        priority = self._state_priority()

        return self._choose_cell_based_on_priority(nbrhood, priority)

    def _choose_cell_based_on_priority(self, nbrhood, priority):
        """ """
        all_agents = chain([cell.agents for cell in nbrhood])
        next_cell = nbrhood

        for prio in priority:
            prio_agents = [agent for agent in all_agents if isinstance(agent, prio)]
            if not prio_agents:
                continue
            next_cell = prio_agents
            break

        return next_cell.select_random_cell()

    def _lay_scent(self):
        """ """
        agents.Smell(self.model, cell=self.cell).step()

    def _set_state(self, new_state):
        """ """
        self.state = new_state

    def _state_priority(self):
        """ """
        match self.state:
            case Ant.WANDER:
                return [agents.Food]
            case Ant.HOLDING:
                return [agents.Hill, agents.Smell]
            case Ant.FOLLOW:
                return [agents.Food, agents.Smell]
