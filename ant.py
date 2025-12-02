"""Ants are the main part of the sim"""

from dataclasses import dataclass
from itertools import chain
from mesa.discrete_space import CellAgent
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

    def __init__(self, model, cell=None):
        """ """
        super().__init__(model, cell)
        self.history = [(0, 0)]
        self.storage = []
        self.state = Ant.WANDER

    def step(self):
        """Called in each iteration of the model"""
        pass
