.title Capacitance-Voltage hysteresis

.param vreset=-4 vset=2 vsine=42m
.param tpulse=1u tsine=1m
.param fsine=10k

.options warn=1
.model fecap heracles
.include modelcard.l

V1 vin_i 0 PULSE ( {vreset} {vset} {tpulse} 1n 1n 1k 2k )
V2 vin vin_i SIN ( 0 {vsine} {fsine} {tsine} 0 0 )
R1 vin te 50
N1 te be fecap
R2 be 0 50

.probe I(V1)
.control
    let start_vset = 0
    let stop_vset = 4
    let delta_vset = 0.1
    let v_act = start_vset
    while v_act le stop_vset
        alter vset v_act
        pre_osdi ../include/heracles_v0.2.1__osdi_v0.3.osdi
        tran 100n 1.2m
        write cv.raw
        set appendwrite
        let v_act = v_act + delta_vset
    end
.endc

.end
