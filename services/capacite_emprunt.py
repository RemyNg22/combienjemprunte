from services.regles import TAUX_ENDETTEMENT, get_taux
from models.dossier import Dossier

def mensualite_max(dossier: Dossier):
    """
    Permet de déterminer quelle est la mensualité max 
    possible pour un emprunt immobilier
    """
    if not dossier.est_valide:
        raise ValueError("Le dossier doit contenir au moins un client")

    revenus = dossier.total_revenus
    charges = dossier.total_charges

    return max((revenus * TAUX_ENDETTEMENT) - charges, 0)


def capital_empruntable(mensualite, duree_annees):
    """
    A l'aide de la mensualité et de la durée, cette 
    fonction calcul le capital possible avec le taux 
    en vigueur selon la durée choisie
    """
    taux_annuel = get_taux(duree_annees)

    taux_mensuel = taux_annuel/100/12
    nb_mois = duree_annees*12

    if taux_mensuel==0:
        return mensualite * nb_mois
    
    capital = mensualite * (1 - (1+taux_mensuel)**-nb_mois) / taux_mensuel
    return round(capital, 2)