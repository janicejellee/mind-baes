class Mind:
    def __init__(self, world, items):
        # where resources are
        self.world = [(4,9), (10,5), (8,10)] # can be initialized, but will just set here
        self.map_length = 15
        self.actual_world = 'ABC'

        # possible assignments to world
        self.beliefs_worlds = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']

        # belief that the orientation is the above
        self.beliefs = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
        self.intents = {'A': .5,
                        'B': .5,
                        'C': .5}
        self.transition_matrix = []
        self.prev_position = (0,0)

    # the entire model pretty much runs here. this calls the other functions
    def receive_observation(self, direction, x, y, action):
        if (x,y) in self.world:
            i = self.world.index((x,y))
            resource = self.actual_world[i]
            self.update_beliefs((x,y), resource)

        # get transition
        transition = get_trasition_matrix(self, position)

        # update intents
        # TODO

        self.prev_position = (x,y)

    # gets the probabilities you are looking for resource x at location y based on current position and prev position
    def get_transition_matrix(self, position):
        dists = []

        for resource_pos in self.world:
            dist1 = self.get_distance(resource_pos, prev_position)
            dist2 = self.get_distance(resource_pos, position)
            diff_dist = dist2-dist1
            dists.append(diff_dist)

        max_value = max(dists)
        min_value = min(dists)
        range_values = max_value - min_value

        # so there are no negatives
        for d in dists:
            d += range_values

        probabilities = []
        for d in dists:
            probabilities.append(d/sum(d))

        return probabilities

    # helper to get distance
    def get_distance(self, p1, p2):
        return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    # helper to get resources that can be seen by mark (he can see a resource if
    # he's within the 5 by 5 block where the resource is at the center)
    def within_range(self, position):
        # should return resource positions that are visible from current position
        resources = []
        for i in range(len(self.world)):
            loc = self.world[i]
            resource = self.actual_world[i]
            if abs(position[0]-loc[0])<=5 or abs(position[1]-loc[1]<=5):
                resources.append(resource)
        return resources

    # updates belief in the possible arrangements of resources in world
    def update_beliefs(self, position, resource):
        # update beliefs when world becomes discovered
        i = self.world.index((x,y))
        for world in self.belief_worlds:
            if world[i] == resource:
                # TODO increase belief in that world
        # TODO decrease belief in other worlds

    # updates intents... the final thing we want to get
    def update_intents(self):
        # based on belief, transition, old intents, and rewards
        # TODO

    # reward function that gives reward for pretty much just collecting since
    # we took off 'marking' locations for later
    def reward(self, resource):
        return 100 * self.intents[resource][0]


    # later: visualizationy stuffz
