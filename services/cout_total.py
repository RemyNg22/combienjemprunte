from services.capacite_emprunt import mensualite_max, capital_empruntable
from services.pret_taux_zero import calcul_ptz
from models.dossier import Dossier

FRAIS_ANCIEN = 0.0955 # Comprend frais notaire 7.5% + 2% frais annexes (frais dossier, organisme cautionnement)
FRAIS_NEUF = 0.045

def calcul_projet_sans_ptz(dossier: Dossier, 
                           duree_annees: int, 
                           type_marche="ancien"):
    """
    Simulation sans PTZ
    """

    mensualite = mensualite_max(dossier)
    capital = capital_empruntable(mensualite, duree_annees)

    financement_total = capital + dossier.total_apport

    frais = FRAIS_ANCIEN if type_marche == "ancien" else FRAIS_NEUF

    prix_bien = financement_total / (1+frais)

    return {
        "type": "sans_ptz",
        "mensualite_max": mensualite,
        "credit_classique": capital,
        "ptz": 0,
        "apport": dossier.total_apport,
        "prix_bien": round(prix_bien, 2),
        "frais_estimes": round(prix_bien*frais, 2),
        "type_marche": type_marche
    }


def calcul_projet_avec_ptz(dossier: Dossier,
                           duree_annees: int,
                           zone: str,
                           type_bien="appartement",
                           type_marche="neuf"):
    """
    Simulation avec PTZ
    """

    mensualite = mensualite_max(dossier)
    capital = capital_empruntable(mensualite, duree_annees)

    #Simulation PTZ max (plafond)
    ptz_data = calcul_ptz(
        prix_bien=9999999,
        rfr=dossier.total_rfr,
        zone=zone,
        nb_personnes=dossier.nb_personnes,
        type_bien=type_bien
    )

    if not ptz_data["eligible"]:
        return None
    
    ptz_max = ptz_data["ptz"]

    financement_total = capital + dossier.total_apport + ptz_max

    frais = FRAIS_NEUF if type_marche == "neuf" else FRAIS_ANCIEN

    prix_bien = financement_total / (1+frais)

    return {
        "type": "avec_ptz",
        "type_bien": type_bien,
        "type_marche": type_marche,
        "mensualite_max": mensualite,
        "credit_classique": capital,
        "ptz": ptz_max,
        "apport": dossier.total_apport,
        "prix_bien": round(prix_bien, 2),
        "frais_estimes": round(prix_bien * frais, 2),
        "tranche": ptz_data["tranche"],
        "quotite": ptz_data["quotite"],
        "plafond_operation": ptz_data["plafond_operation"]
    }



def simulation_globale(dossier: Dossier, duree_annees: int, zone: str):
    """
    Retourne :
    - ancien sans PTZ
    - neuf avec PTZ appartement
    - neuf avec PTZ maison
    """

    if not dossier.est_valide:
        raise ValueError("Dossier invalide")

    resultats = []

    # Sans PTZ (ancien)
    resultats.append(
        calcul_projet_sans_ptz(dossier, duree_annees, type_marche="ancien")
    )

    # PTZ appartement (neuf)
    ptz_appart = calcul_projet_avec_ptz(
        dossier,
        duree_annees,
        zone,
        type_bien="appartement",
        type_marche="neuf"
    )

    if ptz_appart:
        resultats.append(ptz_appart)

    # PTZ maison (neuf)
    ptz_maison = calcul_projet_avec_ptz(
        dossier,
        duree_annees,
        zone,
        type_bien="maison",
        type_marche="neuf"
    )

    if ptz_maison:
        resultats.append(ptz_maison)

    return resultats