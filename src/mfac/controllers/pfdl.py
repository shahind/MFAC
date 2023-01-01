from .. import MFACInterface
import numpy as np
from random import random


class PartialFormDynamicLinearization(MFACInterface):
    @MFACInterface.initializer
    def __init__(self,
                 model,  # plant model
                 iteration_function,  # will be called in each iteration
                 eta,                 # 0 <eta <=2   Weighting Factor
                 mu,                  # 0 < mu      Weighting Factor
                 rho,                 # 0 < rho <= 1 Step Factor
                 labda,               # 0 < labda
                 reference_output,
                 max_steps=1000,
                 mimo=False,
                 f0=None,
                 nu=2,
                 ):
        self.max_iterations = int(max_steps)
        self.eta = eta
        self.mu = mu
        self.rho = rho
        self.labda = labda
        self.nu = nu
        self.Yd = reference_output
        self.is_mimo = mimo
        self.model = model
        self.iteration_function = iteration_function
        self.u = np.matrix(np.zeros([self.model.number_of_inputs, 1]))
        if f0 is None:
            self.f = np.matrix(np.zeros([self.model.number_of_outputs, self.model.number_of_inputs]))
        else:
            self.f = f0
        self.du = self.u
        self.U = np.array([self.u])
        self.F = np.array([self.f])
        self.dU = np.array([self.du])
        self.iteration = 0

    def run(self):
        for self.iteration in range(self.max_iterations):
            self.calculate_zero_control() if self.iteration < 2 + self.nu else self.calculate_control()
            self.model.step(self.u)
            self.iteration_function(self)
        return self

    def calculate_control(self):
        y_pre, y = self.model.observe(2, full_state=False)
        self.f = self.f + self.eta * (y - y_pre - self.f * self.du) * self.du.transpose() / (
                    self.mu + np.power(np.linalg.norm(self.u), 2))
        # limit f between bounds
        self.f += 0.5 * (self.f < 1e-5)

        u_pre = self.u
        y_d = self.Yd[self.iteration + 1]
        self.u = self.u + self.rho * self.f * (
                (y_d - y) - self.f[1:self.nu - 1] * np.transpose(self.du[0: self.nu - 2])) / (
                         self.labda + np.power(self.f[1], 2))
        self.du = self.u - u_pre
        self.F = np.append(self.F, self.f)
        self.U = np.append(self.U, self.u)
        self.dU = np.append(self.dU, self.du)

    def calculate_zero_control(self):
        self.u = np.matrix(np.zeros([self.model.number_of_inputs, 1]))
