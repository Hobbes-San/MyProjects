from threading import Thread
import numpy as np
from multiprocessing import Queue
import random

from Config import Config
# This is a new class for my PGQ: algorithm not found in the original GA3C
class ThreadQL_Trainer(Thread):
    def __init__(self, server, id, QL_training_q, QL_training_q_size):
        super(ThreadQL_Trainer, self).__init__()
        self.setDaemon(True)

        self.id = id
        self.server = server
        self.QL_training_q = QL_training_q
        self.QL_training_q_size = QL_training_q_size
        self.Q_value_wait_q = Queue(maxsize=1)
        self.exit_flag = False
    
    def convert_data(self, experiences):
        prevs = np.array([exp.prev_state for exp in experiences])
        actions = np.eye(self.server.model.num_actions)[np.array([exp.action for exp in experiences])].astype(np.float32)
        rewards = np.array([exp.reward for exp in experiences])
        curs = np.array([exp.cur_state for exp in experiences])
        dones = np.array([exp.done for exp in experiences])
        
        return prevs, actions, rewards, curs, dones

    def run(self):
        while not self.exit_flag:
            if Config.TRAIN_MODELS:
                # Don't do QL update step until there's a minimum number of experiences
                # in the QL replay buffer
                if self.QL_training_q_size.value < Config.MIN_BUFFER_SIZE or self.server.model.get_global_step() % 20 != 0:
                    continue
                # Randomly sample a small batch of experiences
                experiences = random.sample(self.QL_training_q._getvalue(), Config.QL_BATCH_SIZE)
                prevs, actions, rewards, curs, dones = self.convert_data(experiences)
                # These are the QL baselines
                self.server.Q_value_prediction_q.put((self.id, prevs))
                prev_Q = np.sum(self.Q_value_wait_q.get() * actions, axis=1)
                # These are the maximum Q-values for the current state
                self.server.Q_value_prediction_q.put((self.id, curs))
                cur_Q = np.max(self.Q_value_wait_q.get(), axis=1)
                advantages = np.zeros(cur_Q.shape[0])
                # We calculate QL advantages here
                for i in range(cur_Q.shape[0]):
                    advantages[i] = rewards[i] + Config.DISCOUNT*cur_Q[i] - prev_Q[i] if dones[i] is False else rewards[i]         
                self.server.train_model(prevs, advantages, actions, self.id)
