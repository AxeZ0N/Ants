from mesa.discrete_space import FixedAgent


class My_Fixed_Agent(FixedAgent):
    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell
        pass


class Hill(My_Fixed_Agent):
    pass


class Food(My_Fixed_Agent):
    pass


class Smell(My_Fixed_Agent):
    age = 0
    max_age = 999

    def __init__(self, model, cell=None):
        super().__init__(model, cell)
        self.age = 0

    def step(self):
        self._age()

    def _age(self):
        self.age += 1
        if self.age > self.max_age:
            self.remove()
