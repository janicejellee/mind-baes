import math

class Mind:
    def __init__(self):
        # where resources are
        self.world_loc = [(10,0), (0,9), (6,10)] # can be initialized, but will just set here
        self.map_length = 15
        self.world_state = 'ABC'

        # possible assignments to world
        self.beliefs_worlds = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']
        # belief that the orientation is the above
        self.beliefs = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

        self.intents = {'A': 1/3,
                        'B': 1/3,
                        'C': 1/3}

        epsilon_trans = 0.001
        self.state_transitional_prob = 1 - epsilon_trans
        self.prev_position = (0,0)
        self.position = (0,0)


    # the entire model pretty much runs here. this calls the other functions
    def receive_observation(self, x, y):
        self.position = (x,y)
        near_locations = self.within_range((x,y))
        for loc in near_locations:
            i = self.world_loc.index(loc)
            resource = self.world_state[i]
            point = (x,y)
            self.update_beliefs(loc, resource)

        # update intents
        self.update_intents()
        self.prev_position = (x,y)


    # helper to get distance
    def get_distance(self, p1, p2):
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5


    # helper to get resource locations that can be seen by mark (he can see a resource if
    # he's within the 5 by 5 block where the resource is at the center)
    def within_range(self, position):
        # should return resource positions that are visible from current position
        locs = []
        for i in range(len(self.world_loc)):
            loc = self.world_loc[i]
            if abs(position[0]-loc[0])<=5 and abs(position[1]-loc[1])<=5:
                locs.append(loc)
        return locs


    # updates belief in the possible arrangements of resources in world
    # takes into account that observation of a resource being at a location is 100%, by adjusting
    # the beliefs based on current value
    def update_beliefs(self, position, resource):
        # update beliefs when world becomes discovered
        i = self.world_loc.index(position)
        increasing_beliefs = []
        decreasing_beliefs = []
        for j in range(len(self.beliefs_worlds)):
            world = self.beliefs_worlds[j]
            if world[i] == resource:
                increasing_beliefs.append(j)
            else:
                decreasing_beliefs.append(j)

        # decrease belief in other worlds by half
        sum_decrease_beliefs = 0
        for b in decreasing_beliefs:
            self.beliefs[b] /= 2
            sum_decrease_beliefs += self.beliefs[b]

        # increase belief in that world by w/e leftover
        leftover = 1-sum_decrease_beliefs
        increasing_each = leftover / len(increasing_beliefs)
        for b in increasing_beliefs:
            self.beliefs[b] += increasing_each


    def softmax(self, inputs):
        exps = [math.exp(i) for i in inputs]
        sum_of_exps = sum(exps)
        softmax = [j/sum_of_exps for j in exps]
        return softmax


    # gives value, based on agent belief and state (position), the value
    def value(self):
        dists = []

        for resource_pos in self.world_loc:
            dist1 = self.get_distance(resource_pos, self.prev_position)
            dist2 = self.get_distance(resource_pos, self.position)
            diff_dist = dist1-dist2
            dists.append(diff_dist)

        softmax_dists = self.softmax(dists)
        values = [j*1 for j in softmax_dists]
        return values


    # updates intents, softmax function on Q^LA, the state-action value function
    def update_intents(self):
        sa_values = {'A': 0, 'B': 0, 'C': 0}
        value_function = self.value()
        for i in range(len(self.beliefs_worlds)):
            world = self.beliefs_worlds[i]
            belief_prob = self.beliefs[i]
            for i in range(3):
                resource = world[i]
                score = belief_prob * self.state_transitional_prob * (self.reward(resource) + value_function[i])
                sa_values[resource] += score

        values = [sa_values['A'], sa_values['B'], sa_values['C']]
        values_softmax = self.softmax(values)

        new_intents = {'A': values_softmax[0], 'B': values_softmax[1], 'C': values_softmax[2]}
        self.intents = new_intents


    # reward function that gives reward for pretty much just collecting since
    def reward(self, resource):
        return 1 * self.intents[resource]


my_mind = Mind()

# goes to A, then C
print (my_mind.intents)
my_mind.receive_observation(1, 0)
print (my_mind.intents)
my_mind.receive_observation(2, 0)
print (my_mind.intents)
my_mind.receive_observation(3, 0)
print (my_mind.intents)
my_mind.receive_observation(4, 0)
print (my_mind.intents)
my_mind.receive_observation(5, 0)
my_mind.receive_observation(6, 0)
# my_mind.receive_observation(7, 0)
# my_mind.receive_observation(8, 0)
print (my_mind.intents)
my_mind.receive_observation(6, 1)
print (my_mind.intents)
my_mind.receive_observation(6, 2)
my_mind.receive_observation(6, 3)
my_mind.receive_observation(6, 4)
my_mind.receive_observation(6, 5)
my_mind.receive_observation(6, 6)
print (my_mind.intents)

# goes to A but changes mind
# print (my_mind.intents)
# my_mind.receive_observation(1, 0)
# print (my_mind.intents)
# my_mind.receive_observation(2, 0)
# print (my_mind.intents)
# my_mind.receive_observation(3, 0)
# print (my_mind.intents)
# my_mind.receive_observation(4, 0)
# my_mind.receive_observation(5, 0)
# my_mind.receive_observation(6, 0)
# print (my_mind.intents)
# my_mind.receive_observation(5, 0)
# print (my_mind.intents)
# my_mind.receive_observation(4, 0)
# my_mind.receive_observation(3, 0)
# print (my_mind.intents)


print ("done")
