import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from rawfile import rawread


def cv() -> tuple[Figure, Axes]:
    "Capacitance-Voltage extraction with auto-frequency detection"
    data_c = rawread("cv.raw").get(sweeps=2)
    fig, ax = plt.subplots()

    vbias = []
    capacitances = []
    conductances = []
    delay = 1e-3
    fsine_nominal = 1e4  # Expected frequency
    n_cycles = 5

    for sweep in range(data_c.sweepGroups):
        current_c = -data_c[sweep, "vpulse:flow(br)"]
        voltage_c = data_c[sweep, "vin"]
        time_c = data_c[sweep, "time"]

        t_start = delay + 0.5 / fsine_nominal
        t_end = t_start + n_cycles / fsine_nominal
        idx_start = np.searchsorted(time_c, t_start)
        idx_end = np.searchsorted(time_c, t_end)

        if idx_end - idx_start < 20:
            continue

        v_slice = voltage_c[idx_start:idx_end]
        i_slice = current_c[idx_start:idx_end]
        t_slice = time_c[idx_start:idx_end]

        t_uniform = np.linspace(t_slice[0], t_slice[-1], len(t_slice))
        v_uniform = np.interp(t_uniform, t_slice, v_slice)
        i_uniform = np.interp(t_uniform, t_slice, i_slice)
        dt = t_uniform[1] - t_uniform[0]

        v_ac = v_uniform - np.mean(v_uniform)
        i_ac = i_uniform - np.mean(i_uniform)
        dt = t_slice[1] - t_slice[0]
        N = len(v_ac)

        v_fft = np.fft.rfft(v_ac)
        i_fft = np.fft.rfft(i_ac)
        freqs = np.fft.rfftfreq(N, d=dt)

        # Auto-detect fundamental frequency (skip DC bin 0)
        mag_v = np.abs(v_fft[1:])
        idx_peak = np.argmax(mag_v) + 1  # +1 offset for skipped DC bin
        f_actual = freqs[idx_peak]

        V1 = v_fft[idx_peak] * 2.0 / N
        I1 = i_fft[idx_peak] * 2.0 / N

        if abs(V1) < 1e-12 or abs(I1) < 1e-12:
            print("Warning: Check the signal, the extracted amplitudes are very weak")
            continue

        # Admittance Y = I/V = G + jωC
        Y = I1 / V1
        G = np.real(Y)
        C = np.imag(Y) / (2.0 * np.pi * f_actual)

        capacitances.append(C)
        conductances.append(G)
        vbias.append(data_c.sweepData(sweep)["set"])

    if not capacitances:
        raise ValueError(
            "No valid data extracted. Check signal amplitude or window timing."
        )

    # Plot
    ax.plot(vbias, capacitances, "o-", label="C", markersize=4)
    ax.set_xlabel("DC Bias [V]")
    ax.set_ylabel("Capacitance [F]")
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(vbias, conductances, "s--", label="G", color="red", markersize=4)
    ax2.set_ylabel("Conductance [S]")
    ax2.set_yscale("log")
    ax2.legend(loc="upper right")

    return fig, ax


cmap = plt.get_cmap("Dark2")

fig_cv, ax_cv = cv()

plt.show()
