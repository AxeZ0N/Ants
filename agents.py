""" """

from mesa.discrete_space import FixedAgent


class My_Fixed_Agent(FixedAgent):
    """Helper"""

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell
        pass


class Hill(My_Fixed_Agent):
    """Home base. Holds food."""

    color, size = "brown", 30

    def __init__(self, model, cell=None, spawn=None):
        super().__init__(model, cell)
        self._spawn = spawn

    def spawn(self, amt):
        """Can spawn any number of things at self.cell.coordinate"""
        assert self._spawn is not None

        agents = self._spawn.create_agents(
            model=self.model,
            n=amt,
            cell=[self.cell.coordinate for _ in range(amt)],
        )

        return agents


class Food(My_Fixed_Agent):
    """Ants search for these"""

    color, size = "yellow", 30
    pass


class Smell(My_Fixed_Agent):
    """Helps ants navigate"""

    color, size = "green", 15
    age = 0
    max_age = 999

    def __init__(self, model, cell=None):
        """ """
        super().__init__(model, cell)
        self.age = 0

    def step(self):
        """ """
        self._age()

    def _age(self):
        """ """
        self.age += 1
        if self.age > self.max_age:
            self.remove()
