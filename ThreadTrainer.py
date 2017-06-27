from threading import Thread
from Experience import Experience
import numpy as np

from Config import Config

global_step = 0

class ThreadTrainer(Thread):
    def __init__(self, server, id):
        super(ThreadTrainer, self).__init__()
        self.setDaemon(True)

        self.id = id
        self.server = server
        self.exit_flag = False
    
    @staticmethod
    def PG_accumulate_rewards(prevs, actions, rewards, curs, dones, terminal_reward, discount_factor):
        reward_sum = terminal_reward; returns = []
        for t in reversed(range(0, len(rewards)-1)):
            r = np.clip(rewards[t], Config.REWARD_MIN, Config.REWARD_MAX)
            reward_sum = discount_factor * reward_sum + r
            returns.append(reward_sum)
        returns.reverse()
        return returns[:-1]

    def run(self):
        if self.server.global_step % 10 == 0:
            PG = True
        else:
            PG = False
        while not self.exit_flag:
            batch_size = 0
            if PG:
                while batch_size <= Config.TRAINING_MIN_BATCH_SIZE:
                    prevs, actions, rewards, curs, dones, terminal_reward = self.server.training_q.get()
                    returns = ThreadTrainer.PG_accumulate_rewards(prevs, actions, rewards, curs, dones,
                                terminal_reward, Config.DISCOUNT)
                    if batch_size == 0:
                        x__ = prevs; r__ = returns; a__ = actions
                    else:
                        x__ = np.concatenate((x__, prevs))
                        r__ = np.concatenate((r__, returns))
                        a__ = np.concatenate((a__, actions))
                    batch_size += prevs.shape[0]
            else:
                prevs, actions, rewards, curs, dones = self.server.training_q.sample_batch()
                prev_Q = self.server.model.predict_Q(prevs, actions)
                cur_Q = np.max(self.server.model.predict(curs), axis=1)
                advantages = [r + self.gamma*cur_q - prev_q if done is False else r for r, prev_q,
                              cur_q, done in zip(rewards, prev_Q, cur_Q, dones)]            
                x__ = prevs; r__ = advantages; a__ = actions
            if Config.TRAIN_MODELS:
                self.server.train_model(x__, r__, a__, self.id)