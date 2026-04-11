from models.revenu import Revenu
from models.charge import Charge

class Client:
    """
    Représente un client avec ses revenus et ses charges pour 
    calculer sa capacité d'emprunt, avec son apport et son revenu 
    fiscal de référence pour estimer la capacité d'achat et PTZ
    """

    def __init__(self, nom: str, apport: float):
        self.nom = nom
        self.revenu: list[Revenu] = []
        self.charge: list[Charge] = []
        self.apport = apport

    def ajouter_revenu(self, revenus: Revenu):
        """
        Ajoute un revenu au client
        """
        self.revenu.append(revenus)

    def ajouter_charge(self, charges: Charge):
        """
        Ajoute une charge au client
        """
        self.charge.append(charges)

    
    @property
    def total_revenu_pondere_mensuel(self):
        """
        Agrège tous les revenus annuels et mensuels pour 
        les mensualiser
        """
        total_mensuel = 0.0
        for r in self.revenu:
            if r.periodicite == "Annuelle":
                total_mensuel += (r.revenu_pondere/12)

            elif r.periodicite == "Mensuelle":
                total_mensuel += r.revenu_pondere

        return round(total_mensuel, 2)
    

    @property
    def total_charge_mensuelle(self):
        """
        Agrège toutes les charges pour les mensualiser
        """
        return round(sum(c.montant for c in self.charge), 2)