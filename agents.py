"""Non moving interactive agents"""

from mesa.discrete_space import FixedAgent


class MyFixedAgent(FixedAgent):
    """Helper"""

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell
        pass


class Hill(MyFixedAgent):
    """Home base. Holds food."""

    color, size = "brown", 30

    def __init__(self, model, cell=None, spawn=None):
        super().__init__(model, cell)
        self._spawn = spawn
        self.storage = []

    def spawn(self, amt):
        """Can spawn any number of things at self.cell.coordinate"""
        assert self._spawn is not None

        agents = self._spawn.create_agents(
            model=self.model,
            n=amt,
            cell=[self.cell for _ in range(amt)],
        )

        return agents

    def suck_food(self):
        """If the agent moves, try to suck food"""
        for agent in self.cell.agents:
            if not isinstance(agent, FixedAgent):
                if agent.storage:
                    continue
                self.storage.append(agent.storage.pop())
                agent.state = agent.FOLLOW


class Food(MyFixedAgent):
    """Ants search for these"""

    color, size = "blue", 30

    def __init__(self, model, cell=None):
        super().__init__(model, cell)

    def step(self):
        """Every iteration, check for ants to push food on"""
        self.push_food()

    def push_food(self):
        """If the agent moves, try to push food"""
        for agent in self.cell.agents:
            if not isinstance(agent, FixedAgent):
                if agent.storage:
                    continue
                agent.storage.append(self)
                agent.state = agent.HOLDING


class Smell(MyFixedAgent):
    """Helps ants navigate"""

    color, size = "green", 15
    age = 0
    max_age = 100

    def __init__(self, model, cell=None):
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
