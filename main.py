from tetris import Tetris
from agent import Agent
import numpy as np
from keras.callbacks import TensorBoard
from tensorflow.summary import FileWriter

class Board(TensorBoard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.write = FileWriter(self.log_dir)
    
    def log(self, step, **stat):
        self._write_logs(stat, step)
    
    def set_model(self, model):
        pass

def run():
    game = Tetris()
    episodes = 2000
    discount=0.9 
    epsilon=.99
    nuerons=[32,32,32]
    activation_functions=['relu', 'relu', 'relu', 'linear']
    batch_size = 32
    epoch = 5

    dqn = Agent()


