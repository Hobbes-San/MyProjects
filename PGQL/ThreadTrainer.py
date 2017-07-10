from threading import Thread
from Experience import Experience
import numpy as np
from multiprocessing import Queue

from Config import Config

class ThreadTrainer(Thread):
    def __init__(self, server, id):
        super(ThreadTrainer, self).__init__()
        self.setDaemon(True)

        self.id = id
        self.server = server
        self.v_wait_q = Queue(maxsize=1)
        self.Q_value_wait_q = Queue(maxsize=1)
        self.exit_flag = False
    
    @staticmethod
    def PG_accumulate_rewards(rewards, terminal_reward):
        reward_sum = terminal_reward; returns = []
        for t in reversed(range(0, len(rewards)-1)):
            r = np.clip(rewards[t], Config.REWARD_MIN, Config.REWARD_MAX)
            reward_sum = Config.DISCOUNT * reward_sum + r
            returns.append(reward_sum)
        returns.reverse()
        return returns
    
    def convert_data(self, experiences):
        prevs = np.array([exp.prev_state for exp in experiences])
        actions = np.eye(self.server.model.num_actions)[np.array([exp.action for exp in experiences])].astype(np.float32)
        rewards = np.array([exp.reward for exp in experiences])
        curs = np.array([exp.cur_state for exp in experiences])
        dones = np.array([exp.done for exp in experiences])
        
        return prevs, actions, rewards, curs, dones

    def run(self):
        s = self.server.training_step
        if s > 0 and s % 20 == 0:
            PG = False
        else:
            PG = True
        while not self.exit_flag:
            if Config.TRAIN_MODELS:
                if PG:
                    batch_size = 0
                    while batch_size <= Config.PG_TRAINING_MIN_BATCH_SIZE:
                        experiences, terminal_reward = self.server.training_q.get()
                        prevs, actions, rewards, _, _ = self.convert_data(experiences)
                        returns = ThreadTrainer.PG_accumulate_rewards(rewards, terminal_reward)
                        if batch_size == 0:
                            x__ = prevs[:-1]; r__ = returns; a__ = actions[:-1]
                        else:
                            x__ = np.concatenate((x__, prevs[:-1]))
                            r__ = np.concatenate((r__, returns))
                            a__ = np.concatenate((a__, actions[:-1]))
                        batch_size += len(returns)
                    self.server.v_prediction_q.put((self.id, x__))
                    baselines = self.v_wait_q.get()
                    r__ = r__ - baselines
                    self.server.train_model(x__, r__, a__, self.id)
                else:
                    experiences = self.server.training_q.sample_batch()
                    if experiences is not None:
                        prevs, actions, rewards, curs, dones = self.convert_data(experiences)
                        self.server.Q_value_prediction_q.put((self.id, prevs))
                        prev_Q = np.sum(self.server.Q_value_wait_q.get() * actions, axis=1)
                        self.server.Q_value_prediction_q.put((self.id, curs))
                        cur_Q = np.max(self.Q_value_wait_q.get(), axis=1)
                        advantages = np.zeros(cur_Q.shape[0])
                        for i in range(cur_Q.shape[0]):
                            advantages[i] = rewards[i] + Config.DISCOUNT*cur_Q[i] - prev_Q[i] if dones[i] is False else rewards[i]         
                        self.server.train_model(prevs, advantages, actions, self.id)
