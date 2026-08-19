"""
Constantes de Encargados de Área, Zonas Geográficas y Técnicos de Terreno de Innovex.
"""

ESTRUCTURA_ENCARGADOS = {
    "Rodrigo Bustamante": {
        "zonas": [
            "Chiloé"
        ],
        "tecnicos": [
            "Roger Vargas",
            "Bernardo Guenteo",
            "Freddy Blanco",
            "Orlando Andres Garate",
            "Alejandro Mansilla"
        ]
    },
    "Manuel Yovera": {
        "zonas": [
            "Pto. Montt",
            "Hornopirén",
            "Seno Reloncaví",
            "Estuario Reloncaví",
            "Calbuco",
            "Valdivia",
            "Chaitén",
            "Ayacara"
        ],
        "tecnicos": [
            "Armando Perez",
            "Cristian Norambuena",
            "Yerson Seron"
        ]
    },
    "Camilo Oyarzún": {
        "zonas": [
            "Pto. Aguirre",
            "Pto. Chacabuco",
            "Pto. Aysén",
            "Pto. Cisnes"
        ],
        "tecnicos": [
            "Mariluz Tocol",
            "Leonardo Valenzuela",
            "Luis Oyarzun",
            "Heriberto Lira"
        ]
    },
    "Francisco Vásquez": {
        "zonas": [
            "Melinka",
            "Pto. Natales",
            "Pta. Arenas (PUQ)"
        ],
        "tecnicos": [
            "Carlos Rodriguez",
            "Carlos Salinas",
            "Eduin Campos",
            "Hayran Poveda",
            "Franco Quintallana",
            "Glenn Montiel",
            "Pablo Peréz"
        ]
    }
}

# Compatibilidad con diccionario plano ENCARGADOS -> lista de tecnicos
ENCARGADOS = {
    enc: data["tecnicos"] for enc, data in ESTRUCTURA_ENCARGADOS.items()
}

# Diccionario ENCARGADOS -> lista de zonas
ZONAS_POR_ENCARGADO = {
    enc: data["zonas"] for enc, data in ESTRUCTURA_ENCARGADOS.items()
}

# Lista plana de todas las zonas geográficas únicas
TODAS_LAS_ZONAS = sorted(list({z for d in ESTRUCTURA_ENCARGADOS.values() for z in d["zonas"]}))

# Lista plana de todos los técnicos únicos
TODOS_LOS_TECNICOS = sorted(list({t for d in ESTRUCTURA_ENCARGADOS.values() for t in d["tecnicos"]}))