class Charge:

    CATEGORIE_CHARGE = (
        "Loyer persistant",
        "Crédit Immoblier persistant",
        "Crédit Auto",
        "Crédit Consommation",
        "Pension alimentaire",
        "Autre charge"
    )

    def __init__(self,
                 type_depense: str,
                 montant: float):
        
        """
        Représente les charges d'un client.
        """

        if type_depense not in self.CATEGORIE_CHARGE:
            raise ValueError("Type de charge invalide")
        
        if montant <= 0 :
            raise ValueError("Le montant doit être positif")
        
        self.type_depense = type_depense
        self.montant = float(montant)

    def __repr__(self):
        return f"Charge : {self.type_depense} - {self.montant}€/mois"