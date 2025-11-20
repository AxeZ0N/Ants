"""
Things that live in the model
"""

from mesa.discrete_space import CellAgent, FixedAgent


class Smell(FixedAgent):
    """Places where an ant has stepped"""
    color, size = "green", 40

    def __init__(self, model, coords, **kwargs):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []
        self.lifetime = kwargs.get("lifetime", 8888)

    def step(self):
        if self.lifetime <= 0:
            self.remove()
        else:
            self.lifetime -= 1

class Hill(FixedAgent):
    """
    Ants return food to home
    """

    color, size = "brown", 200

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []

    def step(self):
        for agent in self.cell.agents:
            #print('foobar')
            if type(agent).__name__ == "Ant":
                if agent.storage:
                    self.storage.append(agent.storage.pop())


class Food(FixedAgent):
    """
    Ants grab a Chunk of Food and carry it home
    """

    color, size = "orange", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []

    def erase_hx(self, ant):
        for cell in ant.history:

            for agent in cell.agents:
                if isinstance(agent, Smell):
                    agent.lifetime = 0
                    return ant
        return ant

        self.history = []
    def step(self):
        for agent in self.cell.agents:
            #print('foobar')
            if type(agent).__name__ == "Ant":
                if not agent.storage:
                    agent.storage.append(self)
                    agent = self.erase_hx(agent)
                    agent.history = [self.cell]
