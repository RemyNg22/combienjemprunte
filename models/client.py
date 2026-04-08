from models.revenu import Revenu
from models.charge import Charge

class Client:
    """
    Représente un client avec ses revenus et ses charges pour 
    calculer sa capacité d'emprunt
    """

    def __init__(self, nom: str):
        self.nom = nom
        self.revenu: list[Revenu] = []
        self.charge: list[Charge] = []

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
        total_annuel = 0.0
        for r in self.revenu:
            if r.periodicite == "Annuelle":
                total_annuel += r

            elif r.periodicite == "Mensuelle":
                total_annuel += (r*12)

        return round(total_annuel/12, 2)
    

    @property
    def total_charge_mensuel(self):
        """
        Agrège toutes les charges pour les mensualiser
        """
        total_annuel = 0.0
        for r in self.charge:
            total_annuel +=r

        return r/12