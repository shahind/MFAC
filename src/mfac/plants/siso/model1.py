import time

from ... import PlantInterface
import numpy as np
import matplotlib.pyplot as plt

# A simple SISO model based on "Model Free Adaptive Control" book
# X = Y : with size [1]
# U : size [1]
def dynamic(x, u, prev_x, prev_u):
    curr_u = 1.5 * u - 1.5 * np.power(u, 2) + 0.5 * np.power(u, 3)
    prev_u = 1.5 * prev_u - 1.5 * (np.power(prev_u, 2)) + 0.5 * np.power(prev_u, 3)
    next_x = 0.6 * x - 0.1 * prev_x + 1.2 * curr_u - 0.1 * prev_u
    return next_x


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
        self.x = dynamic(self.x, self.u, self.X[self.time-1], self.U[self.time-1])
        self.y = self.x
        self.X = np.append(self.X, self.x)
        self.Y = np.append(self.Y, self.y)
        self.time += 1
        return self.y

    def predict(self, u, full_state=True):
        x = self.x
        x_prev = self.X[self.time-1]
        x_predict = np.array([x])
        u_prev = self.u
        for u_k in u:
            x = dynamic(x, u_k, x_prev, u_prev)
            x_predict = np.append(x_predict, x)
            x_prev = x
            u_prev = u_k
        return x_predict

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