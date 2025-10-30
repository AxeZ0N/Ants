import abc

class Storage:
    storage = []

    def _check_storage(self, agent_storage):
        assert issubclass(type(agent_storage), type(self))

class FoodStorage(Storage):
    '''
    Allows carrying/holding food
    '''
    food: int = 0

    def add_food(self, amt):
        ''' Moves amt food into storage '''
        self.food += amt
        return self.food

    def remove_food(self, amt):
        ''' Remove amt food from self '''
        self.food -= amt
        return amt

