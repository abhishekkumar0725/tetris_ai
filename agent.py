import numpy as np
import tensorflow as tf
import random
from keras.layers import Dense
from keras.models import Sequential, save_model, load_model

class Agent:
    
    def __init__(self, state_size=4, discount=0.9, epsilon=.99, nuerons=[32,32,32], 
        activation_functions=['relu', 'relu', 'relu', 'linear']):
        self.state_size = state_size
        self.discount = discount
        self.epsilon = epsilon
        self.nuerons = nuerons
        self.layers = len(self.nuerons)
        self.activations_functions=activation_functions
        self.samples = []

        self.model = self.build()

    def build(self):
        model = Sequential()
        model.add(Dense(self.nuerons[0], input_dim=self.state_size, activation=self.activations_functions[0]))
        for i in range(1,self.layers):
            model.add(Dense(self.nuerons[i], activation=self.activations_functions[i]))
        model.add(Dense(1, activation=self.activations_functions[self.layers]))
        model.compile(loss='mse', optimizer='adam')
        
        return model
    
    def add_sample(self, state, next_state, reward, complete):
        self.samples.append([state, next_state, reward, complete])
        if len(self.samples) > 10000:
            self.samples.pop(0)

    def train(self, batch_size=64, epoch=5):
        if len(self.samples) >= batch_size:
            batch = random.sample(self.samples, batch_size)
            next_state = [sample[1] for sample in batch]
            q_values = [prediction[0] for prediction in self.model.predict(next_state)]

            rewards = []
            for i, (state, next_state, reward, complete) in enumerate(batch):
                q = reward
                if not complete:
                    q += self.discount * q_values[i]
                rewards.append((state, q))
            
            train_states = np.array([q[0] for q in rewards])
            train_rewards =  np.array([q[1] for q in rewards])
            
            self.model.fit(train_states, train_rewards, batch_size=batch_size, epochs=epoch, verbose=0)
            if self.epsilon > .01:
                self.epsilon -= .05*self.epsilon
        
    def best_state(self, states):
        best_score = -1*float('inf')
        best_state =  None

        for state in states:
            score = self.model.predict(np.reshape(state, [1, self.state_size]))[0]
            if score > best_score:
                best_score = score
                best_state = state
            
        return best_state
        
    def predict(self, state):
        state = np.reshape(state, [1, self.state_size])
        if np.random.rand() < self.epsilon:
            return np.random.rand()
        return self.model.predict(state)[0]