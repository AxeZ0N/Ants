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

        self.base_cell = cell_haver.cell
        self.nbr_cells = self.base_cell.get_neighborhood() or []
        self.all_agents = AgentSet(
            self.nbr_cells.agents, random=cell_haver.model.random
        )

    def sort_agents_by(self, attr):
        """Returns all agents in nbrs, sorted by attr."""
        if not self.all_agents:
            return []

        return sorted(self.all_agents, key=lambda x: getattr(x, attr))

    def sort_cells_by(self, type_):
        """Returns only cells that contain type_"""

        assert isinstance(type_, type)

        return (
            agent.cell
            for cell in self.nbr_cells
            for agent in cell.agents
            if isinstance(agent, type_)
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
    WANDER, HOLDING, FOLLOW = "WANDER", "HOLDING", "FOLLOW"
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
            case self.HOLDING:
                next_cell = self.holding()
            case self.FOLLOW:
                next_cell = self.follow()

        # print(self.state)
        self.drop_scent()
        self.cell = next_cell

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

    def wander(self):
        """Steers ants towards unvisited cells & towards food"""

        def filter_by_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: any(isinstance(agt, type_) for agt in x.agents)
            )
            return type_only

        def filter_by_not_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: not any(
                    isinstance(agt, type_) for agt in x.agents
                )
            )
            return type_only

        # Get possible next cells
        poss_next = self.cell.get_neighborhood()

        # Filter by Food (if avail)
        food_only = filter_by_type(agents.Food)

        # Try to choose a cell
        if food_only:
            return food_only.select_random_cell()

        # Second best choice
        no_smells = filter_by_not_type(agents.Smell)

        # Try to choose a cell
        if no_smells:
            return no_smells.select_random_cell()

        # Fallback, choose randomly
        return poss_next.select_random_cell()

    def holding(self):
        """Guides ant backwards towards hill"""

        def filter_by_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: any(isinstance(agt, type_) for agt in x.agents)
            )
            return type_only

        def filter_by_not_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: not any(
                    isinstance(agt, type_) for agt in x.agents
                )
            )
            return type_only

        # Get possible next cells
        poss_next = self.cell.get_neighborhood()

        # Filter by Hill (if avail)
        hills = filter_by_type(agents.Hill)

        if hills:
            return hills.select_random_cell()

        # Filter by Smell, second best choice
        smells_only = filter_by_type(agents.Smell)

        if smells_only:
            # Should choose oldest smell avail

            class DummySmell:
                age = 0

            oldest_smell = DummySmell

            for smell in chain(*[x.agents for x in smells_only]):
                if not isinstance(smell, agents.Smell):
                    continue

                if smell.age > oldest_smell.age:
                    oldest_smell = smell

            # print(oldest_smell.cell)

            return oldest_smell.cell

        # Fallback, choose randomly
        return poss_next.select_random_cell()

    def follow(self):
        """Guides ant to previously found Food"""

        def filter_by_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: any(isinstance(agt, type_) for agt in x.agents)
            )
            return type_only

        def filter_by_not_type(type_):
            type_only = poss_next.select(
                filter_func=lambda x: not any(
                    isinstance(agt, type_) for agt in x.agents
                )
            )
            return type_only

        # Get possible next cells
        poss_next = self.cell.get_neighborhood()

        # Go to food if it's there
        food = filter_by_type(agents.Food)

        if food:
            return food.select_random_cell()

        # Filter by Smell
        smells_only = filter_by_type(agents.Smell)

        # Filter by Smell:seen_food
        smell_cell_agents = chain(*[cell.agents for cell in smells_only])

        seen_food_only = [
            smell
            for smell in smell_cell_agents
            if isinstance(smell, agents.Smell) and smell.seen_food
        ]

        if seen_food_only:

            class DummySmell:
                age = 999

            youngest_smell = DummySmell

            for smell in seen_food_only:
                if not isinstance(smell, agents.Smell):
                    continue

                if smell.age < youngest_smell.age:
                    youngest_smell = smell

            return youngest_smell.cell

        self.state = self.WANDER

        # Fallback, choose randomly
        return poss_next.select_random_cell()
