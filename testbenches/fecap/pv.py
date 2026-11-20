from time import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from rawfile import rawread


def pv() -> tuple[Figure, Axes, Axes, Axes]:
    """Polarization-Voltage hysteresis plot"""
    data_p = rawread("pv.raw").get()
    fig, (ax_iv, ax_it, ax_statet, ax_vt) = plt.subplots(4, 1)

    current_p = -data_p["vpulse:flow(br)"]
    voltage_p = data_p["vin"]
    time_p = data_p["time"]

    pol = data_p["x1.pol"]

    # polarization = cumulative_trapezoid(current_p, time_p)
    ax_iv.plot(voltage_p, current_p)
    ax_it.plot(time_p, current_p)
    # ax_statet.plot(time_p, voltage_p, label="VOLTAGE")
    ax_statet.plot(time_p, pol, label="Pol")
    ax_statet.legend()
    ax_vt.legend()

    return fig, ax_iv, ax_statet, ax_vt


def pv_sweep():
    """Polarization-Voltage hysteresis plot"""
    data_p = rawread("pvsweep.raw").get(sweeps=1)
    fig, ax = plt.subplots()

    for sweep in range(data_p.sweepGroups):
        current_p = -data_p[sweep, "vpulse:flow(br)"]
        voltage_p = data_p[sweep, "vin"]
        time_p = data_p[sweep, "time"]

        pol = data_p[sweep, "x1.pol"]

        ax.plot(voltage_p, current_p)

    ax.set_xlabel("DC Bias [V]")
    ax.set_ylabel("Capacitance [F]")
    # ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()


cmap = plt.get_cmap("Dark2")

fig_pv, ax_iv, ax_statet, ax_vt = pv()
pv_sweep()

plt.show()
