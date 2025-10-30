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

    def step(self):
        self.cell = self.cell.get_neighborhood().select_random_cell()

    def get_next_action(self):
        ''' Decide if ant should move or not '''
        next_action = self.brain.next_action(self)

class Hill(FixedAgent, FoodStorage):
    '''
    Ants return food to home
    '''
    color, size = 'brown', 200
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]


class Food(FixedAgent, FoodStorage, EmitSmell):
    '''
    Ants grab a Chunk of Food and carry it home
    '''
    color, size = 'orange', 100
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

