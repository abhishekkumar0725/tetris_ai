import numpy as np
import tensorflow as tf
from keras.layers import Dense
from keras.model import Sequential, save_model, load_model

class Agent:

    def __init__(self, state, discount=0.9, epsilon=.99, nuerons=[32,32,32],
        activation_functions=['relu', 'relu', 'relu', 'relu']):
        self.state = state
        self.discount = discount
        self.epsilon = epsilon
        self.nuerons = nuerons
        self.layers = len(self.nuerons)
        self.activations_functions=activation_functions
        self.samples = []

        self.model = self.build()

    def build(self):
        model = Sequential()
        model.add(Dense(self.neurons[0], input_dim=self.state, activation=self.activations_functions[0]))
        for i in range(1,self.layers):
            model.add(Dense(self.nuerons[i], activation=self.activations_functions[i]))
        model.add(1, activation=self.activations_functions[self.layers+1])
        model.compile(loss='mse', optimizer='adam')

        return model

    def new_sample(self, state, action, reward, next_state):
        self.samples.append([state, action, reward, next_state])

    def iterate_once(self, batch_size):
        index = 0
        while index < len(self.samples):
            x = self.samples[index:index + batch_size]
            yield x
            index += batch_size

    def train(self, batch_size, epochs):
        x = []
        y = []


        qVal =
        self.model.fit(x, y, batch_size = batch_size, epochs = epochs)
