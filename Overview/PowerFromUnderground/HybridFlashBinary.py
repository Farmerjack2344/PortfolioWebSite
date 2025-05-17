def HybridBinaryFlashNEW(m_dot_geofluid, init_temp, final_temp, init_pressure, pressure_change, working_fluid,
                     T_injection_well, superheat, turbine_in_pressure, condenser_out_temperature,PropsSI):

    '''
    
        param m_geo_fluid:
                            The mass flow rate of the geo fluid 
        param init_temp:
                            The temperature of the geo fluid temperature at the well head
        param final_temp
                            The pressure of the geo fluid at the exhaust of
                            the flashing turbine
        param init_pressure:
                            The temperature of the geo fluid temperature at
                            the well head
        param pressure_change:
                            The change in the pressure between the wellhead
                            and the inlet at the separator
        param working_fluid:
                            This is working fluid in the ORC
        param T_injection_well:
                            This is the temperature that the geofluid is
                            when it goes into the injection well
        param superheat:
                            This is the excess heat the working fluid will
                            have to make sure that if it superheated and
                            cannot operate under the saturation dome.

        param turbine_in_pressure:
                            The presussre of the working fluid as it enters
                            the turine in the binary cycle section of the
                            ORC
        param condenser_out_temperature:
                            This is the temperatue of the working fluid as
                            it comes out of the condenser in the binary
                            cycle
    
    
    '''

    # m_dot = 85.29   kg / s
    
    dead_state = 25 + 273.15
    Turbine_efficiency = 0.85 #The isentropic efficiency is 85
    Compressor_efficiency = 0.75
    recouperator_effectiveness = 0.65
    Work_out = [0, 0, 0]

    if turbine_in_pressure == PropsSI('pcrit', working_fluid):
        print("The turbine inlet pressure is equal to the critical pressure")
    elif turbine_in_pressure > PropsSI('pcrit', working_fluid):
        raise Exception("The turbine inlet pressure is greater than the critical pressure")

    #1 - 2 Flashing

    if init_temp == 0:
        P1 = init_pressure
        T1 = PropsSI('T', 'P', P1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'P', P1, 'Q', 0, 'WATER')
        S1 = PropsSI('S', 'P', P1, 'Q', 0, 'WATER')
    elif init_pressure == 0:
        T1 = init_temp
        P1 = PropsSI('P', 'T', T1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'Q', 0, 'T', T1, 'WATER')
        S1 = PropsSI('S', 'Q', 0, 'T', T1, 'WATER')
    else:
        P1 = init_pressure
        T1 = PropsSI('T', 'P', P1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'P', P1, 'Q', 0, 'WATER')
        S1 = PropsSI('S', 'P', P1, 'Q', 0, 'WATER')


    #Define enthalpy relative to pressure and temperature because enthelpy is #relative
    H2 = H1
    P2 = P1 * pressure_change
    T2 = PropsSI('T', 'P', P2, 'H', H2, 'WATER')
    S2 = PropsSI('S', 'P', P2, 'H', H2, 'WATER')

    #2 - 4 Separating
    #2 is the mixture of liquid and vapour
    #3 is the saturated liquid stage
    #4 is saturated vapour stage

    Hg4 = PropsSI('H', 'P', P2, 'Q', 1, 'WATER')

    Hl4 = PropsSI('H', 'P', P2, 'Q', 0, 'WATER')
    S3 = PropsSI('S', 'P', P2, 'Q', 0, 'WATER')
    T3 = T2

    x2 = (H2 - Hl4) / (Hg4 - Hl4)
    x3 = 1 - x2

    if x2 > 1:
        raise Exception('It isnt physically possible for x2 to be greater than 1')



    H4 = Hg4
    T4 = T2
    P4 = P2
    S4 = PropsSI('S', 'T', T2, 'Q', 1, 'WATER')

    #4 - 5 Expansion in turbine
    mq_dot = x2 * m_dot_geofluid
    efficiency = 0.85

    T5 = final_temp #50 + 273.15
    S5s = S4
    H5s = PropsSI('H', 'S', S5s, 'T', T5, 'WATER') #HERE
    P5 = PropsSI('P', 'S', S5s, 'T', T5, 'WATER') #This works because they are on the same temperature line
    Hg5 = PropsSI('H', 'T', T5, 'Q', 1, 'WATER') #h7
    Hl5 = PropsSI('H', 'T', T5, 'Q', 0, 'WATER') #h6

    H5 = (efficiency * (H5s - H4)) + H4

    S5 = PropsSI('S', 'H', H5, 'P', P5, 'WATER')
    #S5 is supposed to be greater then S5s

    Work_out[1] = mq_dot * (H5 - H4)

    x5 = (H5 - Hl5) / (Hg5 - Hl5)

    # Binary: Stage 1 - 2(Turbine)

    P1B = turbine_in_pressure #MPa
    T_evap = PropsSI('T', 'P', P1B, 'Q', 1, working_fluid)
    T1B = T_evap + superheat
    S1B = PropsSI('S', 'Q', 1, 'P', P1B, working_fluid)
    H1B = PropsSI('H', 'Q', 1, 'P', P1B, working_fluid)
    v1 = 1 / (PropsSI('D', 'Q', 1, 'P', P1B, working_fluid))

    P2B = PropsSI('P', 'T', condenser_out_temperature, 'Q', 1, working_fluid)

    P2sB = P2B
    S2sB = S1B
    H2sB = PropsSI('H', 'S', S2sB, 'P', P2sB, working_fluid)
    T2sB = PropsSI('T', 'S', S2sB, 'P', P2sB, working_fluid)

    H2B = H1B + Turbine_efficiency * (H2sB - H1B)
    S2B = PropsSI('S', 'H', H2B, 'P', P2B, working_fluid)
    H2aB = v1 * (P2B - P1B) + H1B #Assuming the fluid is incompressible

    T2B = PropsSI('T', 'S', S2B, 'P', P2B, working_fluid)
    #Stage 3 - 4(Condenser)

    T3B = condenser_out_temperature
    P3B = P2B
    H3B = PropsSI('H', 'T', T3B, 'Q', 1, working_fluid) #H3 < H2
    S3B = PropsSI('S', 'T', T3B, 'Q', 1, working_fluid)

    T4B = T3B #Wastes space but, for my readability it is necessary
    P4B = P3B
    H4B = PropsSI('H', 'T', T4B, 'Q', 0, working_fluid)
    S4B = PropsSI('S', 'T', T4B, 'Q', 0, working_fluid)

    #Stage 4 - 5(Compressor / Pump)

    P4B = PropsSI('P', 'T', T4B, 'Q', 0, working_fluid)
    H4B = PropsSI('H', 'T', T4B, 'Q', 0, working_fluid)
    S4B = PropsSI('S', 'T', T4B, 'Q', 0, working_fluid)
    v4 = 1 / (PropsSI('D', 'T', T4B, 'Q', 0, working_fluid))

    P5B = turbine_in_pressure
    if P5B < P4B:
        raise Exception(f'The pressure(P5 = {P5B}) should be higher than P4 ({P4B})')


    P5sB = P5B
    H5sB = PropsSI('H', 'P', P5B, 'S', S4B, working_fluid)

    H5B = H4B + (H5sB - H4B) * (1 / Compressor_efficiency)
    T5B = PropsSI('T', 'P', P5B, 'H', H5B, working_fluid) #125994.162918 crit H for R218
    S5B = PropsSI('S', 'T', T5B, 'P', P5B, working_fluid)

    # Hybrid: Recouperator(7 - 8)
    pinch = 5 #K
    mq_dot_3 = x3 * m_dot_geofluid #Mass flow rate coming from the separator

    mq_dot_5 = x5 * mq_dot #Mass flow rate coming from turbine

    #Hot fluid goes through the tube
    #Cold fluid goes through the shell
    T_tube_inlet = T5 #The temperature of the geofluid out of the turbine
    P_tube_inlet = P5

    T_tube_outlet = T_injection_well

    T_shell_inlet = T5B #The temperature of the working fluid in the ORC
    P_shell_inlet = P5B

    cp_HX = PropsSI('C', 'T', T2, 'Q', 0, 'WATER')
    cp_R = PropsSI('C', 'T', T5, 'Q', 1, 'WATER')

    m_dot_ORC = (mq_dot_3 * (cp_HX) * (T2 - T_injection_well)) / (H1B - H5B)

    Cmin_val = Cmin(cp_R, mq_dot_5, PropsSI('C', 'T', T_shell_inlet, 'P', P_shell_inlet, working_fluid), m_dot_ORC)

    Qmax = Cmin_val * (T_tube_inlet - T_shell_inlet)

    H6B = H5B + ((recouperator_effectiveness * Qmax) / m_dot_ORC)

    prev_H6B = H6B - 10
    threshold = 1e-6

    change = abs(H6B - prev_H6B) / abs(H6B)

    H_values = []
    M_values = []
    differences = []
    iterations = 0

    while abs(H6B - prev_H6B) / abs(H6B) > threshold:

        m_dot_ORC = (mq_dot_3 * (cp_HX) * (T2 - T_injection_well)) / (H1B - H6B)
        M_values = [M_values, m_dot_ORC]

        #Dont think we need this

        Qmax = Cmin_val * (T_tube_inlet - T_tube_outlet)


        Cmin_val = Cmin(cp_R, mq_dot_3, PropsSI('C', 'T', T_shell_inlet, 'P', P_shell_inlet, working_fluid), m_dot_ORC)
        Q = recouperator_effectiveness * Cmin_val * (T_tube_inlet - T_shell_inlet)

        prev_H6B = H6B
        H6B = H5B + Q / m_dot_ORC

        H_values = [H_values, H6B]
        change = abs(H6B - prev_H6B) / abs(H6B)

        iterations = iterations + 1


    Work_out[2] = m_dot_ORC * (H2B - H1B)

    T_shell_out = T_shell_inlet - (Q / (m_dot_ORC * Cmin_val))

    H6l = (PropsSI('H', 'T', T_shell_out, 'Q', 1, working_fluid))
    H6g = (PropsSI('H', 'T', T_shell_out, 'Q', 0, working_fluid))

    Q6B = (H6B - H6g) / (H6l - H6g)

    P6B = P5sB

    S6B = PropsSI('S', 'Q', Q6B, 'P', P5sB, working_fluid)
    T6B = PropsSI('T', 'Q', Q6B, 'P', P5sB, working_fluid)

    Work_out[0] = mq_dot * (H5 - H4) + m_dot_ORC * (H2B - H1B)
    Work_in = m_dot_ORC * (1 / Turbine_efficiency) * (H5B - H4B)

    Heat_in = m_dot_ORC * (H6B - H5B) + m_dot_ORC * (H1B - H6B)
    Heat_out = m_dot_ORC * (H3B - H4B)

    state_entropies = [None, None]
    state_temperatures = [None, None]

    state_entropies[0] =[S1, S2, S3, S4, S5, S5s, S5s, PropsSI('S', 'T', T_injection_well, 'Q', Q6B, 'WATER')]
    state_temperatures[0]=[T1, T2, T3, T4, T5, T5, T5, T_injection_well]

    state_entropies[1] = [S1B, S2B, S2sB, S3B, S4B, S5B, S6B, S1B]
    state_temperatures[1]=[T1B, T2B, T2sB, T3B, T4B, T5B, T6B, T1B]

    state_pressures = [P1B, P2B, P2sB, P3B, P4B, P5B, P5sB, P6B, P1B]
    state_enthalpies = [H1B, H2B, H2sB, H3B, H4B, H5B, H5sB, H6B, H1B]

    CTE = (Work_in - Work_out[1]) / Heat_in

    HeatSinkSource = [min(state_entropies[1]), T3,
                      max(state_entropies[1]), T_injection_well,
                      min(state_entropies[1]), condenser_out_temperature - (Heat_out / (m_dot_ORC * 4 * PropsSI('C', 'T', dead_state, 'P', 101325, 'Air'))),
                      max(state_entropies[1]), condenser_out_temperature]


    return [Work_out, Work_in, Heat_out, Heat_in, state_entropies, state_temperatures, state_enthalpies, state_pressures, CTE, HeatSinkSource, pressure_change]