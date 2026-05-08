import matplotlib.pyplot as plt
import numpy as np
from rawfile import rawread
from scipy.integrate import cumulative_trapezoid

data_p = rawread("tran1.raw").get()
data_c = rawread("tran2.raw").get(sweeps=2)

current_p = -data_p["vin:flow(br)"]
voltage_p = data_p["vin"]
time_p = data_p["time"]
polarization = cumulative_trapezoid(current_p, time_p)

cmap = plt.get_cmap("Dark2")
fig_p, (ax_iv, ax_pv) = plt.subplots(2, 1, sharex=True)
fig_c, ax_c = plt.subplots()

# vbias = np.linspace(-4, 4, 11)
# vbias = np.concatenate([vbias, vbias])
vbias = []
capacitances = []
fsine = 1e4

for sweep in range(data_c.sweepGroups):
    current_c = -data_c[sweep, "vpulse:flow(br)"]
    voltage_c = data_c[sweep, "vin"]
    time_c = data_c[sweep, "time"]
    index = np.searchsorted(time_c, 1.0e-3 + 1 / fsine)
    index_hi = np.searchsorted(time_c, 1.0e-3 + 2 / fsine)

    vmax_index = np.argmax(voltage_c[index:index_hi])
    vmin_index = np.argmin(voltage_c[index:index_hi])
    imax_index = np.argmax(current_c[index:index_hi])
    imin_index = np.argmin(current_c[index:index_hi])

    v_amplitude = (voltage_c[index + vmax_index] - voltage_c[index + vmin_index]) / 2
    i_amplitude = (current_c[index + imax_index] - current_c[index + imin_index]) / 2

    z_abs = float(v_amplitude / i_amplitude)
    z_phase = float(
        (time_c[index + vmin_index] - time_c[index + imin_index]) * fsine * 2 * np.pi
    )
    impedance = z_abs * np.exp(1j * z_phase)

    c = 1 / np.imag(impedance) / 2 / np.pi / fsine
    capacitances.append(c)
    vbias.append(data_c.sweepData(sweep)["set"])

# ax_c.plot(time_c, voltage_c / v_amplitude)
# ax_c.plot(time_c, current_c / i_amplitude)
ax_iv.plot(voltage_p, current_p)
ax_pv.plot(voltage_p[1:], polarization)
ax_c.plot(vbias, capacitances)
# ax_c.set_ylim([-1.5, 1.5])
# ax_c.set_xlim([1e-3, 1.2e-3])

ax_c.set_xlabel("Voltage [V]")
ax_c.set_ylabel("Capacitance [C]")

fig_p.savefig("hysteresis_p.png", dpi=300)
fig_c.savefig("hysteresis_c.png", dpi=300)
