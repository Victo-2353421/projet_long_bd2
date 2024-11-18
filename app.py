from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="mysql",
    database="projet_long"
)

@app.route('/')
def index():
    """
    Page d'accueil.
    """
    return render_template('index.html')

###########
# Permet de saisir adéquatement les informations du client.
###########
@app.route('/ajout-client')
def ajouterClient():
    """
    Page web affichant le formulaire de création de client.

    Retourne:
        'ajout-client.html'.
    """
    return render_template('ajout-client.html')

@app.route('/ajouter-client', methods=['GET'])
def ajoutClient():
    """
    Traitment du formulaire d'ajout de client.

    Retourne:
        'ajout-client-invalide.html' ou 'ajout-client-valide.html'.
    """
    nom = request.args.get('nom')
    telephone = request.args.get('telephone')
    adresse = request.args.get('adresse')
    # vérif sanitaire serait ici
    if not (nom and telephone and adresse):
        return render_template('ajout-client-invalide.html')
    else:
        try:
            requete = "INSERT INTO clients (nom, telephone, adresse) VALUES (%s, %s, %s)"
            valeurs = (nom, telephone, adresse)
            cursor = db.cursor()
            cursor.execute(requete, valeurs)
            cursor.close()
            db.commit()
        except AssertionError as e:
            return render_template('ajout-client-invalide.html')
    return render_template('ajout-client-valide.html')

###########
# Permet de saisir adéquatement une commande client.
###########
@app.route('/commande')
def commande():
    """
    Page web affichant le formulaire de commande.
    On y insert les données de la pizza et le client.

    Retourne:
        'commande-invalide.html' ou 'commande.html'
    """
    cursor = db.cursor()
    cursor.execute("SELECT id, nom, telephone, adresse FROM clients")
    clients = cursor.fetchall()
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT id, nom FROM croutes")
    croutes = cursor.fetchall()
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT id, nom FROM sauces")
    sauces = cursor.fetchall()
    cursor.close()

    cursor = db.cursor()
    cursor.execute("SELECT id, nom FROM garnitures")
    garnitures = cursor.fetchall()
    cursor.close()

    return render_template('commande.html',
                           clients=clients, croutes=croutes, sauces=sauces,
                           garnitures=garnitures)

###########
# Affiche résumé de la commande.
###########
@app.route('/resumer-commande', methods=['GET'])
def resumerCommande():
    """
    Page web affichant le résumé d'une commande avant de la traiter.
    On y accède à partir de '/commande'.

    Retourne:
        'commande-invalide.html' ou 'resumer-commande.html'
    """
    clientId = request.args.get('client')
    crouteId = request.args.get('croute')
    sauceId = request.args.get('sauce')
    garniture1Id = request.args.get('garniture1')
    garniture2Id = request.args.get('garniture2')
    garniture3Id = request.args.get('garniture3')
    garniture4Id = request.args.get('garniture4')

    cursor = db.cursor()
    requete = "SELECT id, nom, telephone, adresse FROM clients WHERE id = %s"
    cursor.execute(requete, (clientId,))
    client = cursor.fetchall()
    if len(client):
        client = client[0]
    else:
        return render_template('commande-invalide.html', message="Client invalide")
    cursor.close()

    cursor = db.cursor()
    requete = "SELECT id, nom FROM croutes WHERE id = %s"
    cursor.execute(requete, (crouteId,))
    croute = cursor.fetchall()
    if len(croute):
        croute = croute[0]
    else:
        return render_template('commande-invalide.html', message="Croute invalide")
    cursor.close()

    cursor = db.cursor()
    requete = "SELECT id, nom FROM sauces WHERE id = %s"
    cursor.execute(requete, (sauceId,))
    sauce = cursor.fetchall()
    if len(sauce):
        sauce = sauce[0]
    else:
        return render_template('commande-invalide.html', message="Sauce invalide")
    cursor.close()

    cursor = db.cursor()
    requete = "SELECT id, nom FROM garnitures WHERE id = %s"
    cursor.execute(requete, (garniture1Id,))
    garniture1 = cursor.fetchall()
    if len(garniture1):
        garniture1 = garniture1[0]
    else:
        garniture1 = None
    cursor.close()
    cursor = db.cursor()
    requete = "SELECT id, nom FROM garnitures WHERE id = %s"
    cursor.execute(requete, (garniture2Id,))
    garniture2 = cursor.fetchall()
    if len(garniture2):
        garniture2 = garniture2[0]
    else:
        garniture2 = None
    cursor.close()
    cursor = db.cursor()
    requete = "SELECT id, nom FROM garnitures WHERE id = %s"
    cursor.execute(requete, (garniture3Id,))
    garniture3 = cursor.fetchall()
    if len(garniture3):
        garniture3 = garniture3[0]
    else:
        garniture3 = None
    cursor.close()
    cursor = db.cursor()
    requete = "SELECT id, nom FROM garnitures WHERE id = %s"
    cursor.execute(requete, (garniture4Id,))
    garniture4 = cursor.fetchall()
    if len(garniture4):
        garniture4 = garniture4[0]
    else:
        garniture4 = None
    cursor.close()
    

    return render_template('resumer-commande.html',
                           client=client, croute=croute, sauce=sauce,
                           garniture1=garniture1,
                           garniture2=garniture2,
                           garniture3=garniture3,
                           garniture4=garniture4)


