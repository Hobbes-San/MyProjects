from threading import Thread
import numpy as np
from multiprocessing import Queue

from Config import Config

def PG_accumulate_rewards(rewards, terminal_reward):
    reward_sum = terminal_reward; returns = []
    for t in reversed(range(0, len(rewards)-1)):
        r = np.clip(rewards[t], Config.REWARD_MIN, Config.REWARD_MAX)
        reward_sum = Config.DISCOUNT * reward_sum + r
        returns.append(reward_sum)
    returns.reverse()
    return returns

class ThreadPG_Trainer(Thread):
    def __init__(self, server, id):
        super(ThreadPG_Trainer, self).__init__()
        self.setDaemon(True)

        self.id = id
        self.server = server
        self.v_wait_q = Queue(maxsize=1)
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
                batch_size = 0
                # Batch up data for PG update step
                while batch_size <= Config.PG_TRAINING_MIN_BATCH_SIZE:
                    experiences, terminal_reward = self.server.PG_training_q.get()
                    prevs, actions, rewards, _, _ = self.convert_data(experiences)
                    returns = PG_accumulate_rewards(rewards, terminal_reward)
                    if batch_size == 0:
                        x__ = prevs[:-1]; r__ = np.array(returns); a__ = actions[:-1]
                    else:
                        x__ = np.concatenate((x__, prevs[:-1]))
                        r__ = np.concatenate((r__, returns))
                        a__ = np.concatenate((a__, actions[:-1]))
                    batch_size += len(returns)
                self.server.v_prediction_q.put((self.id, x__))
                baselines = self.v_wait_q.get()
                # Subtract by the PG baselines to get PG advantages
                r__ = r__ - baselines
                # The main network expects a 1D array, so we must squeeze
                r__ = np.squeeze(r__)
                self.server.train_model(x__, r__, a__, self.id)
