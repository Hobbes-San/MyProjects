import sys
if sys.version_info >= (3,0):
    from queue import Queue as queueQueue
else:
    from Queue import Queue as queueQueue

from datetime import datetime
from multiprocessing import Process, Queue, Value

import matplotlib.pyplot as plt
import numpy as np
import time

from Config import Config

class ProcessStats(Process):
    def __init__(self):
        super(ProcessStats, self).__init__()
        self.episode_log_q = Queue(maxsize=100)
        self.episode_count = Value('i', 0)
        self.training_count = Value('i', 0)
        self.total_frame_count = 0

    def FPS(self):
        # average FPS from the beginning of the training (not current FPS)
        return np.ceil(self.total_frame_count / (time.time() - self.start_time))

    def TPS(self):
        # average TPS from the beginning of the training (not current TPS)
        return np.ceil(self.training_count.value / (time.time() - self.start_time))

    def run(self):
        with open(Config.RESULTS_FILENAME, 'a') as results_logger:
            rolling_frame_count = 0
            rolling_reward = 0
            results_q = queueQueue(maxsize=Config.STAT_ROLLING_MEAN_WINDOW)
            scores = []
            
            self.start_time = time.time()
            first_time = datetime.now()
            while self.episode_count.value < Config.EPISODES:
                episode_time, reward, length = self.episode_log_q.get()
                results_logger.write('%s, %d, %d\n' % (episode_time.strftime("%Y-%m-%d %H:%M:%S"), reward, length))
                results_logger.flush()

                self.total_frame_count += length
                self.episode_count.value += 1

                rolling_frame_count += length
                rolling_reward += reward

                if results_q.full():
                    old_episode_time, old_reward, old_length = results_q.get()
                    rolling_frame_count -= old_length
                    rolling_reward -= old_reward
                    first_time = old_episode_time

                results_q.put((episode_time, reward, length))
                # Print stats and keep a list of scores
                if self.episode_count.value % Config.PRINT_STATS_FREQUENCY == 0:
                    Rscore = rolling_reward / results_q.qsize()
                    scores.append(Rscore)
                    print(
                        '[Time: %8d] '
                        '[Episode: %8d Score: %10.4f] '
                        '[RScore: %10.4f RPPS: %5d] '
                        '[PPS: %5d TPS: %5d] '
                        % (int(time.time()-self.start_time),
                           self.episode_count.value, reward,
                           Rscore,
                           rolling_frame_count / (datetime.now() - first_time).total_seconds(),
                           self.FPS(), self.TPS()))
                    sys.stdout.flush()
            # Plot the scores and save the figure
            plt.plot(np.arange(100, 30100, 100), scores)
            plt.xlabel('Episode Count')
            plt.ylabel('Score')
            plt.show()
            plt.savefig('SpaceInvaders_PGQL.png')
