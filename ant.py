from mesa.discrete_space import CellAgent, FixedAgent
from agents import Food, Hill, Smell

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
        self.ant_brain = AntBrain

    def step(self):
        """Ants do various things depending on state and position each step."""
        #used_turn = self.AntBrain.handle_curr_cell(self)

        next_step = self.ant_brain.prune_next(self)
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
        if not self.ant_brain.handle_standing_on(self):
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



class AntBrain:
    @staticmethod
    def handle_curr_cell(ant):
        self = ant
        if self.storage:
            ret = self.ant_brain.handle_with_food(self)

        keys = [type(agent) for agent in self.cell.agents]

        my_dict = {k: [] for k in keys}

        {my_dict[type(agent)].append(agent) for agent in self.cell.agents}

        # print(my_dict)

    @staticmethod
    def handle_standing_on(ant):
        """Handles interactions with agents in the same cell"""
        self = ant

        def erase_hx():
            for cell in self.history:
                for agent in cell.agents:
                    if isinstance(agent, Smell):
                        agent.lifetime = 0
                        print("SMELL")
                        break

            self.history = []

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
                    erase_hx()
                    if self.is_test:
                        print("I'm an ant, and I stored some food!")
                    return 1
        return 0

    @staticmethod
    def prune_next(ant):
        """Don't offer previously visited cells as options"""
        self = ant
        next_step = [x for x in self.cell.get_neighborhood() if x not in self.history]
        if not next_step:
            next_step = list(self.cell.get_neighborhood())
        return next_step
