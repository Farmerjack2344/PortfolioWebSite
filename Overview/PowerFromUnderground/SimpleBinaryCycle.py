from Overview.PowerFromUnderground.linspace import linspace


def SimpleBinary(working_fluid, m_dot_geo_fluid, reservoir, superheat, turbine_in_pressure, condenser_out_temperature,PropsSI):

    """
    working_fluid:        string
                          This is the working fluid in the ORC

    m_dot_geo_fluid:      double
                          In kg/s
                          This will be the mass flow rate from the production well
                          to the injection well

                          This value will be known from the geothermal resevoir

    T_production:         double
                          This will be the temperature in Kelvin of ther fluid of the
                          production well

                          This value will be known from the geothermal resevoir

    T_injection_well:     double
                          This will be the temperature in Kelvin of the fluid of
                          the injection well

                          This will be a design parameter that we change

    superheat:            double
                          This is the temperature difference between the temperature at the outlet
                          and the evaporation temperature of the working fluid

                          This is a design parameter

    turbine_in_pressure:  double
                          This is the pressure of the working fluid at the inlet
                          of the turbine

                          This is a design parameter(This may likely be fixed)

    condenser_out_temperature: double
                               This is the low temperature of the cycle
                               This is the outlet at the condenser

                               This is a design parameter(This may likely be fixed)


    """


    T_production = reservoir[0]
    T_injection_well = reservoir[1]


    dead_state = 25 + 273.15
    Turbine_efficiency = 0.85#The isentropic efficiency is 85#
    Compressor_efficiency = 0.75

    #Stage 1-2 (Turbine)

    P1 = turbine_in_pressure#MPa
    T_evap = PropsSI('T', 'P', P1 ,'Q', 1 , working_fluid)
    T1 = T_evap + superheat
    S1 = PropsSI('S', 'Q', 1, 'P', P1, working_fluid)
    H1 = PropsSI('H', 'Q', 1, 'P', P1, working_fluid)
    v1 = 1/(PropsSI('D', 'Q', 1, 'P', P1, working_fluid))


    P2 = PropsSI('P', 'T', condenser_out_temperature,'Q', 1, working_fluid)

    P2s = P2
    S2s = S1
    H2s = PropsSI('H', 'S', S2s, 'P', P2s, working_fluid)
    T2s = PropsSI('T', 'S', S2s, 'P', P2s, working_fluid)

    H2 = H1 + Turbine_efficiency*(H2s - H1)
    S2 = PropsSI('S', 'H', H2, 'P', P2, working_fluid)
    H2a = v1 * (P2 - P1) + H1 #Assuming the fluid is incompressible

    T2 = PropsSI('T', 'S', S2, 'P', P2, working_fluid)





    #Stage 3-4 (Condenser)


    T3 = condenser_out_temperature
    P3 = P2
    H3 = PropsSI('H', 'T', T3, 'Q', 1, working_fluid) #H3<H2
    S3 = PropsSI('S', 'T', T3, 'Q', 1, working_fluid)



    T4 = T3#Wastes space but, for my readability it is necessary
    P4 = P3
    H4 = PropsSI('H', 'T', T4, 'Q', 0, working_fluid)
    S4 = PropsSI('S', 'T', T4, 'Q', 0, working_fluid)

    #Stage 4-5 (Compressor/Pump)


    P4 = PropsSI('P', 'T', T4, 'Q', 0, working_fluid)
    H4 = PropsSI('H', 'T', T4, 'Q', 0, working_fluid)
    S4 = PropsSI('S', 'T', T4, 'Q', 0, working_fluid)
    v4 = 1/(PropsSI('D', 'T', T4, 'Q', 0, working_fluid))



    P5 = turbine_in_pressure
    if P5 < P4:
        raise Exception(f'The pressure(P5 = {P5}) should be higher than P4 ({P4})',P5,P4)

    P5s  = P5
    H5s = PropsSI('H','P',P5,'S',S4,working_fluid)

    H5 = H4 + (H5s-H4)*(1/Compressor_efficiency)
    S5 = PropsSI('S', 'P', P5, 'H', H5, working_fluid)
    T5 = PropsSI('T', 'P', P5, 'H', H5, working_fluid)




    #Stage 5-6 (Heat Exchanger)

    P6 = P1
    T6 = T1
    H6 = PropsSI('H', 'P', P6, 'Q', 0, working_fluid)
    S6 = PropsSI('S', 'T', T6, 'Q', 0, working_fluid)


    #Outputs
    cp = PropsSI('C', 'T',T5,'P',P5,'Water')#4184
    m_dot_working = (m_dot_geo_fluid*cp*(T_production-T_injection_well))/(H1-H5)

    Work_out = m_dot_working * (H1-H2)

    Work_in = m_dot_working * (1/Turbine_efficiency) * (H5-H4)

    Heat_out = m_dot_working *(H3-H4)#Heat taken out of the working fluid into the environment

    Heat_in = m_dot_working * (H1 - H5)#The heat transferred to the wokring fluid from the Geofluid

    state_temperatures = [T1, T2, T2s, T3, T4, T5, T6,T1]
    state_entropies = [S1, S2, S2s, S3, S4, S5, S6,S1]

    state_pressures = [P1, P2, P2s, P3, P4, P5, P5s, P6,P1]
    state_enthalpies = [H1, H2, H2s, H3, H4, H5, H5s, H6,H1]

    CTE =  abs(Work_in-Work_out)/Heat_in
    #efficiency_actual = abs(Work_out)/Heat_in
    #efficiency_carnot = 1 - (T4/T6)
    #CTE = efficiency_actual/efficiency_carnot

    HeatSinkSource =[ min(state_entropies), T_production,
                      max(state_entropies), T_injection_well,
                      min(state_entropies), condenser_out_temperature - (Heat_out/(m_dot_working*4*PropsSI('C','T', dead_state,'P', 101325, 'Air'))),#Inlet
                      max(state_entropies), condenser_out_temperature]#Outlet condenser_out_temperature

    Tmin = PropsSI('Tmin', working_fluid)
    Tmax = PropsSI('Tcrit', working_fluid)

    S_liq = []
    S_vap = []

    temperature_range = linspace(Tmin, Tmax, 300)

    for temperature in temperature_range:
        try:
            S_liq.append(PropsSI('S','T',temperature,'Q',0,working_fluid))
            S_vap.append(PropsSI('S','T',temperature,'Q',1,working_fluid))
        except Exception as error:
            print(error)
            pass
    S_liq_vap = [S_liq, S_vap]

    Pmin = PropsSI('pmin', working_fluid)
    Pmax = PropsSI('pcrit', working_fluid)

    H_liq = []
    H_vap = []

    pressure_range = linspace(Pmin, Pmax, 300)

    for pressure in pressure_range:
        try:
            H_liq.append(PropsSI('H', 'P', pressure, 'Q', 0, working_fluid))
            H_vap.append(PropsSI('H', 'P', pressure, 'Q', 1, working_fluid))
        except Exception as error:
            print(error)
            pass


    H_liq_vap = [H_liq, H_vap]

    saturation_dome = [temperature_range, S_liq, S_vap, pressure_range,  H_liq, H_vap]

    output = {'Work_out': Work_out, 'Work_in':Work_in, 'Heat_out': Heat_out, 'state_entropies':state_entropies, 'state_temperatures':state_temperatures,'state_pressures': state_pressures,
              'state_enthalpies': state_enthalpies,'CTE':CTE, 'HeatSinkSource': HeatSinkSource, 'saturation_dome':saturation_dome}
    return output

# T_production = 165+273.15
# working_fluid = "R601"
# Work_out, Work_in, Heat_out, Heat_in, state_entropies, state_temperatures, state_pressures, state_enthalpies, CTE, HeatSinkSource = SimpleBinary(working_fluid, 442.5, [T_production, 136+273.15] , 0, 15.5e5, 317.885)
#
# for i in [Work_out, Work_in, Heat_out, Heat_in, state_entropies, state_temperatures, state_pressures, state_enthalpies, CTE, HeatSinkSource]:
#     print(i)
#     print("\n"*5)