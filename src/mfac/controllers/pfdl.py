from .. import MFACInterface
import numpy as np
from random import random


class PartialFormDynamicLinearization(MFACInterface):
    @MFACInterface.initializer
    def __init__(self,
                 model,  # plant model
                 iteration_function,  # will be called in each iteration
                 eta,  # 0 <eta <=2   Weighting Factor
                 mu,  # 0 < mu      Weighting Factor
                 rho,  # 0 < rho <= 1 Step Factor
                 labda,  # 0 < labda
                 nu,  # nu > 1
                 reference_output,
                 simulation_time=10,
                 time_step=0.01,
                 mimo=False,
                 ):
        self.max_iterations = int(simulation_time / time_step)
        self.eta = eta
        self.mu = mu
        self.rho = rho
        self.labda = labda
        self.Yd = reference_output
        self.is_mimo = mimo
        self.model = model
        self.nu = nu
        self.iteration_function = iteration_function
        self.u = np.zeros(self.model.number_of_inputs)
        self.fai = np.zeros([self.model.number_of_outputs, self.model.number_of_inputs])
        self.du = np.zeros([self.model.number_of_inputs,self.nu])
        self.U = np.array([self.u])
        self.Fai = np.array([self.fai])
        self.dU = np.array([self.du])
        self.iteration = 0

    def run(self):
        for self.iteration in range(self.max_iterations):
            self.calculate_zero_control() if self.iteration < 2 else self.calculate_control()
            self.model.step(self.u)
            self.iteration_function(self)
        return self

    def calculate_control(self):
        y_pre, y = self.model.observe(2, full_state=False)
        self.fai = self.fai + self.eta * (y - y_pre - self.fai * np.transpose(self.du)) * self.du / (
                self.mu + self.du * np.transpose(self.du))
        if self.fai < 1e-5:
            self.fai = 0.5
        u_pre = self.u
        y_d = self.Yd[self.iteration + 1]
        self.u = self.u + self.rho * self.fai * (
                (y_d - y) - self.fai[1:self.nu - 1] * np.transpose(self.du[0: self.nu - 2])) / (
                         self.labda + np.power(self.fai[1], 2))
        self.du = self.u - u_pre
        self.Fai = np.append(self.Fai, self.fai)
        self.U = np.append(self.U, self.u)
        self.dU = np.append(self.dU, self.du)

    def calculate_zero_control(self):
        self.u = np.zeros(self.model.number_of_inputs)
