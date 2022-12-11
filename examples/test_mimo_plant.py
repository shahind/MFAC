import numpy as np
from mfac.plants.mimo import Model1

plant = Model1(initial_state=np.matrix('0.0; 0.0; 0.0; 0.0'))

for t in range(100):
    plant.step(np.matrix([[np.random.rand()],[np.random.rand()]]))
plant.render()
print(plant.predict(np.zeros([10, 2]), full_state=False))
