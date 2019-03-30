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

        # how certain we are of current state
        epsilon_obs = 0.001
        self.observation_distribution_prob = 1 - episilon_obs

        self.prev_state = (0,0)
        self.state = (0,0)

        self.states = []
        for i in range(len(self.map_length)):
            for j in range(len(self.map_length)):
                self.states.append((i,j))

        self.gamma = 0.9

    def reward(self, state):
        "Return a numeric reward for this state."
        if (state in self.world_loc):
            return 10
        else:
            return -1

    def get_next_state(state, action):
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
        elif action == 'down':
            if 0<=x<self.map_length and 0<=(y-1)<self.map_length:
                next_state = (x,y-1)
        elif action == 'up':
            if 0<=x<self.map_length and 0<=(y+1)<self.map_length:
                next_state = (x,y+1)

        return next_state

    def transition(state, action):
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
            pairs.append(next_state, 0.9)
            remaining = len(actions) - 1
            prob = 0.1 / remaining
            for a in actions:
                if a != action:
                    pairs.append((self.get_next_state(state, a), prob))
        else:
            prob = 1.0 / len(actions)
            for a in actions:
                pairs.append((self.get_next_state(state, a), prob))
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
            actions.append('down')
        if 0<=x<self.map_length and 0<=(y+1)<self.map_length:
            actions.append('up')

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

    def beliefs(self, state):
        "Update beliefs"
        near_locations = self.within_range(state)
        for loc in near_locations:
            i = self.world_loc.index(loc)
            resource = self.world_state[i]
            point = (x,y)

        i = self.world_loc.index(state)
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

    def value_iteration(self, state, epsilon=0.001):
        "Solving by value iteration."
        # TODO add beliefs part of equation into this

        actions = self.actions(state)
        next_states = []
            for a in actions:
                next_states.append(self.get_next_state(state, a))

        U1 = dict([(s, 0) for s in next_states])
        R, T, gamma = self.R, self.T, self.gamma

        while True:
            U = U1.copy()
            delta = 0
            for s in self.states:
                U1[s] = R(s) + gamma * max([sum([p * U[s1] for (p, s1) in T(s, a)])
                                            for a in self.actions(s)])
                delta = max(delta, abs(U1[s] - U[s]))
            if delta < epsilon * (1 - gamma) / gamma:
                 return U

    def best_policy(self, U):
        """
        Given an MDP and a utility function U, determine the best policy,
        as a mapping from state to action.
        """
        pi = {}
        for s in self.states:
            pi[s] = argmax(self.actions(s), lambda a:self.expected_utility(a, s, U))
        return pi

    def expected_utility(self, action, state, U):
        "The expected utility of doing a in state s, according to the MDP and U."
        return sum([p * U[s1] for (p, s1) in self.T(state, action)])

    def intents(self):
        "Update intents."
        # TODO get intents based on the best policy?

    def receive_observation(self, action):
        "Receive observation and get updated intents."
        # TODO run one round

# TODO test situations, similary to older versions...
