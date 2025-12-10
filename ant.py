"""Ants are the main part of the sim"""

from dataclasses import dataclass
from itertools import chain

from mesa.discrete_space import CellAgent, CellCollection
from mesa.agent import AgentSet

import agents


class MyCellAgent(CellAgent):
    """Helper"""

    def __init__(self, model, cell=None):
        super().__init__(model)
        self.cell = cell
        self.age = 0
        self.max_age = 9e999

    def _age(self):
        """ """
        self.age += 1
        if self.age > self.max_age:
            self.remove()


@dataclass
class Coord:
    """Class for manipulating xy coords"""

    x: int
    y: int

    def __add__(self, target):
        return self.x + target.x, self.y + target.y

    def __sub__(self, target):
        return self.x - target.x, self.y - target.y


def retrace_ant_steps(ant):
    start_cell = ant.cell.coordinate
    curr_cell = start_cell
    ret = []
    for delta in reversed(ant.history):
        print(f"Curr cell: {curr_cell}")
        print(f"Next delta: {delta}")

        curr_cell = Coord(*curr_cell) + Coord(*delta)

        ret.append(curr_cell)

    return


class CellChoices:
    """Helps with stuff for decisions about next step"""

    def __init__(self, cell_haver):

        self.base = cell_haver
        self.base_cell = cell_haver.cell
        self.nbr_cells = self.base_cell.get_neighborhood() or []
        self.all_agents = AgentSet(
            self.nbr_cells.agents, random=cell_haver.model.random
        )

    def sort_agents_by(self, attr, agents_to_sort=None):
        """Returns all agents in nbrs, sorted by attr."""
        if agents_to_sort is None:
            agents_to_sort = self.all_agents

        return AgentSet(sorted(agents_to_sort, key=lambda x: getattr(x, attr)))

    def sort_cells_by(self, type_, cells_to_sort=None):
        """Returns only cells that contain type_"""

        assert isinstance(type_, type)

        if cells_to_sort is None:
            cells_to_sort = self.nbr_cells

        return CellCollection(
            (
                agent.cell
                for cell in cells_to_sort
                for agent in cell.agents
                if isinstance(agent, type_)
            ),
            random=self.base.model.random,
        )


class Ant(MyCellAgent):
    """
    Wander around until bumping into food

    While in state WANDER:
        Ants prefer Food.
        Ants avoid Smells.

    While in state HOLDING:
        Ants prefer Home -> Smells.
        Ants avoid Food.

    While in state FOLLOW:
        Ants prefer Food -> Smells.

    """

    color, size = "red", 20
    WANDER, HOLD, FOLLOW = "WANDER", "HOLDING", "FOLLOW"
    DEFAULT_STATE = WANDER

    def __init__(self, model, cell=None):
        """ """
        super().__init__(model, cell)
        self.history = []
        self.storage = []
        self.state = Ant.DEFAULT_STATE

    def step(self):
        """Called in each iteration of the model"""
        match self.state:
            case self.WANDER:
                next_cell = self.wander()
            case self.HOLD:
                next_cell = self.hold()
            case self.FOLLOW:
                next_cell = self.follow()

        # print(self.state)
        self.drop_scent()
        self.cell = next_cell
        self._age()

    def drop_scent(self):
        """Helps the ant remember where it's been"""

        for agent in self.cell.agents:
            if isinstance(agent, agents.Smell):
                return

        smell = agents.Smell(
            model=self.model,
            cell=self.cell,
        )

        self.history.append(smell)

    def hold(self):
        """Hill -> Oldest Smell in HX -> Oldest Smell -> Panic"""

        # Worst case
        all_nbrs = self.cell.get_neighborhood()

        cell_chooser = CellChoices(self)

        # Sort by hill
        hill_cells = cell_chooser.sort_cells_by(agents.Hill)
        if hill_cells:
            return hill_cells.select_random_cell()

        # Sort by age
        smell_cells = cell_chooser.sort_cells_by(agents.Smell)
        sorted_smells = cell_chooser.sort_agents_by(
            agents_to_sort=smell_cells.agents,
            attr="age",
        )

        # Filter by cells in HX
        smells_in_history = [smell for smell in sorted_smells if smell in self.history]

        if smells_in_history:
            # Pop the HX smell so we don't backtrack
            oldest = smells_in_history[-1].cell
            self.history.pop(self.history.index(oldest))
            return oldest

        # Otherwise, return oldest smell
        if sorted_smells:
            return sorted_smells[-1].cell

        # Worst case
        return all_nbrs.select_random_cell()

    def wander(self):
        """Food -> None -> Smell"""

        # Worst case
        all_nbrs = self.cell.get_neighborhood()

        cell_chooser = CellChoices(self)

        # If food, move there
        food_nbrs = cell_chooser.sort_cells_by(agents.Food)
        if food_nbrs:
            return food_nbrs.select_random_cell()

        # Get smells only
        # Subtract smell cells from all cells
        smell_nbrs = cell_chooser.sort_cells_by(agents.Smell)

        no_smell_cells = CellCollection(
            set(all_nbrs).difference(smell_nbrs),
            random=self.model.random,
        )

        if no_smell_cells:
            return no_smell_cells.select_random_cell()

        # Worst case
        return all_nbrs.select_random_cell()
