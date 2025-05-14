from CoolProp.CoolProp import PropsSI
def FlashCycle(m_dot, init_temp, final_temp, init_pressure, pressure_change,PropsSI):

    #1 - 2 Flashing
    
    if init_temp == 0:
        P1 = init_pressure
        T1 = PropsSI('T', 'P', P1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'P', P1, 'Q', 0, 'WATER')
        S1 = PropsSI('S', 'P', P1, 'Q', 0, 'WATER')
    elif init_pressure == 0:
        T1 = init_temp + 273.15
        P1 = PropsSI('P', 'T', T1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'Q', 0, 'T', T1, 'WATER')
        S1 = PropsSI('S', 'Q', 0, 'T', T1, 'WATER')
    else:
        P1 = init_pressure
        T1 = PropsSI('T', 'P', P1, 'Q', 0, "WATER")
        H1 = PropsSI('H', 'P', P1, 'Q', 0, 'WATER')
        S1 = PropsSI('S', 'P', P1, 'Q', 0, 'WATER')
    
    
    #Defnie enthalpy relative to pressure and temperature because enthelpy is
    #relative
    H2 = H1
    P2 = P1 * pressure_change #40e5 Pa
    T2 = PropsSI('T', 'P', P2, 'H', H2, 'WATER')
    S2 = PropsSI('S', 'P', P2, 'H', H2, 'WATER')
    
    #2 - 4 Separating(3 is the saturated liquid stage)
    
    Hg4 = PropsSI('H', 'P', P2, 'Q', 1, 'WATER')
    Hl4 = PropsSI('H', 'P', P2, 'Q', 0, 'WATER')
    
    x2 = (H2 - Hl4) / (Hg4 - Hl4)
    x3 = 1 - x2
    m_dot_q_3 = m_dot * x3
    
    if x2 > 1:
        raise Exception('It isnt physically possible for x2 to be greater than 1')
    

    
    H4 = Hg4
    T4 = T2
    P4 = P2
    S4 = PropsSI('S', 'T', T2, 'Q', 1, 'WATER')
    
    #4 - 5 Expansion in turbine
    mq_dot = x2 * m_dot
    isentropic_efficiency = 0.85
    
    T5 = final_temp + 273.15 #50 + 273.15
    S5s = S4
    
    H5s = PropsSI('H', 'S', S5s, 'T', T5, 'WATER')
    P5 = PropsSI('P', 'S', S5s, 'T', T5, 'WATER') #This works because they are on the same temperature line
    
    Hg5 = PropsSI('H', 'T', T5, 'Q', 1, 'WATER') #h7
    Hl5 = PropsSI('H', 'T', T5, 'Q', 0, 'WATER') #h6
    
    H5 = (isentropic_efficiency * (H5s - H4)) + H4
    
    S5 = PropsSI('S', 'H', H5, 'P', P5, 'WATER')
    #S5 is supposed to be greater then S5s
    
    Work_out = mq_dot * (H5 - H4)
    x5 = (H5 - Hl5) / (Hg5 - Hl5)
    
    #5 - 6 Condensation
    T5 = 50 + 273.15
    S5s = S4
    H6 = Hl5
    T6 = T5
    P6 = PropsSI('P', 'T', T6, 'Q', 0, 'WATER')
    S6 = PropsSI('S', 'T', T6, 'Q', 0, 'WATER')
    mq2_dot = x5 * m_dot
    
    heat_out = mq2_dot * (H6 - H5)
    
    S7s = S6
    P7 = P2
    H7s = PropsSI('H', 'P', P7, 'S', S7s, 'WATER')
    
    H7 = ((H7s - H6) / isentropic_efficiency) + H6
    
    Work_in = mq_dot * (H7 - H6) * 2
    
    state_entropies = [S1, S2, S4, S5, S5s, S6]
    state_temperatures = [T1, T2, T4, T5, T6, T6]
    
    efficiency = abs(abs(Work_out - Work_in) / (mq2_dot * (Hg4 - H1)))
    
    return Work_out, heat_out, state_entropies, state_temperatures, efficiency, pressure_change