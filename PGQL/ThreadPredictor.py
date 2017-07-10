from threading import Thread

import numpy as np

from Config import Config


class ThreadPredictor(Thread):
    def __init__(self, server, id):
        super(ThreadPredictor, self).__init__()
        self.setDaemon(True)

        self.id = id
        self.server = server
        self.exit_flag = False

    def run(self):
        ids = np.zeros(Config.PREDICTION_BATCH_SIZE, dtype=np.uint16)
        states = np.zeros(
            (Config.PREDICTION_BATCH_SIZE, Config.IMAGE_HEIGHT, Config.IMAGE_WIDTH, Config.STACKED_FRAMES),
            dtype=np.float32)

        while not self.exit_flag:
            ids[0], states[0] = self.server.prediction_q.get()

            size = 1
            while size < Config.PREDICTION_BATCH_SIZE and not self.server.prediction_q.empty():
                ids[size], states[size] = self.server.prediction_q.get()
                size += 1

            batch = states[:size]
            p, v = self.server.model.predict_p_and_v(batch)
            
            for i in range(size):
                if ids[i] < len(self.server.agents):
                    self.server.agents[ids[i]].wait_q.put((p[i], v[i]))
            
            Q_value_size = 0
            while Q_value_size < Config.PREDICTION_BATCH_SIZE and not self.server.Q_value_prediction_q.empty():
                Q_value_id, Q_value_states = self.server.Q_value_prediction_q.get()
                Q = self.server.model.predict_Q_value(Q_value_states)
                
                if Q_value_id < len(self.server.trainers):
                    self.server.trainers[Q_value_id].Q_value_wait_q.put(Q)
                Q_value_size += 1
            
            v_size = 0
            while v_size < Config.PREDICTION_BATCH_SIZE and not self.server.v_prediction_q.empty():
                v_id, v_states = self.server.v_prediction_q.get()
                v = self.server.model.predict_v(v_states)
                
                if v_id < len(self.server.trainers):
                    self.server.trainers[v_id].v_wait_q.put(v)
                v_size += 1
