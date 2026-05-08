import matplotlib.pyplot as plt
import numpy as np
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit

logger = Logging.setup_logging()

steps = 20

tstep = 1e-8
tstop = 1.2e-3

vset_list = np.linspace(-4, 4, steps)
vreset_list = [-4, 4]
tpulse = 1e-6
vsine = 42e-3
fsine = 10e3
tsine = 1e-3

splice = (tstop - tsine) / tstep

fig, ax = plt.subplots(figsize=[3.45, 2.3])
fig_raw, ax_raw = plt.subplots(nrows=2, sharex=True, figsize=[3.45, 2.3])
for index_reset, vreset in enumerate(vreset_list):
    capacitances = []

    for index_set, vset in enumerate(vset_list):
        run = index_reset * len(vset_list) + (index_set + 1)
        logger.info(f"Run: {run} {vreset:.4g} V -> {vset:.4g} V")

        circuit = Circuit("FeCap parameter extraction")
        circuit.raw_spice = f"""
            .options reltol=0.001 abstol=1e-12 gmin=1e-12 method=Gear

            * Load OSDI model
            .control
            pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
            .endc

            * Model definition with current parameters
            .model fecap heracles (
                + area = 1e-12
                + t_fe = 10e-9
                + t_int = 0.5e-9
                + eps_fe = 70
                + eps_int = 7
                + w_b = 1.05
                + d_e = 7.5e-9
                + e_off = 1e7
                + p_s = 20e-2
                + n_depl = 1.2e28
                + eps_depl = 2.2
                + q_fix_depl_u = -8e-2
                + q_fix_depl_d = 20e-2
                + m_eff_fe = 0.4
                + m_eff_int = 0.3
                + phi_b_fe = 2
                + phi_b_int = 2.7
                + mu_fe = 0.2
                + n_c_fe = 1e24
                + phi_tr_fe = 1.05
                + area_mc = 0
                + t_fe_mc = 0
                + t_int_mc = 0
                + p_s_mc = 0
                + n_depl_mc = 0)

            * Circuit elements
            V1 vin_i 0 PULSE ( {vreset} {vset} {tpulse} 1n 1n 1k 2k )
            V2 vin vin_i SIN ( 0 {vsine} {fsine} {tsine} 0 0 )
            R1 vin te 50
            N1 te be fecap
            R2 be 0 50

            .probe I(V1)
            .save vin @n1[c_depl_tot]
            """

        simulator = circuit.simulator(temperature=21, nominal_temperature=21)
        analysis = simulator.transient(tstep, tstop)

        time = analysis.time
        voltage = analysis.vin
        current = analysis.v1
        c_depl_tot = analysis["@n1[c_depl_tot]"]

        index_lo = np.searchsorted(time, tsine + 1 / fsine)
        index_hi = np.searchsorted(time, tsine + 2 / fsine)
        vmax_index = np.argmax(voltage[index_lo:index_hi])
        vmin_index = np.argmin(voltage[index_lo:index_hi])
        imax_index = np.argmax(current[index_lo:index_hi])
        imin_index = np.argmin(current[index_lo:index_hi])

        ax_raw[0].plot(time[index_lo:index_hi], voltage[index_lo:index_hi])
        ax_raw[1].plot(time[index_lo:index_hi], current[index_lo:index_hi])

        v_amplitude = (
            voltage[index_lo + vmax_index] - voltage[index_lo + vmin_index]
        ) / 2
        i_amplitude = (
            current[index_lo + imax_index] - current[index_lo + imin_index]
        ) / 2

        z_abs = float(v_amplitude / i_amplitude)
        z_phase = float((time[vmax_index] - time[imax_index]) * fsine * 2 * np.pi)
        impedance = z_abs * np.exp(1j * z_phase)

        c = -1 / np.imag(impedance) / 2 / np.pi / fsine
        capacitances.append(c)

    ax.plot(vset_list, capacitances)

fig.savefig("cv.png", dpi=600)
