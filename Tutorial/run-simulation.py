import pybamm
import matplotlib.pyplot as plt

# default DFN model
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600]) # run the simulation for 3600s = 1hr

# sim.plot(["Current [A]", "Voltage [V]"]) # plot the results

# list all model variables (we can also search for)
# print(model.variable_names())
model.variables.search("capacity") # select - Discharge capacity [A.h]
# sim.plot([["Current [A]", "Discharge capacity [A.h]"], "Voltage [V]"])

# let us store the simulation results
solution = sim.solution
voltage = solution["Voltage [V]"].data # get as 1d numpy array
# print(solution["Voltage [V]"](t=1200)) # voltage value at time t = 1200s
# print(voltage)
discharge_capacity = solution["Discharge capacity [A.h]"].data


plt.plot(voltage, discharge_capacity)
plt.xlabel('Voltage [V]')
plt.ylabel('Discharge capacity [A.h]')
plt.show()