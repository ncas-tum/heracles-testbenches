import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from rawfile import rawread

T_READ_N = 1e-3
T_PRG = 1.5e-3
T_READ_P = 2.5e-3


def i_read(id: np.ndarray, time: np.ndarray) -> tuple[float, float]:
    """Extracts the read currents"""

    idx_read_n = np.searchsorted(time, 1e-3)
    idx_prg = np.searchsorted(time, 1.5e-3)
    idx_read_p = np.searchsorted(time, 2.5e-3)

    trace_read_n = id[idx_read_n:idx_prg]
    trace_read_p = id[idx_read_p:]

    i_read_p = np.mean(trace_read_p)
    i_read_n = np.mean(trace_read_n)

    return i_read_p, i_read_n


def v_delta(vgn: np.ndarray, time: np.ndarray) -> tuple[float, float]:
    """Retrieves the steady-state voltage on the floating node"""

    idx_read_n = np.searchsorted(time, 1e-3)
    idx_read_p = np.searchsorted(time, 2.5e-3)

    v_delta_p = vgn[idx_read_p - 1]
    v_delta_n = vgn[idx_read_n - 1]

    return v_delta_p, v_delta_n


def trace(filename: str, sweeps: int) -> pd.DataFrame:
    """Extracts traces from a sweeped raw file"""

    raw = rawread(filename).get(sweeps=sweeps)

    i_read_p, i_read_n = i_read(raw["vdrain:flow(br)"], raw["time"])
    v_delta_p, v_delta_n = v_delta(raw["m1:g_n"], raw["time"])

    records = {
        "i_read_p": i_read_p,
        "i_read_n": i_read_n,
        "v_delta_p": v_delta_p,
        "v_delta_n": v_delta_n,
        "time": raw["time"],
        "v_g": raw["vin"],
        "v_gn": raw["m1:g_n"],
        "i_g": -raw["vpulse_up:flow(br)"],
        "i_d": -raw["vdrain:flow(br)"],
        "p": raw["m1:x1:n1"],
    }

    df = pd.DataFrame(data=records)
    return df


if __name__ == "__main__":
    df = trace("pv.raw", 1)

    print(f"I_read_p: {df['i_read_p'].iloc[0]}")
    print(f"I_read_n: {df['i_read_n'].iloc[0]}")
    print(f"V_delta_p: {df['v_delta_p'].iloc[0]}")
    print(f"V_delta_n: {df['v_delta_n'].iloc[0]}")

    idx_read_n = np.searchsorted(df["time"], 1e-3)
    idx_prg = np.searchsorted(df["time"], 1.5e-3)
    idx_read_p = np.searchsorted(df["time"], 2.5e-3)

    fig_iv, ax_iv = plt.subplots()

    ax_iv.plot(df["v_g"].iloc[idx_read_n:idx_prg], df["i_d"].iloc[idx_read_n:idx_prg])
    ax_iv.plot(df["v_g"].iloc[idx_read_p:], df["i_d"].iloc[idx_read_p:])

    ax_iv.set_yscale("log")
    ax_iv.set_ylim([1e-12, 1e-3])
    ax_iv.set_xlim([-1, 2.5])
    ax_iv.set_xlabel("Voltage [V]")
    ax_iv.set_ylabel("Current [A]")
    ax_iv.spines["left"].set_position(("outward", 5))
    ax_iv.spines["bottom"].set_position(("outward", 5))

    fig_state, ax_state = plt.subplots()

    ax_state.plot(df["time"], df["p"])
    ax_state.plot(df["time"], df["v_g"])
    ax_state.plot(df["time"], df["v_gn"])
    ax_state.plot()

    fig_iv.savefig("transfer.svg")

    plt.show()
