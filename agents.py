from mesa.discrete_space import Cell, CellAgent, FixedAgent
from agent_mixins import FoodStorage, EmitSmell
from brain import Brain

class Ant(CellAgent, FoodStorage, EmitSmell):
    '''
    Wander around until bumping into food
    '''
    color, size = 'red', 100
    brain = None
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.brain = Brain(priority = [Hill, Food, Smell,])
        self.smell = self.set_scent(Smell)

    def step(self):
        self.drop_smell()
        self.cell = self.cell.get_neighborhood().select_random_cell()

    def get_next_action(self):
        ''' Decide if ant should move or not '''
        next_action = self.brain.next_action(self)

class Hill(FixedAgent, FoodStorage):
"""
Things that live in the model
"""


class Smell(FixedAgent):
    """Places where an ant has stepped"""

    color, size = "white", 1

    def __init__(self, model, coords, **kwargs):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []
        self.lifetime = kwargs.get("lifetime", 8888)

    def step(self):
        if self.lifetime > 0:
            self.lifetime -= 1
        else:
            self.remove()

    def update_display(self, color, size):
        self.color, self.size = color, size


class Hill(FixedAgent):
    """
    Ants return food to home
    """

    color, size = "brown", 200

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]


class Food(FixedAgent, FoodStorage, EmitSmell):
        self.storage = []

    def _suck_food(self):
        """Remove and store food from any ant that crosses"""
        for agent in self.cell.agents:
            if type(agent).__name__ == "Ant" and agent.storage:
                self.storage.append(agent.storage.pop())
                agent.state = agent.FOLLOW

    def step(self):
        self._suck_food()


class Food(FixedAgent):
    """
    Ants grab a Chunk of Food and carry it home
    """

    color, size = "orange", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]


class Smell(FixedAgent, EmitSmell):
    '''
    Doesn't move, tracks previous ant positions
    '''
    color, size = 'green', 75
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []

    def _clear_scent(self, ant):
        """Declutter the screen of scent markers"""
        for cell in ant.history:
            for agent in cell.agents:
                if isinstance(agent, Smell):
                    agent.lifetime = 0

    def step(self):
        for agent in self.cell.agents:
            if type(agent).__name__ == "Ant":
                if not agent.storage:
                    agent.storage.append(self)
                    self._clear_scent(agent)
                    # agent.history = [self.cell] # Can erase ant history if needed
