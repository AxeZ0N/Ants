"""Ants are the main part of the sim"""

from mesa.discrete_space import CellAgent
from agents import Food, Hill, Smell


class Ant(CellAgent):
    """
    Wander around until bumping into food
    """

    is_test = True

    color, size = "red", 100

    # States
    WANDER, HOLDING = "WANDER", "HOLDING"

    def __init__(self, model, coords):
        super().__init__(model)
        self.cell = self.model.grid[coords]
        self.history = [self.cell]
        self.storage = []
        self.ant_brain = AntBrain
        self.state = self.WANDER

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
            case _:
                pass

        # Step 2: Update hx and pos
        self.cell = move_fcn(self)
        self.history.append(self.cell)

        # Step 3: Update state dependants
        self.state = self._update_state()
        self.color = self._update_color()
        self.plot_history()

    def _update_color(self):
        """Internal"""
        match self.state:
            case self.WANDER:
                return "red"
            case self.HOLDING:
                return "brown"

    def _update_state(self):
        """Internal"""
        return self.HOLDING if self.storage else self.WANDER

    def plot_history(self):
        """Place Smell in curr cell"""
        Smell(self.model, self.cell.coordinate)


class AntBrain:
    """This is where most decisions about movement are made"""

    @staticmethod
    def prune_next(ant):
        """Don't offer previously visited cells as options"""
        nbrs = ant.cell.get_neighborhood()
        poss_next = [x for x in nbrs if x not in ant.history]
        return poss_next if poss_next else list(nbrs)

    # Process:
    # Ant tries to walk home.
    # case: Ant has home in history.
    #   Ant looks around and chooses any cell such that
    #       cell in direction of home
    #       cell contains Smell obj
    # case: Ant doesn't have home in history.
    #   Undefined
    # case: Ant has no smells around.
    #   Undefined

    @staticmethod
    def can_go_home(ant):
        """ """
        return [
                cell
                for cell in ant.history
                for agent in cell.agents
                if isinstance(agent, Hill)
                ]

    @staticmethod
    def get_smell_nbrs(ant):
        """ """
        return [
                cell
                for cell in ant.cell.get_neighborhood()
                for agent in cell.agents
                if isinstance(agent, Smell)
                ]

    @staticmethod
    def _select_cells(possible, validation_fcn):
        return [
                cell
                for cell in possible
                if validation_fcn(cell)
                ]

    @staticmethod
    def go_home(ant):
        valid = lambda cell: cell in ant.history
        possible = ant.cell.get_neighborhood()

        next_step = AntBrain._select_cells(possible, valid)
        
        return next_step if next_step else list(possible)

    @staticmethod
    def prune_next(ant):
        valid = lambda cell: cell not in ant.history
        possible = ant.cell.get_neighborhood()

        next_step = AntBrain._select_cells(possible, valid)
        
        return next_step if next_step else list(possible)

    @staticmethod
    def aim_for(ant, target):
        """Return cell if avail"""
        for cell in ant.cell.get_neighborhood():
            for agent in cell.agents:
                if isinstance(agent, target):
                    return cell

        return ant.model.random.choice(AntBrain.prune_next(ant))

    @staticmethod
    def wander(ant):
        """Return Food if avail"""
        return AntBrain.aim_for(ant, Food)

    @staticmethod
    def holding(ant):
        """Return Hill if avail"""
        return AntBrain.aim_for(ant, Hill)
