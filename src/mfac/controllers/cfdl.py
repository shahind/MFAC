from .. import MFACInterface
import numpy as np


class CompactFormDynamicLinearization(MFACInterface):
    @MFACInterface.initializer
    def __init__(self,
                 model,  # plant model
                 iteration_function,  # will be called in each iteration
                 eta,  # 0 <eta <=2   Weighting Factor
                 miu,  # 0 < miu      Weighting Factor
                 rou,  # 0 < rou <= 1 Step Factor
                 lamda,  # 0 < lambda
                 reference_output,
                 simulation_time=10,
                 time_step=0.01,
                 mimo=False,
                 ):
        self.max_iterations = int(simulation_time / time_step)
        self.eta = eta
        self.miu = miu
        self.rou = rou
        self.lamda = lamda
        self.Yd = reference_output
        self.is_mimo = mimo
        self.model = model
        self.nu = self.model.number_of_inputs
        self.iteration_function = iteration_function
        self.u = np.array([0] * self.nu)
        self.fai = np.array([0] * self.nu)
        self.du = np.array([0] * self.nu)
        self.U = np.array([np.array([0] * self.nu)])
        self.Fai = np.array([np.array([0] * self.nu)])
        self.dU = np.array([np.array([0] * self.nu)])
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
                    self.miu + self.du * np.transpose(self.du))
        if self.fai < 1e-5:
            self.fai = 0.5
        u_pre = self.u
        y_d = self.Yd[self.iteration + 1]
        if self.nu == 1:
            self.u = self.u + self.rou * self.fai * (y_d - y) / (self.lamda + np.power(self.fai, 2))
        else:
            self.u = self.u + self.rou * self.fai * (
                        (y_d - y) - self.fai[1:self.nu - 1] * np.transpose(self.du[0: self.nu - 2])) / (
                                 self.lamda + np.power(self.fai[1], 2))
        self.du = self.u - u_pre
        self.Fai = np.append(self.Fai, self.fai)
        self.U = np.append(self.U, self.u)
        self.dU = np.append(self.dU, self.du)

    def calculate_zero_control(self):
        self.u = np.array([0] * self.nu)
