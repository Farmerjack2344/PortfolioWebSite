def Cmin(Cp1,m_dot_1, Cp2, m_dot_2):
    if Cp2 == 0 and m_dot_2 == 0:
        output = Cp1*m_dot_1
    elif (Cp1 * m_dot_1) > (Cp2 * m_dot_2):
        output = (Cp2 * m_dot_2)
    else:
        output = (Cp1 * m_dot_1)

    return output

