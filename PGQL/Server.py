from multiprocessing import Queue

import time

from Config import Config
from Environment import Environment
from NetworkVP import NetworkVP
from ProcessAgent import ProcessAgent
from ProcessStats import ProcessStats
from ThreadDynamicAdjustment import ThreadDynamicAdjustment
from ThreadPredictor import ThreadPredictor
from ThreadTrainer import ThreadTrainer
from Buffer import Buffer

class Server:
    def __init__(self):
        self.stats = ProcessStats()

        self.training_q = Buffer(minsize=Config.MIN_BUFFER_SIZE, maxsize=Config.MAX_BUFFER_SIZE,
                                 DQ_batch_size=Config.DQ_BATCH_SIZE)
        
        # The queue below is for action probability and value predictions that will be
        # used for the agents to play the game and record the experiences.
        self.prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)
        
        # The queue below is for the value predictions that will be used as the baseline
        # for the PG update step.
        self.v_prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)
        
        # The queue below is for the Q-value predictions that will be used as the baseline
        # for the DQ update step.
        self.Q_value_prediction_q = Queue(maxsize=Config.MAX_QUEUE_SIZE)

        self.model = NetworkVP(Config.DEVICE, Config.NETWORK_NAME, Environment().get_num_actions())
        if Config.LOAD_CHECKPOINT:
            self.stats.episode_count.value = self.model.load()

        self.training_step = 0
        self.frame_counter = 0

        self.agents = []
        self.predictors = []
        self.trainers = []
        self.dynamic_adjustment = ThreadDynamicAdjustment(self)

    def add_agent(self):
        self.agents.append(
            ProcessAgent(len(self.agents), self.training_q, self.prediction_q,
                         self.stats.episode_log_q))
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

    def add_trainer(self):
        self.trainers.append(ThreadTrainer(self, len(self.trainers)))
        self.trainers[-1].start()

    def remove_trainer(self):
        self.trainers[-1].exit_flag = True
        self.trainers[-1].join()
        self.trainers.pop()

    def train_model(self, x_, r_, a_, trainer_id):
        self.model.train(x_, r_, a_, trainer_id)
        self.training_step += 1
        self.frame_counter += x_.shape[0]

        self.stats.training_count.value += 1
        self.dynamic_adjustment.temporal_training_count += 1

        if Config.TENSORBOARD and self.stats.training_count.value % Config.TENSORBOARD_UPDATE_FREQUENCY == 0:
            self.model.log(x_, r_, a_)

    def save_model(self):
        self.model.save(self.stats.episode_count.value)

    def main(self):
        self.stats.start()
        self.dynamic_adjustment.start()

        if Config.PLAY_MODE:
            for trainer in self.trainers:
                trainer.enabled = False

        learning_rate_multiplier = (Config.LEARNING_RATE_END - Config.LEARNING_RATE_START) / Config.ANNEALING_EPISODE_COUNT
        beta_multiplier = (Config.BETA_END - Config.BETA_START) / Config.ANNEALING_EPISODE_COUNT

        while self.stats.episode_count.value < Config.EPISODES:
            step = min(self.stats.episode_count.value, Config.ANNEALING_EPISODE_COUNT - 1)
            self.model.learning_rate = Config.LEARNING_RATE_START + learning_rate_multiplier * step
            self.model.beta = Config.BETA_START + beta_multiplier * step

            # Saving is async - even if we start saving at a given episode, we may save the model at a later episode
            if Config.SAVE_MODELS and self.stats.should_save_model.value > 0:
                self.save_model()
                self.stats.should_save_model.value = 0

            time.sleep(0.01)

        self.dynamic_adjustment.exit_flag = True
        while self.agents:
            self.remove_agent()
        while self.predictors:
            self.remove_predictor()
        while self.trainers:
            self.remove_trainer()
