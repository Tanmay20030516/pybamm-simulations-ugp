import pybamm
import matplotlib.pyplot as plt

numCycles = 3
CCCV = pybamm.Experiment([
    (f"Discharge at 1C until 2.5V",
    "Rest for 1 hour",
    f"Charge at 2C until 4.2V",
    "Hold at 4.2V until C/50"),
] * numCycles)
model = pybamm.lithium_ion.SPMe()
parameter_values = pybamm.ParameterValues("Chen2020")
sim = pybamm.Simulation(model, experiment=CCCV, parameter_values=parameter_values)
sim.solve()
sim.plot(["Terminal voltage [V]", "Current [A]"])



constPower = pybamm.Experiment([
    ("Discharge at 5A until 2.5V",
    "Charge at 15W until 4.2V",
    "Hold at 4.2V until 0.01A")
])
sim = pybamm.Simulation(model, experiment=constPower, parameter_values=parameter_values)
# sim.solve()
# sim.plot(["Current [A]", "Terminal power [W]", "Terminal voltage [V]"])



initialSOC = pybamm.Experiment([("Charge at 1C until 4.2V", "Hold at 4.2V until C/50")])
sols = []
initial_socs = [0,0.2,0.4,0.6,0.8]
for initial_soc in initial_socs:
  sim = pybamm.Simulation(model, parameter_values=parameter_values, experiment=initialSOC)
  sol = sim.solve(initial_soc=initial_soc)
  sols.append(sol)
# pybamm.dynamic_plot(sols,labels=[f"initial soc = {x}" for x in initial_socs])
fig, ax = plt.subplots(1,2)
for sol in sols:
  cc = sol.cycles[0].steps[0]
  cv = sol.cycles[0].steps[1]
  t_cc = cc["Time [h]"].data
  t_cv = cv["Time [h]"].data
  ax[0].plot(t_cc-t_cv[0], cc["Terminal voltage [V]"].data)
  ax[0].set_title("Voltage [V] during CC")
  ax[1].plot(t_cv-t_cv[0], cv["Current [A]"].data)
  ax[1].set_title("Current [A] during CV")
  ax[1].legend([f"initial soc = {x}" for x in initial_socs])
# plt.show()