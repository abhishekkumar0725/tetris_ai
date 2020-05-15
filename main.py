from tetris import Tetris
from agent import Agent
import numpy as np
from datetime import datetime
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

    dqn = Agent(4, discount, epsilon, nuerons, activation_functions)

    log_dir = f'logs/tetris-nn={str(nuerons)}-mem={10000}-bs={batch_size}-e={epoch}-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
    log = Board(log_dir=log_dir)

    episodes = 2000
    scores = []
    for episode in range(episodes):
        current = game.newGame()
        done, step = False, 0

        while not done:
            actions = game.getLegalActions()
            bestState = dqn.best_state(actions.values())

            for action, state in action.items():
                if state == bestState


