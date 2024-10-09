import pybamm
import matplotlib.pyplot as plt
import numpy as np


model = pybamm.lithium_ion.DFN()

# Trying different C-rates
# sim1 = pybamm.Simulation(model, C_rate=1)
# sim1.solve([0, 3600])
# sol1 = sim1.solution

# sim2 = pybamm.Simulation(model, C_rate=2)
# sim2.solve([0, 3600])
# sol2 = sim2.solution

# sim3 = pybamm.Simulation(model, C_rate=0.5)
# sim3.solve([0, 3600])
# sol3 = sim3.solution

# sols = [sol3, sol1, sol2]
# labels = ["0.5C", "1C", "2C"]

# plot for both charge rates
# pybamm.dynamic_plot(sols,["Voltage [V]"], labels=labels)

# fig, ax = plt.subplots()
# for solution, label in zip(sols, labels):
#     discharge_capacity = solution["Discharge capacity [A.h]"].data
#     voltage = solution["Voltage [V]"].data
#     ax.plot(discharge_capacity, voltage, label=label)
# ax.set_xlabel("Discharge capacity [A.h]")
# ax.set_ylabel("Voltage [V]")
# ax.legend()
# plt.show()


# Check other parameter values in pybamm.Simulation(model, parameter_values = params)
# https://docs.pybamm.org/en/stable/source/api/parameters/parameter_sets.html#
params = pybamm.ParameterValues("Chen2020")
# print(params)
# not all parameters needed in model
# print(model.print_parameter_info()) # rather important in deciding parameters for a particular simulation
params = { # we can update the keys of below params dict
    ...:...,
    "Lower voltage cut-off [V]" : ...,
    "Upper voltage cut-off [V]" : ...,
    "Number of cells connected in series to make a battery" : ...,
    "Initial temperature [K]" : ...,
    "Nominal cell capacity [A.h]" : ...,
    ...:...
}

# try with some other parameters
def my_current(t):
    return -0.1 * pybamm.sin(2*np.pi*t/60)
params["Current function [A]"] = my_current
sim = pybamm.Simulation(model, parameter_values=params)
sim.solve([0, 180])
sim.plot(["Current [A]", "Terminal voltage [V]"])
