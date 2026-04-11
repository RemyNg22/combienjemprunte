from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import redis
import uuid
import os
from models.client import Client
from models.revenu import Revenu
from models.charge import Charge
from models.dossier import Dossier
from data.zonage import get_zone_from_commune
from services.cout_total import (calcul_projet_sans_ptz, calcul_projet_avec_ptz)
from dotenv import load_dotenv
load_dotenv()


# App config

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

app.config.update(
    SESSION_TYPE="redis",
    SESSION_PERMANENT=True,
    SESSION_USE_SIGNER=True,
    SESSION_REDIS=redis.from_url(os.getenv("REDIS_URL"))
)

Session(app)


# Init session
@app.before_request
def init_session():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    if "dossier" not in session:
        _reset_dossier()
 
 
def _reset_dossier():
    session["dossier"] = {
        "clients": [],
        "current_client": 0,
        "rfr": None,
        "zone": None,
        "commune": None,
        "nb_personnes": None,
        "ptz_active": False,
        "duree_annees": 25,
    }
 
 
# Accueil
@app.route("/")
def accueil():
    _reset_dossier()
    return render_template("etape_accueil.html")
 
 
# Clients
@app.route("/client", methods=["GET", "POST"])
def client():
    if request.method == "POST":
        noms = request.form.getlist("noms")
        apports_raw = request.form.getlist("apports")
 
        clients = []
        for i, nom in enumerate(noms):
            nom = nom.strip()
            if not nom:
                continue
            try:
                apport = float(apports_raw[i]) if i < len(apports_raw) and apports_raw[i].strip() else 0.0
            except ValueError:
                apport = 0.0
            clients.append({"nom": nom, "revenus": [], "charges": [], "apport": apport})
 
        if not clients:
            return render_template("etape_client.html", error="Au moins un client requis")
 
        session["dossier"]["clients"] = clients
        session["dossier"]["current_client"] = 0
        session.modified = True
        return redirect(url_for("revenus"))
 
    return render_template("etape_client.html")
 
 
# Revenus
TYPES_REVENU_VALIDES = list(Revenu.TYPE_REVENU.keys())
 
@app.route("/revenus", methods=["GET", "POST"])
def revenus():
    d = session["dossier"]
    clients = d["clients"]
 
    if not clients:
        return redirect(url_for("client"))
 
    if request.method == "POST":
        if "finaliser_revenus" in request.form:
            if not any(c["revenus"] for c in clients):
                return render_template(
                    "etape_revenu.html",
                    clients=clients,
                    types_revenu=TYPES_REVENU_VALIDES,
                    error="Veuillez saisir au moins un revenu.",
                )
            return redirect(url_for("charges"))
 
        try:
            client_idx = int(request.form["client_idx"])
            type_rev = request.form["type"]
            if type_rev not in TYPES_REVENU_VALIDES:
                raise ValueError("Type invalide")
            nouveau_revenu = {
                "type": type_rev,
                "montant": float(request.form["montant"]),
                "periodicite": request.form["periodicite"],
            }
            clients[client_idx]["revenus"].append(nouveau_revenu)
            session.modified = True
        except (ValueError, IndexError):
            return render_template(
                "etape_revenu.html",
                clients=clients,
                types_revenu=TYPES_REVENU_VALIDES,
                error="Erreur lors de l'ajout du revenu.",
            )
        return redirect(url_for("revenus"))
 
    return render_template("etape_revenu.html", clients=clients, types_revenu=TYPES_REVENU_VALIDES)
 
 
# Charges
TYPES_CHARGE_VALIDES = list(Charge.CATEGORIE_CHARGE)
 
