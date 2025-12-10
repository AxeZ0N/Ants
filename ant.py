"""Ants are the main part of the sim"""

from dataclasses import dataclass
from itertools import chain

from mesa.discrete_space import CellAgent, CellCollection
from mesa.agent import AgentSet

import agents


class MyCellAgent(CellAgent):
    """Helper"""

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell


@dataclass
class Coord:
    """Class for manipulating xy coords"""

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


class CellChoices:
    """Helps with stuff for decisions about next step"""

    def __init__(self, cell_haver):

        self.base = cell_haver
        self.base_cell = cell_haver.cell
        self.nbr_cells = self.base_cell.get_neighborhood() or []
        self.all_agents = AgentSet(
            self.nbr_cells.agents, random=cell_haver.model.random
        )

    def sort_agents_by(self, attr):
        """Returns all agents in nbrs, sorted by attr."""
        if not self.all_agents:
            return []

        return AgentSet(sorted(self.all_agents, key=lambda x: getattr(x, attr)))

    def sort_cells_by(self, type_):
        """Returns only cells that contain type_"""

        assert isinstance(type_, type)

        return CellCollection(
            (
                agent.cell
                for cell in self.nbr_cells
                for agent in cell.agents
                if isinstance(agent, type_)
            ),
            random=self.base.model.random,
        )


class Ant(MyCellAgent):
    """
    Wander around until bumping into food

    While in state WANDER:
        Ants prefer Food.
        Ants avoid Smells.

    While in state HOLDING:
        Ants prefer Home -> Smells.
        Ants avoid Food.

    While in state FOLLOW:
        Ants prefer Food -> Smells.

    """

    color, size = "red", 20
    WANDER, HOLDING, FOLLOW = "WANDER", "HOLDING", "FOLLOW"
    DEFAULT_STATE = WANDER

    def __init__(self, model, cell=None):
        """ """
        super().__init__(model, cell)
        self.history = []
        self.storage = []
        self.state = Ant.DEFAULT_STATE

    def step(self):
        """Called in each iteration of the model"""
        match self.state:
            case self.WANDER:
                next_cell = self.wander()
            case self.HOLDING:
                next_cell = self.holding()
            case self.FOLLOW:
                next_cell = self.follow()

        # print(self.state)
        self.drop_scent()
        self.cell = next_cell

    def drop_scent(self):
        """Helps the ant remember where it's been"""

        for agent in self.cell.agents:
            if isinstance(agent, agents.Smell):
                return

        smell = agents.Smell(
            model=self.model,
            cell=self.cell,
        )

        self.history.append(smell)

    def wander(self):
        cell_chooser = CellChoices(self)

        all_nbrs = self.cell.get_neighborhood()
        print(type(all_nbrs))
        smell_nbrs = cell_chooser.sort_cells_by(agents.Smell)

        no_smell_cells = CellCollection(
            set(all_nbrs).difference(set(smell_nbrs)),
            random=self.model.random,
        )

        ret = no_smell_cells.select_random_cell()
        print(ret.coordinate)

        return ret
