"""
Règles et calcul pour PTZ 2026 pris sur 
https://www.economie.gouv.fr/particuliers/emprunter-et-sassurer/pret-taux-zero-ptz-tout-ce-quil-faut-savoir#
"""

# Plafonds d'éligibilité

PLAFONDS_ELIGIBILITE = {
    "A":  [49000, 73500, 88200, 102900, 117600, 132300, 147000, 161700],
    "B1": [34500, 51750, 62100, 72450, 82800, 93150, 103500, 113850],
    "B2": [31500, 47250, 56700, 66150, 75600, 85050, 94500, 103950],
    "C":  [28500, 42750, 51300, 59850, 68400, 76950, 85500, 94050],
}

# Plafonds d'opération

PLAFONDS_OPERATION = {
    "A":  [150000, 225000, 270000, 315000, 360000],
    "B1": [135000, 202500, 243000, 283500, 324000],
    "B2": [110000, 165000, 198000, 231000, 264000],
    "C":  [100000, 150000, 180000, 210000, 240000],
}


# Plafonds par tranche

PLAFONDS_TRANCHES = {
    "A":  [25000, 31000, 37000, 49000],
    "B1": [21500, 26000, 30000, 34500],
    "B2": [18000, 22500, 27000, 31500],
    "C":  [15000, 19500, 24000, 28500],
}

# Quotité appartement

QUOTITES_APPARTEMENT = {
    1: 0.50,
    2: 0.40,
    3: 0.40,
    4: 0.20,
}

# Quotité maison

QUOTITES_MAISON = {
    1: 0.30,
    2: 0.20,
    3: 0.20,
    4: 0.10,
}


# FONCTIONS

