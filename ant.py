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
        self.state = 'WANDER'

    def step(self):
        """Ants do various things depending on state and position each step."""
        #used_turn = self.AntBrain.handle_curr_cell(self)

        # Step 1: Dispatch based on state
        move_fcn = None
        match self.state:
            case "WANDER": move_fcn = self.ant_brain.wander
            case "HOLDING": move_fcn = self.ant_brain.holding

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
            self.cell = self.model.random.choice(next_step)
            self.history.append(self.cell)

        if self.storage:
            self.color = "brown"
        else:
            self.color = "red"

        self.state = self.update_state()

    def update_state(self):
        return "WANDER" if not self.state else "HOLDING"

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
    def prune_next(ant):
        """Don't offer previously visited cells as options"""
        self = ant
        next_step = [x for x in self.cell.get_neighborhood() if x not in self.history]
        if not next_step:
            next_step = list(self.cell.get_neighborhood())
        return next_step


    @staticmethod
    def wander(ant):
        pass

    @staticmethod
    def holding(ant):
        pass
