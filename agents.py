"""Non moving interactive agents"""

from mesa.discrete_space import FixedAgent


class MyFixedAgent(FixedAgent):
    """Helper"""

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell
        self.age = 0
        self.max_age = 9e99
        pass

    def _age(self):
        """ """
        self.age += 1
        if self.age > self.max_age:
            self.remove()


class Hill(MyFixedAgent):
    """Home base. Holds food."""

    color, size = "brown", 30

    def __init__(self, model, cell=None, spawn=None):
        super().__init__(model, cell)
        self._spawn = spawn
        self.storage = []

    def step(self):
        """ """
        self.suck_food()
        self._age()

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
                if not agent.storage:
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
        self._age()

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
    max_age = 125

    def __init__(self, model, cell=None):
        super().__init__(model, cell)
        self.age = 0
        self.seen_food = False

    def step(self):
        """Ants add a bit to the max age every time they pass over."""
        # Age the agent
        self._age()

        # Check if the agent should extend its lifespan
        for agent in self.cell.agents:
            if isinstance(agent, FixedAgent):
                continue
            self.max_age += 20
            break

        # Check if this agent has seen an ant carrying food
        for agent in self.cell.agents:
            if isinstance(agent, FixedAgent):
                continue
            if agent.storage:
                self.seen_food = True
