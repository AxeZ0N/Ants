from mesa.discrete_space import Cell, CellAgent, FixedAgent

class FoodStorage:
    '''
    Allows carrying/holding food
    '''
    food = 0

    def add_food(self, agent, amt):
        '''
        Moves amt food into storage
        '''
        assert issubclass(type(agent.FoodStorage), FoodStorage)
        agent.FoodStorage.remove_food(amt)
        self.food += amt

    def remove_food(self, amt):
        '''
        Remove amt food from self
        '''
        self.food -= amt
        return amt


class Ant(CellAgent):
    '''
    Wander around until bumping into food
    '''
    color, size = 'red', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.FoodStorage = FoodStorage()

    def step(self):
        self.cell = self.cell.get_neighborhood().select_random_cell()


class Hill(FixedAgent):
    '''
    Ants return food to home
    '''
    color, size = 'brown', 200
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.FoodStorage = FoodStorage()


class Food(FixedAgent):
    '''
    Ants grab a Chunk of Food and carry it home
    '''
    color, size = 'orange', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.FoodStorage = FoodStorage()

