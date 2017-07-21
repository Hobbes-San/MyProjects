from multiprocessing import Queue, Value, Lock
from multiprocessing.managers import SyncManager

import time
from collections import deque

from Config import Config
from Environment import Environment
from NetworkVP import NetworkVP
from ProcessAgent import ProcessAgent
from ProcessStats import ProcessStats
from ThreadPredictor import ThreadPredictor
from ThreadPG_Trainer import ThreadPG_Trainer
from ThreadQL_Trainer import ThreadQL_Trainer

class Server:
    def __init__(self):
        self.stats = ProcessStats()
        
        # The queue below is for PG updates
        self.PG_training_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)
        
        # The queue below is for action probability and value predictions that will be
        # used for the agents to play the game and record the experiences.
        self.prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)
        
        # The queue below is for the value predictions that will be used as the baseline
        # for the PG update step.
        self.v_prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)
        
        # The queue below is for the Q-value predictions that will be used as the baseline
        # for the QL update step.
        self.Q_value_prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)

        self.model = NetworkVP(Config.DEVICE, Config.NETWORK_NAME, Environment().get_num_actions())
        if Config.LOAD_CHECKPOINT:
            self.stats.episode_count.value = self.model.load()

        self.frame_counter = 0

        self.agents = []
        self.predictors = []
        self.PG_trainers = []
        self.QL_trainers = []

    def add_agent(self, QL_training_q, QL_training_q_size, lock):
        self.agents.append(
            ProcessAgent(len(self.agents), self.PG_training_q, QL_training_q,
                         QL_training_q_size, self.prediction_q, self.stats.episode_log_q,
                         lock))
        self.agents[-1].start()

    def remove_agent(self):
        self.agents[-1].exit_flag.value = True
        self.agents[-1].join()
        self.agents.pop()

    def add_predictor(self):
        self.predictors.append(ThreadPredictor(self, len(self.predictors)))
        self.predictors[-1].start()

    def remove_predictor(self):
        self.predictors[-1].exit_flag = True
        self.predictors[-1].join()
        self.predictors.pop()

    def add_PG_trainer(self):
        self.PG_trainers.append(ThreadPG_Trainer(self, len(self.PG_trainers)))
        self.PG_trainers[-1].start()

    def remove_PG_trainer(self):
        self.PG_trainers[-1].exit_flag = True
        self.PG_trainers[-1].join()
        self.PG_trainers.pop()
        
    def add_QL_trainer(self, QL_training_q, QL_training_q_size):
        self.QL_trainers.append(ThreadQL_Trainer(self, len(self.QL_trainers), QL_training_q,
                                QL_training_q_size))
        self.QL_trainers[-1].start()
        
    def remove_QL_trainer(self):
        self.QL_trainers[-1].exit_flag = True
        self.QL_trainers[-1].join()
        self.QL_trainers.pop()

    def train_model(self, x_, r_, a_, trainer_id):
        self.model.train(x_, r_, a_, trainer_id)
        self.frame_counter += x_.shape[0]
        
        self.stats.training_count.value += 1

    def main(self):
        self.stats.start()
        # Make deque multiprocessing friendly by using SyncManager
        SyncManager.register('deque', deque)
        m = SyncManager(); m.start(); QL_training_q = m.deque(maxlen=Config.MAX_BUFFER_SIZE)
        # Initialize lock to keep an accurate counter for the buffer size
        lock = Lock(); QL_training_q_size = Value('i', 0)
        # Since ThreadDynamicAdjustment class is gone, we must add all processes
        # and agents manually
        for _ in range(Config.AGENTS):
            self.add_agent(QL_training_q, QL_training_q_size, lock)
        for _ in range(Config.PREDICTORS):
            self.add_predictor()
        for _ in range(Config.PG_TRAINERS):
            self.add_PG_trainer()
        for _ in range(Config.QL_TRAINERS):
            self.add_QL_trainer(QL_training_q, QL_training_q_size)

        if Config.PLAY_MODE:
            for trainer in self.PG_trainers + self.QL_trainers:
                trainer.enabled = False

        time.sleep(0.01)
        
        # Shut down everything
        m.shutdown()
        while self.agents:
            self.remove_agent()
        while self.predictors:
            self.remove_predictor()
        while self.trainers:
            self.remove_trainer()
