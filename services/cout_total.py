from services.capacite_emprunt import mensualite_max, capital_empruntable
from services.pret_taux_zero import est_eligible, calcul_tranche, get_quotite, get_plafond_operation
from models.dossier import Dossier

FRAIS_ANCIEN = 0.0955
FRAIS_NEUF = 0.045


def _cout_interets(mensualite: float, capital: float, duree_annees: int) -> float:
    return round(max(mensualite * duree_annees * 12 - capital, 0), 2)


def calcul_projet_sans_ptz(dossier: Dossier, duree_annees: int, type_marche="ancien"):
    mensualite = mensualite_max(dossier)
    capital = capital_empruntable(mensualite, duree_annees)
    financement_total = capital + dossier.total_apport
    frais = FRAIS_ANCIEN if type_marche == "ancien" else FRAIS_NEUF
    prix_bien = financement_total / (1 + frais)

    return {
        "type": "sans_ptz",
        "mensualite_max": round(mensualite, 2),
        "mensualite_classique": round(mensualite, 2),
        "mensualite_ptz": 0,
        "credit_classique": round(capital, 2),
        "ptz": 0,
        "apport": round(dossier.total_apport, 2),
        "prix_bien": round(prix_bien, 2),
        "frais_estimes": round(prix_bien * frais, 2),
        "type_marche": type_marche,
        "cout_interets": _cout_interets(mensualite, capital, duree_annees),
        "duree_differe_p1": 0,
        "duree_remboursement_p2": duree_annees,
        "total_duree": duree_annees,
    }


def calcul_projet_avec_ptz(dossier: Dossier, duree_annees: int, zone: str,
                           type_bien="appartement", type_marche="neuf"):
    """
    Simulation avec PTZ — résolution itérative.

    Règle de lissage bancaire (pire cas, conforme HCSF) :
    La mensualité du crédit classique est calculée sur toute sa durée,
    en déduisant la mensualité PTZ (phase 2). C'est la contrainte la plus stricte.

    Note : appart peut avoir un budget légèrement inférieur à maison si la mensualité
    PTZ (plus élevée car quotité plus grande) consomme plus de capacité classique.
    Mais le coût total des intérêts est toujours inférieur grâce au PTZ gratuit.
    """
    mensualite_totale_max = mensualite_max(dossier)

    if not est_eligible(dossier.rfr, zone, dossier.nb_personnes):
        return None

    tranche = calcul_tranche(dossier.rfr, zone, dossier.nb_personnes)
    quotite = get_quotite(tranche, type_bien)
    plafond_op = get_plafond_operation(zone, dossier.nb_personnes)

    durees_p2 = {1: 15, 2: 12, 3: 13, 4: 10}
    differes_p1 = {1: 10, 2: 8, 3: 2, 4: 0}
    annees_p2 = durees_p2[tranche]
    annees_p1 = differes_p1[tranche]

    # Estimation initiale sans PTZ
    capital_classique = capital_empruntable(mensualite_totale_max, duree_annees)
    prix_estime = (dossier.total_apport + capital_classique) / (1 + FRAIS_NEUF)

    for _ in range(25):
        base = min(prix_estime, plafond_op)
        montant_ptz = round(base * quotite, 2)
        mensualite_ptz = round(montant_ptz / (annees_p2 * 12), 2)

        mensualite_dispo = max(mensualite_totale_max - mensualite_ptz, 0)
        capital_classique = capital_empruntable(mensualite_dispo, duree_annees)

        financement = dossier.total_apport + montant_ptz + capital_classique
        nouveau_prix = financement / (1 + FRAIS_NEUF)

        if abs(nouveau_prix - prix_estime) < 1:
            prix_estime = nouveau_prix
            break
        prix_estime = nouveau_prix

    mensualite_classique = max(mensualite_totale_max - mensualite_ptz, 0)

    return {
        "type": "avec_ptz",
        "type_bien": type_bien,
        "prix_bien": round(prix_estime, 2),
        "mensualite_max": round(mensualite_totale_max, 2),
        "mensualite_classique": round(mensualite_classique, 2),
        "mensualite_ptz": round(mensualite_ptz, 2),
        "credit_classique": round(capital_classique, 2),
        "ptz": round(montant_ptz, 2),
        "apport": round(dossier.total_apport, 2),
        "frais_estimes": round(prix_estime * FRAIS_NEUF, 2),
        "type_marche": type_marche,
        "tranche": tranche,
        "quotite": quotite,
        "plafond_operation": plafond_op,
        "duree_differe_p1": annees_p1,
        "duree_remboursement_p2": annees_p2,
        "total_duree": annees_p1 + annees_p2,
        "cout_interets": _cout_interets(mensualite_classique, capital_classique, duree_annees),
    }


def simulation_globale(dossier: Dossier, duree_annees: int, zone: str):
    if not dossier.est_valide:
        raise ValueError("Dossier invalide")

    resultats = [calcul_projet_sans_ptz(dossier, duree_annees, type_marche="ancien")]
    for type_bien in ["appartement", "maison"]:
        r = calcul_projet_avec_ptz(dossier, duree_annees, zone, type_bien=type_bien, type_marche="neuf")
        if r:
            resultats.append(r)
    return resultats