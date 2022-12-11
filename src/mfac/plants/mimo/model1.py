import time

from ... import PlantInterface
import numpy as np
import matplotlib.pyplot as plt


# A simple MIMO model based on "Model Free Adaptive Control" book
# X : size [4]
# Y : size [2]
# U : size [2]

def dynamic(x, u, k):
    a = 1 + 0.1 * np.sin(2 * np.pi * k / 1000)
    b = 1 + 0.1 * np.cos(2 * np.pi * k / 1000)
    next_x = x
    next_x[0] = (x[0] ** 2 / (1 + x[0] ** 2)) + 0.3 * x[1]
    next_x[1] = (x[0] ** 2 / (1 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2)) + a * u[0]
    next_x[2] = (x[2] ** 2 / (1 + x[2] ** 2)) + 0.2 * x[3]
    next_x[3] = (x[2] ** 2 / (1 + x[0] ** 2 + x[1] ** 2 + x[3] ** 2)) + b * u[1]
    return next_x


class Model1(PlantInterface):
    @PlantInterface.initializer
    def __init__(self,
                 initial_state=np.array([0]),
                 ):
        self.number_of_inputs = 2
        self.number_of_states = 4
        self.number_of_outputs = 2
        self.x = initial_state
        self.y = np.matrix('1,0,0,0;0,0,1,0') * self.x
        self.u = np.matrix('0; 0')
        self.X = np.array([self.x])
        self.Y = np.array([self.y])
        self.U = np.array([self.u])
        self.time = 0

    def reset(self):
        self.x = self.X[0]
        self.y = self.Y[0]
        self.u = np.matrix('0; 0')
        self.X = np.array([self.x])
        self.Y = np.array([self.y])
        self.U = np.array([self.u])
        self.time = 0

    def step(self, u):
        self.u = u
        self.U = np.append(self.U, [self.u], axis=0)
        self.x = dynamic(self.x, self.u, self.time)
        self.y = np.matrix('1,0,0,0;0,0,1,0') * self.x
        self.X = np.append(self.X, [self.x], axis=0)
        self.Y = np.append(self.Y, [self.y], axis=0)
        self.time += 1
        return self.y

    def predict(self, u, full_state=True):
        x = self.x
        y = self.y
        k = self.time
        x_predict = np.array([x])
        y_predict = np.array([y])
        for u_k in u:
            x = dynamic(x, u_k, k)
            y = np.matrix('1,0,0,0;0,0,1,0') * x
            x_predict = np.append(x_predict, [x], axis=0)
            y_predict = np.append(y_predict, [y], axis=0)
            k += 1
        if full_state:
            return x_predict
        else:
            return y_predict

    def observe(self, time_window, full_state=True):
        if full_state:
            return self.X[-time_window:]
        else:
            return self.Y[-time_window:]

    def render(self, mode='plot'):
        if (mode == 'print'):
            print(self.y)
        if (mode == 'plot'):
            plt.subplot(2, 1, 1)
            plt.plot(range(self.time + 1), self.Y[:, 0])
            plt.xlabel("k")
            plt.ylabel("y1(k)")
            plt.subplot(2, 1, 2)
            plt.plot(range(self.time + 1), self.Y[:, 1])
            plt.xlabel("k")
            plt.ylabel("y2(k)")
            plt.show()
        if (mode == 'visual'):
            print('Visualization is disabled for this model')
