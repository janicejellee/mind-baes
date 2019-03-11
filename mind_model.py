class Mind:
    def __init__(self, world):
        self.world = world
        self.time = 0
        self.beliefs = None
        self.intents = None

    def receive_observation(self, direction, x, y):
        return None

    def update_beliefs(self):
        return None

    def update_intents(self):
        return None

    def reward(self, action):
        return None

    # later: visualizationy stuffz
