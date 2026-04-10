from models.client import Client


class Dossier:
    """
    Représente un foyer (1 ou plusieurs clients)
    """

    def __init__(self):
        self.clients: list[Client] = []
        self.nb_personnes_charge = 0

    def ajouter_client(self, client: Client):
        if not isinstance(client, Client):
            raise TypeError("Doit être un Client")

        self.clients.append(client)

    @property
    def est_valide(self):
        return len(self.clients) > 0

    @property
    def total_revenus(self):
        return sum(c.total_revenu_pondere_mensuel for c in self.clients)


    @property
    def total_charges(self):
        return sum(c.total_charge_mensuelle for c in self.clients)

    @property
    def total_apport(self):
        return sum(c.apport for c in self.clients)

    @property
    def total_rfr(self):
        return sum(c.revenu_fiscal_reference for c in self.clients)

    @property
    def nb_personnes(self):
        return len(self.clients) + self.nb_personnes_charge