from datetime import datetime
from multiprocessing import Process, Queue, Value

import numpy as np
import time

from Config import Config
from Environment import Environment
from Experience import Experience

class ProcessAgent(Process):
    def __init__(self, id, training_q, episode_log_q):
        super(ProcessAgent, self).__init__()

        self.id = id
        
        self.training_q = training_q
        self.episode_log_q = episode_log_q

        self.env = Environment()
        self.num_actions = self.env.get_num_actions()
        self.actions = np.arange(self.num_actions)

        self.discount_factor = Config.DISCOUNT
        # one frame at a time
        self.wait_q = Queue(maxsize=1)
        self.Q_value_wait_q = Queue(maxsize=1)
        self.exit_flag = Value('i', 0)
        
    def convert_data(self, experiences):
        prevs = np.array([exp.prev_state for exp in experiences])
        actions = np.eye(self.num_actions)[np.array([exp.action for exp in experiences])].astype(np.float32)
        rewards = np.array([exp.reward for exp in experiences])
        curs = np.array([exp.cur_state for exp in experiences])
        dones = np.array([exp.done for exp in experiences])
        
        return prevs, actions, rewards, curs, dones

    def predict(self, state):
        # put the state in the prediction q
        self.prediction_q.put((self.id, state))
        # wait for the prediction to come back
        p, v = self.wait_q.get()
        return p, v
    
    def predict_Q(self, state, action):
        self.

    def select_action(self, prediction):
        if Config.PLAY_MODE:
            action = np.argmax(prediction)
        else:
            action = np.random.choice(self.actions, p=prediction)
        return action

    def run_episode(self):
        self.env.reset()
        done = False
        experiences = []

        time_count = 0
        reward_sum = 0.0

        while not done:
            # very first few frames
            if self.env.current_state is None:
                self.env.step(0)  # 0 == NOOP
                continue

            prediction, value = self.predict(self.env.current_state)
            action = self.select_action(prediction)
            reward, done = self.env.step(action)
            reward_sum += reward
            exp = Experience(self.env.previous_state, action, reward, self.env.current_state, done)
            experiences.append(exp)

            if done or time_count == Config.TIME_MAX:
                terminal_reward = 0 if done else value
                prevs, actions, rewards, curs, dones = self.convert_data(experiences)
                yield prevs, actions, rewards, curs, dones, terminal_reward, reward_sum

                # reset the tmax count
                time_count = 0
                # keep the last experience for the next batch
                experiences = [experiences[-1]]
                reward_sum = 0.0

            time_count += 1

    def run(self):
        # randomly sleep up to 1 second. helps agents boot smoothly.
        time.sleep(np.random.rand())
        np.random.seed(np.int32(time.time() % 1 * 1000 + self.id * 10))

        while self.exit_flag.value == 0:
            total_reward = 0
            total_length = 0
            for curs, actions, rewards, nexts, dones, terminal_reward, reward_sum in self.run_episode():
                total_reward += reward_sum
                total_length += len(rewards) + 1  # +1 for last frame that we drop
                self.training_q.put((curs, actions, rewards, nexts, dones, terminal_reward))
            self.episode_log_q.put((datetime.now(), total_reward, total_length))