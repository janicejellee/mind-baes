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

        self.state = (0,0)

        self.states = []
        for i in range(self.map_length):
            for j in range(self.map_length):
                self.states.append((i,j))

        self.gamma = 0.5

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

        # figure out which locations you can see
        # update beliefs for the ones close to you


        #redistribute beliefs

        for loc in near_locations:
            i = self.world_loc.index(loc)
            resource = self.world_state[i]
            print ("observed resource %s" % resource)
            consistently_observed_worlds = []
            inconsistently_observed_worlds = []
            for j in range(len(self.beliefs_worlds)):
                world = self.beliefs_worlds[j]
                if world[i] == resource:
                    consistently_observed_worlds.append(j)
                else:
                    inconsistently_observed_worlds.append(j)
            factor = len(consistently_observed_worlds)
            sum_of_consistently_observed = sum([self.beliefs[i] for i in consistently_observed_worlds])
            sum_of_inconsistently_observed = sum([self.beliefs[i] for i in inconsistently_observed_worlds])
            for i in range(len(self.beliefs)):
                if i in consistently_observed_worlds:
                    self.beliefs[i] = 0.9 * self.beliefs[i]/sum_of_consistently_observed
                else:
                    self.beliefs[i] = 0.1 * self.beliefs[i]/sum_of_inconsistently_observed

            self.beliefs = [float(i)/sum(self.beliefs) for i in self.beliefs]
            print("new beliefs %s " % self.beliefs)

        #
        #
        #
        # for loc in near_locations:
        #     i = self.world_loc.index(loc)
        #     resource = self.world_state[i]
        #
        #     increasing_beliefs = []
        #     decreasing_beliefs = []
        #     for j in range(len(self.beliefs_worlds)):
        #         world = self.beliefs_worlds[j]
        #         if world[i] == resource:
        #             increasing_beliefs.append(j)
        #         else:
        #             decreasing_beliefs.append(j)
        #
        #     # increase belief in worlds
        #     sum_increase_beliefs = 0
        #     for b in increasing_beliefs:
        #         self.beliefs[b] *= 2
        #         sum_increase_beliefs += self.beliefs[b]
        #     # print ("increasing ", increasing_beliefs)
        #
        # new_beliefs = []
        # for b in self.beliefs:
        #     new_beliefs.append(b/sum(self.beliefs))
        #
        # self.beliefs = new_beliefs


        ''' 90% accuracy
        ABC    ACB   BCA BAC  CBA  CAB
        [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]
        observe A in loc 1
        [.45, .45, 0.025, 0.025, 0.025, 0.025]
        observe C in loc 2

        normalize????

        [ 0.45 * 0.1/4 , .9 * 45./47.5, 0.9 * 2.5/47.5, 0.025 * 0.1/4, 0.025 * 0.1/4, 0.025 * 0.1/4]




        '''

    def value_iteration(self, epsilon=0.001):
        "Solving by value iteration."
        # TODO check that beliefs part of eqn was added correctly?

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

    def intents_update(self, action):
        "Update intents."
        """
            belief: [Pr(ABC), Pr(ACB), Pr(BAC), Pr(BCA), Pr(CAB), Pr(CBA)]
            state: current location on the grid
            action: action he takes
        """

        next_state = self.get_next_state(self.state, action)

        # difference in distance that this action takes us, or how much closer or farther
        # we get from the 3 resource locations
        dists = []

        for resource_pos in self.world_loc:
            dist1 = self.get_distance(resource_pos, self.state)
            dist2 = self.get_distance(resource_pos, next_state)
            diff_dist = dist1-dist2
            dists.append(diff_dist)

        print (dists)

        new_intents_scores = {'A': 0, 'B': 0, 'C': 0}

        for i in range(len(self.beliefs_worlds)):
            world = self.beliefs_worlds[i]
            belief = self.beliefs[i]
            for i in range(3):
                r = world[i]
                new_intents_scores[r] += dists[i] * belief

        new_intents = {}
        factor = 0.3
        sum_new_intents = 0
        for r in self.intents:
            new_intents[r] = max(self.intents[r] + factor * new_intents_scores[r], 0)
            sum_new_intents += new_intents[r]

        self.intents = {'A': new_intents['A']/sum_new_intents, 'B': new_intents['B']/sum_new_intents, 'C': new_intents['C']/sum_new_intents}

    def receive_observation(self, action):
        "Receive observation, update model, and get updated intents."
        print ("------")
        self.state = self.get_next_state(self.state, action)
        self.beliefs_update(self.state)
        U = self.value_iteration()
        # print (U)
        policy = self.best_policy(U)
        print (self.state)
        self.intents_update(action)
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

print ("---------------------------")

# # goes to A, then C
my_mind = Mind()
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('right')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')
my_mind.receive_observation('down')


print ("done")
