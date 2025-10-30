from mesa.discrete_space import Cell, CellAgent, FixedAgent
from agent_mixins import FoodStorage

class Ant(CellAgent, FoodStorage):
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


class Food(FixedAgent, FoodStorage):
    '''
    Ants grab a Chunk of Food and carry it home
    '''
    color, size = 'orange', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]

