from mesa.discrete_space import Cell, CellAgent, FixedAgent

class HasFoodStorage:
    food = 0

class Ant(CellAgent, HasFoodStorage):
    '''
    Wander around until bumping into food
    '''
    color, size = 'red', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]

    def step(self):
        self.cell = self.cell.get_neighborhood().select_random_cell()

    def grab_food(self, food_agent, amt):
        '''
        Moves amt food into the ant's storage
        '''
        assert issubclass(type(food_agent), HasFoodStorage)
        food_agent.remove_food(amt)
        self.food += amt

class Hill(FixedAgent, HasFoodStorage):
    '''
    Ants return food to home
    '''
    color, size = 'brown', 200
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]

class Food(FixedAgent, HasFoodStorage):
    '''
    Ants grab a Chunk of Food and carry it home
    '''
    color, size = 'orange', 100
    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]

    def remove_food(amt):
        self.food -= amt
        return amt

