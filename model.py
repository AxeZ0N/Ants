from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid

class Model(Model):
    '''
    Top level, holds and runs the sim
    '''

    def generate_test_state(self, *args):
        for player in args:
            player.create_agents(
                    self,
                    1,
                    self.grid.empties.select_random_cell().coordinate,
                    )

    def __init__(self,
                 width = 10,
                 height = 10,
                 seed = 1,
                 players = None
                 ): 

        super().__init__( seed = seed )

        self.grid = OrthogonalMooreGrid(
                dimensions = (width, height),
                random = self.random,
                )

        if players is not None:
            self.generate_test_state(*players)

    def step(self):
        agents_list = self.agents_by_type.copy()
        [v.do('step') for k,v in agents_list.items()]
