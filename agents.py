from mesa.discrete_space import Cell, CellAgent, FixedAgent
import abc

class Storage:
    def _check_storage(self, agent_storage):
        assert issubclass(type(agent_storage), self)

    @abc.abstractmethod
    def add(self, agent, amt): pass

    @abc.abstractmethod
    def remove(self, amt): pass

class FoodStorage(Storage):
    '''
    Allows carrying/holding food
    '''
    food = 0

    def add(self, agent, amt):
        self.add_food(agent, amt)

    def remove(self, amt):
        return self.remove(amt)

    def _add_food(self, agent, amt):
        '''
        Moves amt food into storage
        '''
        self._check_storage(agent.FoodStorage)
        agent.FoodStorage.remove_food(amt)
        self.food += amt

    def _remove_food(self, amt):
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

