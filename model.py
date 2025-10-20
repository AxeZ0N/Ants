from mesa import Model
from mesa.discrete_space import OrthogonalMooreGrid

class Model(Model):
    '''
    Top level, holds and runs the sim
    '''
    def __init__(self,
                 width = 1,
                 height = 1,
                 seed = 1
                 ): 

        super().__init__( seed = seed )

        self.grid = OrthogonalMooreGrid(
                dimensions = (width,height),
                random = self.random,
                )

    def step(self):
        agents_list = self.agents_by_type.copy()
        [v.do('step') for k,v in agents_list.items()]
