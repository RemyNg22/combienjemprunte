# Combienjemprunte : Simulateur de capacité d'emprunt

Combienjemprunte.com est un simulateur personnel de capacité d'emprunt pour découvrir quel bien immobilier vous pouvez acheter, à l'aide de vos revenus, des charges et taux de crédits actuels.
Le logiciel est développé en **Python** avec une interface web **HTML/Flask**

**Le lien du site web Combienjemprunte.com**

Lien vers le notebook :

---

## Objectif

- Déterminer la capacité d'emprunt de 10 à 25 ans d'une personne ou d'un foyer à l'aide de ses revenus, de ses charges et du type de projet immobilier (neuf/ancien). 

- Déterminer le montant de l'acquisition qu'il est possible d'acheter avec l'apport disponible.

---

## Architecture du projet

```text
combienjemprunte/

├── app.py                  #point d'entrée, routes flask
├── session_store.py        # Stockage en mémoire serveur (temporaire)
├── README.md               # Description projet
├── requirements.txt        # à installer
├── .gitignore              # à masquer
|
├── models/
│   ├── client.py           # POO objet Client
│   ├── charge.py           # POO objet charge
│   └── revenu.py           # POO objet revenu
|
├── services/
│   ├── regles.py           # Définit toutes les règles pour les calculs
│   ├── capacite_emprunt.py # Calcul la mensualité max et capacité d'emprunt avec taux classique
│   └── pret_taux_zero.py
|
├── data/
│   ├── liste_communes_zonage_sept_2025.xlsx    # Permet de trouver le zonage de sa commune
│   └── zonage.py                               # Extrait les zones du xlsx
|
```

## Lancement du projet

**1. Installation**

```
pip install -r requirements.txt
```

**2. Lancement de l'application**

```
python app.py
```

## Logique métier

L’application repose sur une séparation claire :

- models/ : structure des données
- services/ : calculs financiers et règles métier
- templates/ : rendu utilisateur