import pybamm
import numpy as np
import matplotlib.pyplot as plt

parameter_values = pybamm.ParameterValues("Mohtat2020")
parameter_values.update({"SEI kinetic rate constant [m.s-1]": 1e-14})
spm = pybamm.lithium_ion.SPM({"SEI": "ec reaction limited"})
numCycles = 100
experiment = pybamm.Experiment([
    ("Charge at 1C until 4.2V",
     "Hold at 4.2V until C/50",
     "Discharge at 1C until 2V",
     "Rest for 1 hour")
] * numCycles,
termination="80% capacity"
)
sim = pybamm.Simulation(spm, experiment=experiment, parameter_values=parameter_values)
sol = sim.solve()
# sim.plot(["Current [A]", "Terminal voltage [V]"])
# sim.plot([
#     "Negative electrode stoichiometry",
#     "Positive electrode stoichiometry",
#     "Total lithium in particles [mol]",
#     "Loss of lithium to negative SEI [mol]",
#     "X-averaged negative total SEI thickness [m]",
# ])


# Plotting summary variables (shows how battery degrades overtime)
# sorted(sol.summary_variables.keys())
vars_to_plot = [
    "Capacity [A.h]",
    "Loss of lithium inventory [%]",
    "x_100",
    "x_0",
    "y_100",
    "y_0"
]
l = len(vars_to_plot)
n = int(l//np.sqrt(l))
m = int(np.ceil(l/n))
fig, axes = plt.subplots(n,m,figsize=(10,6))
for var, ax in zip(vars_to_plot,axes.flat):
    ax.plot(sol.summary_variables["Cycle number"], sol.summary_variables[var])
    ax.set_xlabel("Cycle number")
    ax.set_ylabel(var)
    ax.set_xlim([1,sol.summary_variables["Cycle number"][-1]])
fig.tight_layout()
plt.show()
