class Brain:
    def __init__(self, priority):
        self.priority = priority

    def next_action(self, ant):
        ''' Make a decision based on priority '''
        agents_in_cell = [x for x in ant.cell.agents if x is not ant]
        if not len(agents_in_cell): return None
        # If nothing worth doing, return none
        
        priority = self.priority.copy()

        # Cycle through priority list, dispatch method if seen

        top_prio = priority.pop(0)
        top = [x for x in agents_in_cell if type(x) is not top_prio]
