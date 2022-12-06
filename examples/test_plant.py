import numpy as np
from mfac.plants.siso import Model1

plant = Model1(initial_state=np.array([0]))

for t in range(800):
    plant.step(np.array([0]))
plant.render()
