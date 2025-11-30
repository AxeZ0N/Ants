"""Ants are the main part of the sim"""

from mesa.discrete_space import CellAgent


class My_Cell_Agent(CellAgent):
    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell


class Ant(My_Cell_Agent):
    """
    Wander around until bumping into food
    """

    def __init__(self, model, cell=None):
        super().__init__(model, cell)
        self.history = []
        self.storage = []

    def step(self):
        self.cell = self._choose_next_cell()
        pass

    def _choose_next_cell(self):
        next_cell = self.cell.get_neighborhood().select_random_cell()
        return next_cell
