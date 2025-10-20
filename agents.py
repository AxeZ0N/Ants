from mesa.discrete_space import CellAgent, Cell

class Ant(CellAgent):
    def __init__(self, model, coords):
        super().__init__( model )
        self.cell = self.model.grid[coords]
