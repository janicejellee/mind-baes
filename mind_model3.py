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

        # self.intents = {'A': 1/3,
        #                 'B': 1/3,
        #                 'C': 1/3}

        self.intents = {'A': 0.05,
                        'B': 0.09,
                        'C': 0.05}
        # how certain we are of current state
        epsilon_obs = 0.001
        self.observation_distribution_prob = 1 - epsilon_obs

        self.state = (0,0)

        self.states = []
        for i in range(self.map_length):
            for j in range(self.map_length):
                self.states.append((i,j))

        self.gamma = 0.9

    def reward(self, state, world):
        "Return a numeric reward for this state."
        if (state in self.world_loc):
            i = self.world_loc.index(state)
            resource = world[i]
            return 10*self.intents[resource]
        else:
            return -1

    def get_next_state(self, state, action):
        """
        Helper function. Given state and action, gives next state that would
        be reached. Returns None if off map.
        """
        next_state = None
        x = state[0]
        y = state[1]

        if action == 'right':
            if 0<=(x+1)<self.map_length and 0<=y<self.map_length:
                next_state = (x+1,y)
        elif action == 'left':
            if 0<=(x-1)<self.map_length and 0<=y<self.map_length:
                next_state = (x-1,y)
        elif action == 'up':
            if 0<=x<self.map_length and 0<=(y-1)<self.map_length:
                next_state = (x,y-1)
        elif action == 'down':
            if 0<=x<self.map_length and 0<=(y+1)<self.map_length:
                next_state = (x,y+1)

        return next_state

    def transition(self, state, action):
        """
        Transition model.  From a state and an action, return a list
        of (result-state, probability) pairs.
        """
        actions = self.actions(state)
        pairs = []

        action_valid = False
        next_state = self.get_next_state(state, action)

        x = state[0]
        y = state[1]

        if next_state:
            pairs.append((next_state, 0.9))
            remaining = len(actions) - 1
            prob = 0.1 / remaining
            for a in actions:
                if a != action:
                    pairs.append((self.get_next_state(state, a), prob))
        else:
            prob = 1.0 / len(actions)
            for a in actions:
                pairs.append((self.get_next_state(state, a), prob))

        # print (pairs)
        return pairs

    def actions(self, state):
        "Set of actions that can be performed in this state."
        actions = []
        x = state[0]
        y = state[1]

        if 0<=(x+1)<self.map_length and 0<=y<self.map_length:
            actions.append('right')
        if 0<=(x-1)<self.map_length and 0<=y<self.map_length:
            actions.append('left')
        if 0<=x<self.map_length and 0<=(y-1)<self.map_length:
            actions.append('up')
        if 0<=x<self.map_length and 0<=(y+1)<self.map_length:
            actions.append('down')

        return actions

    def within_range(self, position):
        """
        Helper to get resource locations that can be seen by mark (he can see a resource if
        he's within the 5 by 5 block where the resource is at the center)
        Should return resource positions that are visible from current state.
        """
        locs = []
        for i in range(len(self.world_loc)):
            loc = self.world_loc[i]
            if abs(position[0]-loc[0])<=5 and abs(position[1]-loc[1])<=5:
                locs.append(loc)
        return locs

    def beliefs_update(self, state):
        "Update beliefs"
        near_locations = self.within_range(state)
        for loc in near_locations:
            i = self.world_loc.index(loc)
            resource = self.world_state[i]

            increasing_beliefs = []
            decreasing_beliefs = []
            for j in range(len(self.beliefs_worlds)):
                world = self.beliefs_worlds[j]
                if world[i] == resource:
                    increasing_beliefs.append(j)
                else:
                    decreasing_beliefs.append(j)

            # increase belief in worlds
            sum_increase_beliefs = 0
            for b in increasing_beliefs:
                self.beliefs[b] *= 2
                sum_increase_beliefs += self.beliefs[b]
            # print ("increasing ", increasing_beliefs)

        new_beliefs = []
        for b in self.beliefs:
            new_beliefs.append(b/sum(self.beliefs))

        self.beliefs = new_beliefs

    def value_iteration(self, state, epsilon=0.001):
        "Solving by value iteration."
        # TODO check that beliefs part of eqn was added correctly?

        actions = self.actions(state)
        next_states = []
        for a in actions:
            next_states.append(self.get_next_state(state, a))

        U1 = dict([(s, 0) for s in self.states])
        R, T, gamma = self.reward, self.transition, self.gamma

        for i in range(10):
            U = U1.copy()
            delta = 0
            for w_i in range(len(self.beliefs_worlds)):
                for s in self.states:
                    # self.beliefs[w_i] *
                    U1[s] = R(s, self.beliefs_worlds[w_i]) + gamma * max([sum([self.beliefs[w_i] * p * U[s1] for (s1, p) in T(s, a)])
                                                for a in self.actions(s)])
                    delta = max(delta, abs(U1[s] - U[s]))
            if delta < epsilon * (1 - gamma) / gamma:
                 return U
        return U

    def best_policy(self, U):
        """
        Given an MDP and a utility function U, determine the best policy,
        as a mapping from state to action.
        """
        pi = {}
        for s in self.states:
            pi[s] = self.argmax(self.actions(s), lambda a:self.expected_utility(a, s, U))
        return pi

    def argmax(self, keys, f):
        "Helper function to get argmax."
        return max(keys, key=f)

    def expected_utility(self, action, state, U):
        "The expected utility of doing a in state s, according to the MDP and U."
        return sum([p * U[s1] for (s1, p) in self.transition(state, action)])

    def get_distance(self, p1, p2):
        "Helper to get distance."
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**.5

    def softmax(self, inputs):
        "Helper to softmax."
        exps = [math.exp(i) for i in inputs]
        sum_of_exps = sum(exps)
        softmax = [j/sum_of_exps for j in exps]
        return softmax

    def intents_update(self, policy):
        "Update intents."
        # TODO get intents based on the best policy?
        best_action = policy[self.state]
        print (best_action)
        next_state = self.get_next_state(self.state, best_action)

        dists = []

        for resource_pos in self.world_loc:
            dist1 = self.get_distance(resource_pos, self.state)
            dist2 = self.get_distance(resource_pos, next_state)
            diff_dist = dist1-dist2
            dists.append(diff_dist)
        print (dists)
        max_value = max(dists)
        min_value = min(dists)
        range_values = max_value - min_value

        for i in range(len(dists)):
            dists[i] += range_values

        # probabilities A,B,C is in location 0,1,2
        probs = [{'A': 0, 'B': 0, 'C': 0},
                 {'A': 0, 'B': 0, 'C': 0},
                 {'A': 0, 'B': 0, 'C': 0}]

        for i in range(len(self.beliefs_worlds)):
            world = self.beliefs_worlds[i]
            for j in range(3):
                resource = world[j]
                probs[j][resource] += self.beliefs[i]

        scores = [0, 0, 0]
        for i in range(3):
            prob = probs[i]
            scores[0] += dists[i] * prob['A']
            scores[1] += dists[i] * prob['B']
            scores[2] += dists[i] * prob['C']
        self.intents = {'A': scores[0]/sum(scores), 'B': scores[1]/sum(scores), 'C': scores[2]/sum(scores)}

    def receive_observation(self, action):
        "Receive observation and get updated intents."
        print ("------")
        self.state = self.get_next_state(self.state, action)
        self.beliefs_update(self.state)
        U = self.value_iteration(self.state)
        policy = self.best_policy(U)
        print (self.state)
        # print (policy)
        self.intents_update(policy)
        # print ('beliefs: ', self.beliefs)
        print ('intents: ', self.intents)


# testing
# goes to A but changes mind
my_mind = Mind()
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('left')
my_mind.receive_observation('left')
my_mind.receive_observation('left')
my_mind.receive_observation('left')
my_mind.receive_observation('left')


# goes to A, then C
# my_mind.receive_observation('right')
# my_mind.receive_observation('right')
# my_mind.receive_observation('right')
# my_mind.receive_observation('right')
# my_mind.receive_observation('right')
# my_mind.receive_observation('right')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')
# my_mind.receive_observation('down')

print ("done")
