import abc

class MixinBase: pass

class Smells(MixinBase):
    '''
    Smell related methods
    '''
    scent = None

    def set_scent(self, scent):
        self.scent = scent

class EmitSmell(Smells):
    '''
    Drops related scent on the field
    '''

    def drop_smell(self):
        smell = self.scent(self.model, self.cell.coordinate)
        self.cell.add_agent(smell)

class Storage(MixinBase):
    storage = []

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
