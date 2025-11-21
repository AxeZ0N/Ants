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
        self.state = "WANDER"

    def step(self):
        """Ants do various things depending on state and position each step."""
        # used_turn = self.AntBrain.handle_curr_cell(self)

        # Step 1: Dispatch based on state
        move_fcn = None
        match self.state:
            case "WANDER":
                move_fcn = self.ant_brain.wander
            case "HOLDING":
                move_fcn = self.ant_brain.holding
            case _: pass

        # Step 2: Update hx and pos
        self.cell = move_fcn(self)
        self.history.append(self.cell)

        # Step 3: Update state dependants
        self.state = self._update_state()
        self.color = self._update_color()

    def _update_color(self):
        match self.state:
            case "WANDER":
                return "red"
            case "HOLDING":
                return "brown"

    def _update_state(self):
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
    def aim_for(ant, target):
        nbrs = list(ant.cell.get_neighborhood())
        cells = []
        for cell in nbrs:
            for agent in cell.agents:
                if isinstance(agent, target):
                    cells.append(cell)
                    break

        if cells:
            return cells.pop()

        poss_next = AntBrain.prune_next(ant)
        return ant.model.random.choice(poss_next)

    @staticmethod
    def wander(ant):
        return AntBrain.aim_for(ant, Food)

    @staticmethod
    def holding(ant):
        return AntBrain.aim_for(ant, Hill)