@app.route("/charges", methods=["GET", "POST"])
def charges():
    d = session.get("dossier")
    if not d or not d.get("clients"):
        return redirect(url_for("client"))
 
    clients = d["clients"]
 
    if request.method == "POST":
        if "finaliser_charges" in request.form:
            return redirect(url_for("ptz"))
 
        t = request.form.get("type")
        m = request.form.get("montant")
        c_idx = request.form.get("client_idx")
 
        if t and m and c_idx is not None:
            if t not in TYPES_CHARGE_VALIDES:
                return render_template(
                    "etape_charge.html",
                    clients=clients,
                    types_charge=TYPES_CHARGE_VALIDES,
                    error="Type de charge invalide.",
                )
            try:
                idx = int(c_idx)
                clients[idx]["charges"].append({"type": t, "montant": float(m)})
                session.modified = True
            except (ValueError, IndexError):
                pass
 
        return redirect(url_for("charges"))
 
    return render_template("etape_charge.html", clients=clients, types_charge=TYPES_CHARGE_VALIDES)
 
 
# PTZ
@app.route("/ptz", methods=["GET", "POST"])
def ptz():
    d = session["dossier"]
    nb_emprunteurs = len(d["clients"])
 
    if request.method == "POST":
        if request.form.get("skip_ptz"):
            d["ptz_active"] = False
            session.modified = True
            return redirect(url_for("resultat"))
 
        try:
            commune = request.form.get("commune", "").strip()
            zone = get_zone_from_commune(commune) or request.form.get("zone", "").strip().upper() or None
 
            if not zone:
                return render_template(
                    "etape_ptz.html",
                    nb_emprunteurs=nb_emprunteurs,
                    error=f"Zone non trouvée pour « {commune} ». Vérifiez l'orthographe ou choisissez la zone manuellement.",
                )
 
            rfr_raw = request.form.get("rfr", "").strip()
            rfr = float(rfr_raw) if rfr_raw else None
 
            if rfr is None:
                d["ptz_active"] = False
                session.modified = True
                return redirect(url_for("resultat"))
 
            nb_personnes_saisi = int(request.form.get("nb_personnes", nb_emprunteurs))
            nb_personnes = max(nb_personnes_saisi, nb_emprunteurs)
 
            d.update({
                "commune": commune,
                "zone": zone,
                "rfr": rfr,
                "nb_personnes": nb_personnes,
                "duree_annees": int(request.form.get("duree_annees", 25)),
                "ptz_active": True,
            })
            session.modified = True
            return redirect(url_for("resultat"))
 
        except ValueError:
            return render_template(
                "etape_ptz.html",
                nb_emprunteurs=nb_emprunteurs,
                error="Erreur de saisie — vérifiez les champs numériques.",
            )
 
    return render_template("etape_ptz.html", nb_emprunteurs=nb_emprunteurs)
 
 
# Reconstruction du dossier depuis la session
def construire_dossier() -> Dossier:
    data = session["dossier"]
    dossier = Dossier()
    dossier.rfr = float(data.get("rfr") or 0)
 
    nb_emprunteurs = len(data["clients"])
    total_foyer = max(int(data.get("nb_personnes") or nb_emprunteurs), nb_emprunteurs)
    dossier.nb_personnes_charge = total_foyer - nb_emprunteurs
 
    for c in data["clients"]:
        client_obj = Client(nom=c["nom"], apport=float(c.get("apport") or 0))
 
        for r in c["revenus"]:
            client_obj.ajouter_revenu(Revenu(r["type"], r["montant"], r["periodicite"]))
 
        for ch in c["charges"]:
            client_obj.ajouter_charge(Charge(type_depense=ch["type"], montant=ch["montant"]))
 
        dossier.ajouter_client(client_obj)
 
    return dossier
 
 
# Résultat
@app.route("/resultat")
def resultat():
    d = session["dossier"]
    dossier = construire_dossier()
    duree = int(d.get("duree_annees") or 25)
 
    resultats = [calcul_projet_sans_ptz(dossier, duree, type_marche="ancien")]
 
    if d.get("ptz_active"):
        for type_bien in ["appartement", "maison"]:
            r = calcul_projet_avec_ptz(
                dossier=dossier,
                duree_annees=duree,
                zone=d["zone"],
                type_bien=type_bien,
                type_marche="neuf",
            )
            if r:
                resultats.append(r)
 
    return render_template("resultat.html", resultats=resultats)
 
 
# À propos
@app.route("/a-propos")
def a_propos():
    return render_template("a_propos.html")
 
 
 
if __name__ == "__main__":
    app.run(debug=True, port=5000)