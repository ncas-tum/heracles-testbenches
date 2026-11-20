import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from rawfile import rawread


def trace_sim() -> pd.DataFrame:
    raw = rawread("pv.raw").get()
    records = {
        "time": raw["time"],
        "v_in": raw["vin"],
        "i_src": -raw["vpulse:flow(br)"],
        "pol": raw["x1:n1"],
    }
    df = pd.DataFrame(data=records)
    return df


if __name__ == "__main__":
    # pos, neg = trace_exp()
    sim = trace_sim()

    fig, ax = plt.subplots()

    ax.plot(sim["v_in"], sim["i_src"] * 1e9, label="sim", color="#d95f02")

    ax.legend()
    ax.spines["left"].set_position(("outward", 5))
    ax.spines["bottom"].set_position(("outward", 5))
    ax.set_xlabel("Voltage [V]")
    ax.set_ylabel("Current [nA]")

    fig_state, ax_state = plt.subplots()
    ax_state.plot(sim["time"], sim["pol"])

    plt.show()
