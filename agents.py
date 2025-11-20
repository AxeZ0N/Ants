"""
Things that live in the model
"""

from mesa.discrete_space import CellAgent, FixedAgent


class Ant(CellAgent):
    """
    Wander around until bumping into food
    """

    is_test = True

    color, size = "red", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.history = [self.cell]
        self.storage = []
        self.AntBrain = __AntBrain__

    def step(self):
        """Ants do various things depending on state and position each step."""
        used_turn = self.AntBrain.handle_curr_cell(self)

        next_step = self.AntBrain.prune_next(self)
        new = []
        for cell in next_step:
            for agent in cell.agents:
                if issubclass(type(agent), Food) and not self.storage:
                    new.append(cell)
                    continue
            for agent in cell.agents:
                if issubclass(type(agent), Hill) and self.storage:
                    new.append(cell)
                    continue

        if new:
            next_step = new
        if not self.AntBrain.handle_standing_on(self):
            if self.is_test:
                self.plot_history()
                print(f"I'm an ant, choosing from {len(next_step)} cells!")
            self.cell = self.model.random.choice(next_step)
            self.history.append(self.cell)

        if self.storage:
            self.color = "brown"
        else:
            self.color = "red"

    def plot_history(self):
        Smell(self.model, self.cell.coordinate)


class Smell(FixedAgent):
    color, size = "green", 40

    def __init__(self, model, coords, **kwargs):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []
        self.lifetime = kwargs.get("lifetime", 8888)

    def step(self):
        if self.lifetime <= 0:
            self.remove()
        else:
            self.lifetime -= 1


class __AntBrain__:
    @staticmethod
    def handle_curr_cell(self):
        if self.storage:
            ret = self.AntBrain.handle_with_food(self)

        keys = [type(agent) for agent in self.cell.agents]

        my_dict = {k: [] for k in keys}

        {my_dict[type(agent)].append(agent) for agent in self.cell.agents}

        # print(my_dict)

    def handle_with_food(self):
        pass

    @staticmethod
    def handle_standing_on(self):
        """Handles interactions with agents in the same cell"""
        for agent in self.cell.agents:
            if issubclass(type(agent), Food):
                if not self.storage:
                    self.storage.append(agent)
                    if self.is_test:
                        print("I'm an ant, and I grabbed some food!")
                    return 1
            if issubclass(type(agent), Hill):
                if self.storage:
                    agent.storage.append(self.storage.pop())
                    for cell in self.history:
                        for agent in cell.agents:
                            if isinstance(agent, Smell):
                                agent.lifetime = 0
                                print("SMELL")
                    self.history = []
                    if self.is_test:
                        print("I'm an ant, and I stored some food!")
                    return 1
        return 0

    @staticmethod
    def prune_next(self):
        """Don't offer previously visited cells as options"""
        next_step = [x for x in self.cell.get_neighborhood() if x not in self.history]
        if not next_step:
            next_step = list(self.cell.get_neighborhood())
        return next_step


class Hill(FixedAgent):
    """
    Ants return food to home
    """

    color, size = "brown", 200

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []


class Food(FixedAgent):
    """
    Ants grab a Chunk of Food and carry it home
    """

    color, size = "orange", 100

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.storage = []