@app.route('/commander', methods=['GET'])
def commander():
    """
    Traitment du formulaire de commande.

    Retourne:
        'commande-invalide.html' ou 'commande-valide.html'.
    """
    client = request.args.get('client')
    croute = request.args.get('croute')
    sauce = request.args.get('sauce')
    garnitures = [
        request.args.get('garniture1'),
        request.args.get('garniture2'),
        request.args.get('garniture3'),
        request.args.get('garniture4')
    ]
    garnitures = garnitures[:4]
    if client and croute and sauce:
        try:
            print("1")
            #pizza & croute
            requete = "INSERT INTO pizzas (id_croute) VALUES (%s)"
            cursor = db.cursor()
            cursor.execute(requete, (croute,))
            pizza = cursor.lastrowid
            cursor.close()
            if pizza is None:
                raise LookupError('id pizza créé introuvable')

            #sauce
            requete = "INSERT INTO sauces_pizzas (id_sauce, id_pizza) VALUES (%s, %s)"
            valeurs = (sauce, pizza,)
            cursor = db.cursor()
            cursor.execute(requete, valeurs)
            cursor.close()
            #garnitures
            for garniture in garnitures:
                if garniture:
                    requete = "INSERT INTO garnitures_pizzas (id_garniture, id_pizza) VALUES (%s, %s)"
                    valeurs = (garniture, pizza,)
                    cursor = db.cursor()
                    cursor.execute(requete, valeurs)
                    cursor.close()

            #sauce
            requete = "INSERT INTO commandes (id_pizza, id_client) VALUES (%s, %s)"
            valeurs = (pizza, client,)
            cursor = db.cursor()
            cursor.execute(requete, valeurs)
            cursor.close()

            db.commit()

        except Exception as e:
            print("Erreur:", e)
            return render_template('commande-invalide.html', message="erreur interne")
    else:
        return render_template('commande-invalide.html', message="requête invalide")

    return render_template('commande-valide.html')

###########
# Affiche adéquatement la liste des commandes en attente de livraison
# et
# permet de compléter adéquatement une livraison.
###########
@app.route('/liste-attente-commandes')
def listeCommande():
    """
    Affichage de la liste d'attente de commandes.

    Retourne:
        'liste-attente-commandes.html'.
    """
    cursor = db.cursor()
    cursor.execute("""
        SELECT attente_commandes.id, clients.nom, clients.adresse FROM attente_commandes
            INNER JOIN commandes ON commandes.id = attente_commandes.id_commande
            INNER JOIN clients ON clients.id = commandes.id_client
    """)
    commandes = cursor.fetchall()
    cursor.close()
    return render_template('liste-attente-commandes.html', commandes=commandes)

@app.route('/completer-commande/<int:id>')
def completerCommande(id):
    """
    Traitement de la complétion du commande de la liste d'attente.
    On y accède à partir de '/liste-attente-commandes'

    Retourne:
        'completion-commande-reussie.html' ou 'completion-commande-echouee.html'.
    """
    requete = """
        SELECT clients.nom, clients.adresse FROM attente_commandes
            INNER JOIN commandes ON commandes.id = attente_commandes.id_commande
            INNER JOIN clients ON clients.id = commandes.id_client
            WHERE attente_commandes.id = %s
            LIMIT 1
    """
    cursor = db.cursor()
    cursor.execute(requete, (id,))
    info = cursor.fetchall()
    cursor.close()
    if len(info):
        requete = "DELETE FROM attente_commandes WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(requete, (id,))
        cursor.close()
        db.commit()
        return render_template('completion-commande-reussie.html', info=info[0])
    else:
        return render_template('completion-commande-echouee.html')

if __name__ == '__main__':
    app.run(debug=True)