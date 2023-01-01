import time

from ... import PlantInterface
import numpy as np
import matplotlib.pyplot as plt


# A simple SISO model based on "Model Free Adaptive Control" book
# X = Y : with size [1]
# U : size [1]
def dynamic(x, u, prev_x, prev_u):
    A = [[4.4, 1, 0, 0, 0], [-8.09, 0, 1, 0, 0], [7.83, 0, 0, 1, 0], [-4, 0, 0, 0, 1], [0.86, 0, 0, 0, 0]]
    B = [[0.00098], [0.01299], [0.01859], [0.00330], [-0.00002]]
    C = [1, 0, 0, 0, 0]
    K = [[2.3], [-6.64], [7.515], [-4.0146], [0.86336]]
    D = [0]
    #e = np.random.normal(0, 0.1, size=1)
    next_x = A * x + B * u
    return next_x


class Wingerden(PlantInterface):
    @PlantInterface.initializer
    def __init__(self,
                 initial_state=np.array([0]),
                 ):
        self.number_of_inputs = 1
        self.number_of_states = 5
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
        self.x = dynamic(self.x, self.u, self.X[self.time - 1], self.U[self.time - 1])
        self.y = self.x[0]
        self.X = np.append(self.X, self.x)
        self.Y = np.append(self.Y, self.y)
        self.time += 1
        return self.y

    def predict(self, u, full_state=True):
        x = self.x
        x_prev = self.X[self.time - 1]
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
        if (mode == 'print'):
            print(self.y)
        if (mode == 'plot'):
            plt.plot(range(self.time + 1), self.Y)
            plt.xlabel("k")
            plt.ylabel("y(k)")
            plt.title("Output")
            plt.show()
        if (mode == 'visual'):
            print('Visualization is disabled for this model')
