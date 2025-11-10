"""
Things that live in the model
"""

from mesa.discrete_space import CellAgent, FixedAgent


class Ant(CellAgent):
    """
    Wander around until bumping into food
    """
    is_test = False

    color, size = "red", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.history = [self.cell]

    def step(self):
        next_step = [x for x in self.cell.get_neighborhood() if x not in self.history]
        if self.model.grid.width == 1 and self.is_test:
            print(f"I'm an ant, choosing from {len(next_step)} cells!")
        if not len(next_step): next_step = list(self.cell.get_neighborhood())
        self.cell = self.model.random.choice(next_step)
        self.history.append(self.cell)


class Hill(FixedAgent):
    """
    Ants return food to home
    """

    color, size = "brown", 200

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]


class Food(FixedAgent):
    """
    Ants grab a Chunk of Food and carry it home
    """

    color, size = "orange", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
