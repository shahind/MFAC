from .. import MFACInterface
import numpy as np
from random import random

class PartialFormDynamicLinearization(MFACInterface):
    @MFACInterface.initializer
    def __init__(self,
                 model,  # fitness function
                 iteration_function,  # will be called in each iteration
                 eta,  # 0 <eita <=2  Weighting Factor
                 miu,  # 0 < miu      Weighting Factor
                 rou,  # 0 < rou <= 1 Step Factor
                 lamda,  # 0 < lambda
                 reference_output,
                 simulation_time=10,
                 time_step=0.01,
                 ):
        self.u = None
        self.max_iterations = simulation_time / time_step

    def run(self):
        for self.iteration in range(self.max_iterations):
            self.u = 0
            self.model.step(self.u, self.iteration)
            self.iteration_function(self)
        return self
