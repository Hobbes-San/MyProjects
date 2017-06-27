class Experience:
    def __init__(self, prev_state, action, reward, cur_state, done):
        self.prev_state = prev_state
        self.action = action
        self.reward = reward
        self.cur_state = cur_state
        self.done = done