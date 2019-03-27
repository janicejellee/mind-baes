class Mind:
    def __init__(self):
        # where resources are
        self.world = [(10,0), (0,9), (6,10)] # can be initialized, but will just set here
        self.map_length = 15
        self.actual_world = 'ABC'

        # possible assignments to world
        self.beliefs_worlds = ['ABC', 'ACB', 'BAC', 'BCA', 'CAB', 'CBA']

        # belief that the orientation is the above
        self.beliefs = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
        self.intents = {'A': 1/3,
                        'B': 1/3,
                        'C': 1/3}
        self.transition_matrix = []
        self.prev_position = (0,0)
        self.position = (0,0)


    # the entire model pretty much runs here. this calls the other functions
    def receive_observation(self, x, y):
        self.position = (x,y)
        near_locations = self.within_range((x,y))
        # print ("LOC")
        # print ((x,y))
        # print (near_locations)
        for loc in near_locations:
            i = self.world.index(loc)
            resource = self.actual_world[i]
            point = (x,y)
            self.update_beliefs(loc, resource)

        # update transition
        self.update_transition_matrix()

        # update intents
        self.update_intents()

        self.prev_position = (x,y)


    # gets the probabilities you are looking for resource x at location y based on current position and prev position
    def update_transition_matrix(self):
        dists = []

        for resource_pos in self.world:
            dist1 = self.get_distance(resource_pos, self.prev_position)
            dist2 = self.get_distance(resource_pos, self.position)
            diff_dist = dist1-dist2
            dists.append(diff_dist)

        # -2 2 2  R1 R2 R3
        # 2, 6, 6
        # 2/14, 6/14, 6/14

        max_value = max(dists)
        min_value = min(dists)
        range_values = max_value - min_value

        # so there are no negatives
        # print (dists)
        for i in range(len(dists)):
            dists[i] += range_values
        # print (dists)
        # print ("------")
        probabilities = []
        for d in dists:
            probabilities.append(d/sum(dists))

        self.transition_matrix = probabilities


    # helper to get distance
    def get_distance(self, p1, p2):
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5


    # helper to get resource locations that can be seen by mark (he can see a resource if
    # he's within the 5 by 5 block where the resource is at the center)
    def within_range(self, position):
        # should return resource positions that are visible from current position
        locs = []
        for i in range(len(self.world)):
            loc = self.world[i]
            # print ("---")
            # print (position)
            # print (loc)
            # print (abs(position[0]-loc[0])<=5)
            # print ("---")
            if abs(position[0]-loc[0])<=5 and abs(position[1]-loc[1])<=5:
                locs.append(loc)
        return locs


    # updates belief in the possible arrangements of resources in world
    def update_beliefs(self, position, resource):
        # update beliefs when world becomes discovered
        i = self.world.index(position)
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


    # updates intents
    def update_intents(self):
        # based on belief, transition, old intents, and rewards
        scores = {'A': 0, 'B': 0, 'C': 0}
        for i in range(len(self.beliefs_worlds)):
            world = self.beliefs_worlds[i]
            belief_prob = self.beliefs[i]
            for i in range(3):
                resource = world[i]
                trans_prob = self.transition_matrix[i]
                score = belief_prob * trans_prob * self.reward(resource)
                scores[resource] += score

        scores_list = []
        for i in scores:
            scores_list.append(scores[i])


        max_score = max(scores_list)
        min_score = min(scores_list)
        range_values = max_score - min_score

        for i in scores:
            scores[i] += range_values

        sum_scores = scores['A'] + scores['B'] + scores['C']

        new_intents = {}
        for s in scores:
            new_intents[s] = scores[s] / sum_scores

        self.intents = new_intents


    # reward function that gives reward for pretty much just collecting since
    # we took off 'marking' locations for later
    def reward(self, resource):
        return 100 * self.intents[resource]


    # later: visualizationy stuffz

my_mind = Mind()

# goes to A, then C
# print (my_mind.intents)
# my_mind.receive_observation(1, 0)
# print (my_mind.intents)
# my_mind.receive_observation(2, 0)
# print (my_mind.intents)
# my_mind.receive_observation(3, 0)
# print (my_mind.intents)
# my_mind.receive_observation(4, 0)
# print (my_mind.intents)
# my_mind.receive_observation(5, 0)
# my_mind.receive_observation(6, 0)
# # my_mind.receive_observation(7, 0)
# # my_mind.receive_observation(8, 0)
# print (my_mind.intents)
# my_mind.receive_observation(6, 1)
# print (my_mind.intents)
# my_mind.receive_observation(6, 2)
# my_mind.receive_observation(6, 3)
# my_mind.receive_observation(6, 4)
# my_mind.receive_observation(6, 5)
# my_mind.receive_observation(6, 6)
# print (my_mind.intents)

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

my_mind = Mind()
my_mind.receive_observation(1, 0)
print (my_mind.intents)
my_mind.receive_observation(2, 0)
print (my_mind.intents)
my_mind.receive_observation(3, 0)
print (my_mind.intents)
my_mind.receive_observation(4, 0)
print (my_mind.intents)
my_mind.receive_observation(5, 0)
print (my_mind.intents)
my_mind.receive_observation(6, 0)
print (my_mind.intents)
my_mind.receive_observation(5, 0)
print (my_mind.intents)
my_mind.receive_observation(4, 0)
print (my_mind.intents)
my_mind.receive_observation(3, 0)

print ("done")
