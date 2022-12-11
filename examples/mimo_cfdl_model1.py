import numpy as np
import matplotlib.pyplot as plt

# import the plant and controller from MFAC
from mfac.plants.mimo import Model1
from mfac.controllers import CompactFormDynamicLinearization

# define the model and set the initial values
model = Model1(initial_state=np.matrix('0.0; 0.0; 0.0; 0.0'))

# desired output
total_time = 8
step_time = 0.01

y_d = np.array([np.matrix('0.75; 0.5')])
for k in range(int(total_time / step_time) + 1):
    yd = np.matrix('0.0; 0.0')
    yd[0] = 0.5 + 0.25 * np.cos(0.25 * np.pi * k / 100) + 0.25 * np.sin(0.5 * np.pi * k / 100)
    yd[1] = 0.5 + 0.25 * np.sin(0.25 * np.pi * k / 100) + 0.25 * np.sin(0.5 * np.pi * k / 100)
    y_d = np.append(y_d, [yd], axis=0)

# log function which will be run after each iteration
def log_function(cfdl):
    print('iteration: ', cfdl.iteration)


# define the controller
controller = CompactFormDynamicLinearization(model=model,
                                             iteration_function=log_function,
                                             time_step=step_time,
                                             reference_output=y_d,
                                             simulation_time=total_time,
                                             labda=1,
                                             eta=1,
                                             mu=1,
                                             rho=1.8,
                                             f0=np.matrix('0.5 0.2;0.2 0.5')
                                             )

# run the simulation
controller.run()

# plot the output
plt.title('Output')
plt.subplot(2, 1, 1)
plt.plot(model.Y[:, 0])
plt.plot(y_d[:, 0])
plt.xlabel("k")
plt.ylabel("y1(k)")
plt.grid()
plt.subplot(2, 1, 2)
plt.plot(model.Y[:, 1])
plt.plot(y_d[:, 1])
plt.xlabel("k")
plt.ylabel("y2(k)")
plt.grid()
plt.show()
