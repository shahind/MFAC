import time

from ... import PlantInterface
import numpy as np
import matplotlib.pyplot as plt

# A simple SISO model based on "Model Free Adaptive Control" book
# X = Y : with size [1]
# U : size [1]
class Model1(PlantInterface):
    @PlantInterface.initializer
    def __init__(self,
                 initial_state=np.array([0]),
                 ):
        self.number_of_inputs = 1
        self.number_of_states = 1
        self.number_of_outputs = 1
        self.x = initial_state
        self.y = initial_state
        self.u = np.array([0])
        self.X = np.array([self.x])
        self.Y = np.array([self.y])
        self.U = np.array([self.u])
        self.time = 0

    def reset(self):
        self.x = self.X[0]
        self.y = self.Y[0]
        self.u = np.array([0])
        self.X = np.array([self.x])
        self.Y = np.array([self.y])
        self.U = np.array([self.u])
        self.time = 0

    def step(self, u):
        self.u = u
        self.U = np.append(self.U, self.u)
        curr_u = 1.5 * u - 1.5 * np.power(u, 2) + 0.5 * np.power(u, 3)
        prev_u = 1.5 * self.U[self.time-1] - 1.5 * (np.power(self.U[self.time-1], 2)) + 0.5 * np.power(self.U[self.time-1], 3)
        self.x = 0.6 * self.Y[self.time] - 0.1 * self.Y[self.time-1] + 1.2 * curr_u - 0.1 * prev_u
        self.y = self.x
        self.X = np.append(self.X, self.x)
        self.Y = np.append(self.Y, self.y)
        self.time += 1
        return self.y

    def observe(self, time_window, full_state=True):
        if full_state:
            return self.X[-time_window:]
        else:
            return self.Y[-time_window:]

    def render(self, mode='plot'):
        if(mode=='print'):
            print(self.y)
        if(mode=='plot'):
            plt.plot(range(self.time+1), self.Y)
            plt.xlabel("k")
            plt.ylabel("y(k)")
            plt.title("Output")
            plt.show()
        if(mode=='visual'):
            print('Visualization is disabled for this model')