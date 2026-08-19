"""
Parser para la salida de texto plano del comando 'cmd motes' / 'cmd status' / logs Jennic.
"""

import re


def parse_cmd_motes(texto: str) -> list[dict]:
    """Parsea la salida de texto plano del comando 'cmd motes' / 'cmd status' / logs."""
    motes = []
    macs_vistas = set()

    def normalizar_mac(raw_m: str) -> str:
        clean = raw_m.strip(",;()[]\"'").replace("-", ":").upper()
        if len(clean) == 16 and ":" not in clean and re.match(r"^[0-9A-F]{16}$", clean):
            clean = ":".join(clean[i:i+2] for i in range(0, 16, 2))
        return clean

    lineas = texto.strip().splitlines()
    for linea in lineas:
        linea_str = linea.strip()
        if not linea_str:
            continue

        # Encabezados de tabla y prompts
        if "mote" in linea_str.lower() and "mac" in linea_str.lower():
            continue
        if linea_str.lower().startswith(("cmd>", "pancoordinator>", "pancoordinator#", "pancoordinator$")):
            linea_str = re.sub(r"^(?:cmd|pancoordinator)[>#$]\s*", "", linea_str, flags=re.I).strip()
        if linea_str.lower().startswith("cmd "):
            linea_str = linea_str[4:].strip()

        partes = linea_str.split()
        if len(partes) >= 2:
            # Buscar la posición de la MAC en las partes de la línea
            mac_idx = -1
            for i, p in enumerate(partes):
                p_norm = normalizar_mac(p)
                if re.match(r"^[0-9A-F]{2}(?::[0-9A-F]{2}){7}$", p_norm, re.I):
                    mac_idx = i
                    break
                elif re.match(r"^00:15:8[D]:[0-9A-F:]{11,}$", p_norm, re.I):
                    mac_idx = i
                    break

            if mac_idx != -1:
                mac = normalizar_mac(partes[mac_idx])
                if mac in macs_vistas:
                    continue
                macs_vistas.add(mac)

                # Detectar número de mote previo a la MAC
                prev_token = partes[mac_idx - 1].strip("[]().#") if mac_idx > 0 else ""
                mote = prev_token if prev_token.isdigit() else str(len(motes) + 1)

                signal = "N/D"
                last_rx = "N/D"
                name_parts = []

                # Analizar los tokens posteriores a la MAC
                tokens_post = partes[mac_idx + 1:]
                for idx, t in enumerate(tokens_post):
                    t_clean = t.strip(",;()")
                    if idx == 0 and (":" in t_clean or "/" in t_clean or t_clean.lstrip("-").isdigit() or "dbm" in t_clean.lower()):
                        signal = t_clean
                    elif idx == 1 and signal != "N/D" and (t_clean.endswith("s") or t_clean.isdigit() or ":" in t_clean):
                        last_rx = t_clean
                    else:
                        name_parts.append(t)

                name = " ".join(name_parts).strip()
                if name.isdigit():
                    asociacion = f"Equipo {name}"
                elif name:
                    asociacion = name
                else:
                    asociacion = f"Equipo {mote}"

                motes.append({
                    "mote": mote,
                    "mac": mac,
                    "signal": signal,
                    "last_rx": last_rx,
                    "name": name,
                    "asociacion": asociacion
                })
                continue

        # Regex fallback para cualquier MAC Jennic encontrada en la línea
        matches_mac = re.findall(r"(00:15:8[dD]:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2})", linea_str, re.IGNORECASE)
        if not matches_mac:
            matches_mac = re.findall(r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){7})", linea_str, re.I)
        if not matches_mac:
            matches_mac = re.findall(r"\b(00158[dD][0-9a-fA-F]{10})\b", linea_str, re.I)

        for mac_found in matches_mac:
            mac_u = normalizar_mac(mac_found)
            if mac_u not in macs_vistas:
                macs_vistas.add(mac_u)
                mote_num = str(len(motes) + 1)

                # Intentar extraer señal y voltaje de la misma línea
                sig_match = re.search(r"(?:signal|rssi|lqi)\s*[:=\s]\s*([0-9:/-]+(?:dBm)?)", linea_str, re.I)
                sig_val = sig_match.group(1) if sig_match else "N/D"

                motes.append({
                    "mote": mote_num,
                    "mac": mac_u,
                    "signal": sig_val,
                    "last_rx": "N/D",
                    "name": "",
                    "asociacion": f"Equipo {mote_num}"
                })

    return motes
