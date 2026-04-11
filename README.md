# Combienjemprunte : Simulateur de capacité d'emprunt

Combienjemprunte.com est un simulateur personnel de capacité d'emprunt pour découvrir quel bien immobilier vous pouvez acheter, avec ou sans Prêt à Taux Zéro (PTZ), à l'aide de vos revenus, des charges et taux de crédits actuels.
Le logiciel est développé en **Python** avec une interface web **HTML/Flask**

**Le lien du site web Combienjemprunte.com**

[https://combienjemprunte.com/](https://combienjemprunte.com)


---

## Objectif

- Déterminer la capacité d'emprunt de 7 à 25 ans d'une personne ou d'un foyer à l'aide de ses revenus, de ses charges et du type de projet immobilier (neuf/ancien). 

- Déterminer le montant de l'acquisition qu'il est possible d'acheter avec l'apport disponible.

- Déterminer le montant du PTZ et de l'acquisition avec PTZ

---

## Architecture du projet

```text
combienjemprunte/

├── app.py                  #point d'entrée, routes flask
├── README.md               # Description projet
├── requirements.txt        # à installer
├── .gitignore              # à masquer
|
├── models/
│   ├── dossier.py          # Agrège les différents clients
│   ├── client.py           # POO objet Client
│   ├── charge.py           # POO objet charge
│   └── revenu.py           # POO objet revenu
|
├── services/
│   ├── regles.py           # Définit toutes les règles pour les calculs
│   ├── capacite_emprunt.py # Calcul la mensualité max et capacité d'emprunt avec taux classique
│   ├── pret_taux_zero.py   # Calcul le montant du PTZ et voit si éligible ou pas
│   └── cout_total.py       # Calcul le montant d'acquisition possible avec frais de notaire et annexes (PTZ inclu ou pas)
|
├── data/
│   ├── liste_communes_zonage_sept_2025.xlsx    # Permet de trouver le zonage de sa commune
│   └── zonage.py                               # Extrait les zones du xlsx
|
|
├── templates/
│   ├── base.html
│   ├── etape_accueil.html
│   ├── etape_client.html
│   ├── etape_revenu.html
│   ├── etape_charge.html
│   ├── etape_ptz.html
│   ├── resultat.html
│   └── a_propos.html
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