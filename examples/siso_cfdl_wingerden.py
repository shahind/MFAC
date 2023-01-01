import numpy as np
import matplotlib.pyplot as plt

# import the plant and controller from MFAC
from mfac.plants.siso import Wingerden
from mfac.controllers import CompactFormDynamicLinearization

# define the model and set the initial values
model = Wingerden(initial_state=np.matrix('0.0; 0.0; 0.0; 0.0; 0.0'))

# desired output
total_steps = 3000

y_d = np.zeros(total_steps + 1)
for k in range(total_steps + 1):
    y_d[k] = 50 + 50*np.power(-1, np.round((k+500)/500))

# log function which will be run after each iteration
def log_function(cfdl):
    print('iteration: ', cfdl.iteration)

# define the controller
controller = CompactFormDynamicLinearization(model=model,
                                             iteration_function=log_function,
                                             reference_output=y_d,
                                             max_steps=total_steps,
                                             labda=0.007,
                                             eta=0.0024,
                                             mu=0.005,
                                             rho=0.00002,
                                             )

# run the simulation
controller.run()

# plot the output
fig, ax = plt.subplots()
ax.plot(model.Y)
ax.plot(y_d)
ax.set(xlabel='time (k)', ylabel='output (y(k))',
       title='system output')
ax.grid()
# fig.savefig("test.png")
plt.show()
