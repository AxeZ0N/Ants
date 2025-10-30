from mesa.discrete_space import Cell, CellAgent, FixedAgent
from agent_mixins import FoodStorage, EmitSmell

class Ant(CellAgent, FoodStorage, EmitSmell):
    '''
    Wander around until bumping into food
    '''
    color, size = 'red', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]

    def step(self):
        self.cell = self.cell.get_neighborhood().select_random_cell()


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

