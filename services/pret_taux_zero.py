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

# Coefficient familial

COEFFICIENT_FAMILIAL = {
    1: 1,
    2: 1.5,
    3: 1.8,
    4: 2.1,
    5: 2.4,
}


# FONCTIONS

def get_coefficient_familial(nb_personnes: int) -> float:
    """
    Retourne le coefficient familial
    """
    if nb_personnes <= 0:
        raise ValueError("Nombre de personnes invalide")

    if nb_personnes >= 5:
        return COEFFICIENT_FAMILIAL[5]

    return COEFFICIENT_FAMILIAL[nb_personnes]


def est_eligible(rfr: float, zone: str, nb_personnes: int) -> bool:
    """
    Vérifie si le client est éligible au PTZ
    """
    plafonds = PLAFONDS_ELIGIBILITE[zone]

    if nb_personnes >= 8:
        plafond = plafonds[7]
    else:
        plafond = plafonds[nb_personnes - 1]

    return rfr <= plafond

def calcul_tranche(rfr: float, zone: str, nb_personnes: int):
    """
    Détermine la tranche PTZ (1 à 4)
    """
    coeff = get_coefficient_familial(nb_personnes)
    rfr_corrige = rfr / coeff

    plafonds = PLAFONDS_TRANCHES[zone]

    for i, plafond in enumerate(plafonds):
        if rfr_corrige <= plafond:
            return i + 1

    return 4


def get_plafond_operation(zone:str, nb_personnes: int):
    """
    Détermine le plafonds d'opération possible
    """
    plafonds = PLAFONDS_OPERATION[zone]

    if nb_personnes >=5:
        return plafonds[4]
    else:
        return plafonds[nb_personnes - 1]
    

def get_quotite(tranche: int, type_bien: str):
    """
    Retourne la quotité en fonction du type de bien
    """

    if type_bien == "maison":
        return QUOTITES_MAISON[tranche]
    else:
        return QUOTITES_APPARTEMENT[tranche]
    

def calcul_ptz(prix_bien: float,
               rfr: int,
               zone: str,
               nb_personnes: int,
               type_bien: str = "appartement"):
    """
    Fonction de calcul du PTZ avec Barème 2026 (Lissage et Mensualités)
    """

    if not est_eligible(rfr, zone, nb_personnes):
        return {
            "eligible": False,
            "ptz": 0,
            "mensualite_ptz": 0,
            "tranche": None,
            "quotite": 0
        }
    
    tranche = calcul_tranche(rfr, zone, nb_personnes)

    quotite = get_quotite(tranche, type_bien)

    plafond = get_plafond_operation(zone, nb_personnes)

    base = min(prix_bien, plafond)

    montant_ptz = base * quotite

    durees_p2 = {
        1: 15,
        2: 12,
        3: 13,
        4: 10
    }
    
    differes_p1 = {
        1: 10,
        2: 8,
        3: 2,
        4: 0
    }

    annees_p2 = durees_p2.get(tranche, 10)
    annees_p1 = differes_p1.get(tranche, 0)

    mensualite_ptz = 0
    if montant_ptz > 0:
        mensualite_ptz = montant_ptz / (annees_p2 * 12)

    return {
        "eligible": True,
        "ptz": round(montant_ptz, 2),
        "mensualite_ptz": round(mensualite_ptz, 2),
        "tranche": tranche,
        "quotite": quotite,
        "plafond_operation": plafond,
        "base_calcul": base,
        "duree_differe_p1": annees_p1,
        "duree_remboursement_p2": annees_p2,
        "total_duree": annees_p1 + annees_p2
    }