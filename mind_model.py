class Mind:
    def __init__(self, world, items):
        # where resources are
        self.world = [(5,5), (6,1), (1,8)] # can be initialized, but will just set here
        self.actual_world = 'ABC'

        # possible assignments to world
        self.beliefs_worlds = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']

        # belief that the orientation is the above
        self.beliefs = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

        # need now, need later, do not need
        self.intents = {'A': [1/3, 1/3, 1/3],
                        'B': [1/3, 1/3, 1/3],
                        'C': [1/3, 1/3, 1/3]}

        # this is not done yet, but how likely you are trying to reach a resource if you walk from __ direction
        self.transition_matrix = []
        # for i in range(10):
        #     row_transitions = []
        #     for j in range(10):
        #         row_transitions.append({'up':,
        #         'down': ,
        #         'left': ,
        #         'right': })
        #     self.transition_matrix.append(row_transitions)

        self.time = 0 # don't know if needed...
        self.current_position = (0,0)
        self.current_direction = 'up'
        self.current_action = action # collect or pass

    def receive_observation(self, direction, x, y, action):
        self.current_position = (x,y)
        self.current_direction = direction
        self.current_action = action

        if (x,y) in self.world:
            i = self.world.index((x,y))
            resource = self.actual_world[i]
            self.update_beliefs((x,y), resource)

        # call update_transition_matrix

        # call update_intents

    def update_transition_matrix(self):
        # TODO

    def update_beliefs(self, position, resource):
        # update beliefs when world becomes discovered
        i = self.world.index((x,y))
        for world in self.belief_worlds:
            if world[i] == resource:
                # TODO increase belief in that world
        # TODO decrease belief in other worlds

    def update_intents(self):
        # based on transition, old intents, and rewards
        # TODO

    def reward(self, resource, action):
        if action == 'collect':
            return 100 * self.intents[resource][0]
        else if action == 'mark':
            return 50 * self.intents[resource][1]
        return 0

    # later: visualizationy stuffz
