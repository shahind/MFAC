import time

import numpy as np
# This is temporary fix to import module from parent folder
# It will be removed when package is published
import sys

sys.path.append('../src/')
# End of fix

from src.mfac.plants.siso import Model1

plant = Model1(initial_state=np.array([0]))

for t in range(800):
    plant.step(np.array([0]))

plant.render()
