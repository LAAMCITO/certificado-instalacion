import re

raw_log = """
2026-08-18 16:05:36,815 DEBUG Received: :2439312:13:0:NODE 0 3.330 4.930 19.0 99 69 6.00 9.00 0 0
2026-08-18 16:05:37,100 DEBUG Received: :2439313:1:0:NODE 0 3.250 4.880 19.0 99 69 6.00 9.00 0 0
:2:0:NODE 0 3.180 4.850 19.0 99 69 6.00 9.00 0 0
:2:0:OXY 0 10.00 12.76 8.97 96.1 20.00 0 6 0 13 0 6
:2:1:COND 0 10.00 12.72 35.67 46.67 32.13 0 6 0 0 13 13
:1:0:FLOW 0 10.00 -84.18 5.19 205.00 9 0 0 0 0
"""

def parsear_tramas_completas(texto: str):
    voltajes = {}
    sensores = {}

    pat_node1 = re.compile(r":(?:\d+:)?(\d+):\d+:NODE\s+\d+\s+([0-9]+(?:\.[0-9]+)?)\s+([0-9]+(?:\.[0-9]+)?)", re.I)
    pat_node2 = re.compile(r"\bNODE\s+(\d+)\s+([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)", re.I)

    pat_oxy = re.compile(r":(?:\d+:)?(\d+):\d+:OXY\s+(\d+)\s+([0-9.]+)\s+([0-9.-]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", re.I)
    pat_cond = re.compile(r":(?:\d+:)?(\d+):\d+:COND\s+(\d+)\s+([0-9.]+)\s+([0-9.-]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", re.I)
    pat_flow = re.compile(r":(?:\d+:)?(\d+):\d+:FLOW\s+(\d+)\s+([0-9.]+)\s+([0-9.-]+)\s+([0-9.]+)\s+([0-9.]+)", re.I)

    for linea in texto.splitlines():
        linea_s = linea.strip()
        if not linea_s:
            continue

        m_node = pat_node1.search(linea_s) or pat_node2.search(linea_s)
        if m_node:
            nodo = int(m_node.group(1))
            v_bat = float(m_node.group(2))
            v_alim = float(m_node.group(3))
            voltajes[nodo] = {'voltaje': v_bat, 'alimentacion': v_alim}

        m_oxy = pat_oxy.search(linea_s)
        if m_oxy:
            nodo = int(m_oxy.group(1))
            groups = m_oxy.groups()
            estado, cable, temp, o2, sat, sal = groups[1], groups[2], groups[3], groups[4], groups[5], groups[6]
            if nodo not in sensores: sensores[nodo] = {}
            sensores[nodo]['oxy'] = {
                'estado': int(estado), 'cable': float(cable), 'temp': float(temp),
                'o2': float(o2), 'sat': float(sat), 'sal': float(sal)
            }

        m_cond = pat_cond.search(linea_s)
        if m_cond:
            nodo = int(m_cond.group(1))
            groups = m_cond.groups()
            estado, cable, temp, cond1, cond2, sal = groups[1], groups[2], groups[3], groups[4], groups[5], groups[6]
            if nodo not in sensores: sensores[nodo] = {}
            sensores[nodo]['cond'] = {
                'estado': int(estado), 'cable': float(cable), 'temp': float(temp),
                'cond1': float(cond1), 'cond2': float(cond2), 'sal': float(sal)
            }

        m_flow = pat_flow.search(linea_s)
        if m_flow:
            nodo = int(m_flow.group(1))
            groups = m_flow.groups()
            estado, cable, factor, vel, direccion = groups[1], groups[2], groups[3], groups[4], groups[5]
            if nodo not in sensores: sensores[nodo] = {}
            sensores[nodo]['flow'] = {
                'estado': int(estado), 'cable': float(cable), 'factor': float(factor),
                'vel': float(vel), 'dir': float(direccion)
            }

    return voltajes, sensores

v, s = parsear_tramas_completas(raw_log)
print('Voltajes detectados por nodo:', v)
print('Lecturas de sensores detectadas por nodo:', s)
