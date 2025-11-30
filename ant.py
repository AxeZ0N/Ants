"""Ants are the main part of the sim"""

from mesa.discrete_space import CellAgent
from dataclasses import dataclass


class My_Cell_Agent(CellAgent):
    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell

@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, target):
        return self.x+target.x, self.y+target.y

    def __sub__(self, target):
        return self.x-target.x, self.y-target.y

def get_delta(c1,c2):
    return Coord(*c1) - Coord(*c2)

class Ant(My_Cell_Agent):
    """
    Wander around until bumping into food
    """

    def __init__(self, model, cell=None):
        super().__init__(model, cell)
        self.history = []
        self.storage = []

    def step(self):
        next_cell = self._choose_next_cell()
        delta = get_delta(self.cell.coordinate, next_cell.coordinate)

        self.history.append(delta)
        self.cell = next_cell

    def _choose_next_cell(self):
        next_cell = self.cell.get_neighborhood().select_random_cell()
        return next_cell
