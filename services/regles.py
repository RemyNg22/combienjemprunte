"""
Ici seront toutes les règles globales de taux, taux d'endettement max, etc..
Dernière mise à jour manuelle : avril 2026
"""

TAUX_ENDETTEMENT = 0.34 # Mettons 34%, un peu inférieur au taux HCSF 35% car calculerons mensualité hors assurance

TAUX_CREDIT = {
    "7 ans" : 3.18,
    "10 ans" : 3.35,
    "15 ans" : 3.52,
    "20 ans" : 3.61,
    "25 ans" : 3.70,
}


def get_taux(duree_annees: int) -> float:
    """
    Permet d'utiliser les taux de TAUX_CREDIT simplement
    """
    cle = f"{duree_annees} ans"

    if cle not in TAUX_CREDIT:
        raise ValueError(f"Taux non défini pour {duree_annees} ans")

    return TAUX_CREDIT[cle]
