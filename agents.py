from mesa.discrete_space import FixedAgent


class My_Fixed_Agent(FixedAgent):
    def __init__(self, model, cell=None):
        self.model = model
        self.cell = cell
        pass


class Hill(My_Fixed_Agent):
    pass


class Food(My_Fixed_Agent):
    pass


class Smell(My_Fixed_Agent):
    pass
