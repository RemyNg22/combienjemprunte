class Revenu:

    TYPE_REVENU = {
        # Revenus principaux
        "Salaire CDI": 1.0,
        "Salaire fonctionnaire": 1.0,
        "Retraite": 1.0,
        "Pension d'invalidité": 1.0,
        "Revenu non salarié stable (3 ans)": 1.0,

        # Revenus semi-stables
        "Revenu locatif": 0.7,
        "Prime contractuelle / 13e mois": 0.7,
        "Prime variable": 0.5,

        # CAF
        "Allocations familiales": 0.5,
        "Prime d'activité": 0.0,
        "APL": 0.0,

        # Revenus exclus
        "Allocations chômage": 0.0,
        "RSA": 0.0,
        "Bourse étudiante": 0.0,

        # Divers
        "Autre": 0.0
    }

    PERIODE = ("Mensuelle", "Annuelle")


    def __init__(self, type_de_revenu: str, 
                 montant: float,
                 periodicite: str):
        
        """
        Représente les revenus d'un client.
        """

        if type_de_revenu not in self.TYPE_REVENU:
            raise ValueError("Type de revenu invalide")
        
        if periodicite not in self.PERIODE:
            raise ValueError("La périodicité doit être 'mensuelle' ou 'annuelle'")
        
        if montant <= 0:
            raise ValueError("Le montant doit être positif")
        
        self.type_de_revenu = type_de_revenu
        self.periodicite = periodicite
        self.montant = float(montant)

    @property
    def revenu_pondere(self):
        """
        Pondérer le revenu en fonction du type de revenu.
        """
        return self.montant*self.TYPE_REVENU[self.type_de_revenu]
    
    
    def __repr__(self):
        return (f"Type de revenu : {self.type_de_revenu} - "
                f"Montant : {self.montant}€ - "
                f"Montant pondéré : {self.revenu_pondere}€ - "
                f"Périodicité : {self.periodicite}")
    