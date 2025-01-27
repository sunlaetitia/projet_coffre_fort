import os
import time
from contexte import chemin_coffre_fort, chemin_Utilisateurs, chemin_doc_crypté, chemin_bd_json, chemin_ca, chemin_cles_coffre_json, chemin_cles_ca_json, chemin_cert_coffre_fort
from contexte import contexte
import authentification
import utilitaire
import dérivation
import gestion_fichier
import certificat
import json
import re
from datetime import datetime
from utilitaire import generer_cle_RSA, renouveler_cle_RSA
from journalisation import journaliser_action

#Fonction pour initialiser les répertoires au démarrage du programme
def initialiser_repertoires():
    os.makedirs(chemin_coffre_fort, exist_ok=True)
    os.makedirs(chemin_ca, exist_ok=True)
    os.makedirs(chemin_Utilisateurs, exist_ok=True)
    os.makedirs(chemin_doc_crypté, exist_ok=True)

    # Génération des clés RSA pour le coffre-fort si elles n'existent pas
    chemin_cle_coffre = os.path.join(chemin_coffre_fort, "cles_coffre.json")
    if not os.path.exists(chemin_cle_coffre):
        cle_privee, cle_publique, expiration, p = generer_cle_RSA()
        sauvegarder_cles(chemin_cle_coffre, cle_privee, cle_publique, expiration)
        print("Clés RSA pour le coffre-fort générées et sauvegardées.")
    else:
        verifier_cle_perimee(chemin_cle_coffre)
    # Génération des clés RSA pour l'autorité de certification si elles n'existent pas
    chemin_CA = os.path.join(chemin_ca, "CA.json")
    if not os.path.exists(chemin_CA):
        cle_privee, cle_publique, expiration, p = generer_cle_RSA()
        sauvegarder_cles(chemin_CA, cle_privee, cle_publique, expiration)
        print("Clés RSA pour la CA générées et sauvegardées.")
    print("Arborescence des répertoires initialisée.")


# sauvegarde dans un fichier json des clés publics et privées
def sauvegarder_cles(chemin, cle_privee, cle_publique, expiration):
    with open(chemin, "w") as fichier:
        json.dump({
            "cle_privee":  list(cle_privee),
            "cle_publique": list(cle_publique),
            "expiration": expiration.isoformat()
        }, fichier)
        
def verifier_cle_perimee(chemin):
    with open(chemin, "r") as fichier:
        cles = json.load(fichier)
        expiration = datetime.fromisoformat(cles["expiration"])
        if expiration < datetime.utcnow():
            print("Les clés RSA du coffre-fort sont expirées. Renouvellement en cours...")
            cle_privee, cle_publique, nouvelle_expiration = renouveler_cle_RSA()
            sauvegarder_cles(chemin, cle_privee, cle_publique, nouvelle_expiration)
            #enregistrer_renouvellement_utilisateur(nom_utilisateur)
            print("Clés RSA du coffre-fort renouvelées avec succès.")
        else:
            print("Les clés RSA du coffre-fort sont encore valides.")

def utilisateur_existe(nom_utilisateur):
    if os.path.exists(chemin_bd_json):
        with open(chemin_bd_json, 'r') as f:
            utilisateurs = json.load(f)
            return nom_utilisateur in utilisateurs
    return False

def creer_arborescence_utilisateur(utilisateur):
    chemin_utilisateur = os.path.join(chemin_Utilisateurs, utilisateur)
    os.makedirs(chemin_utilisateur, exist_ok=True)
    os.makedirs(os.path.join(chemin_utilisateur, "fichiers_cryptes"), exist_ok=True)
    return chemin_utilisateur

def demander_nom_utilisateur():
    noms_interdits = ["admin", "root", "test"]
    
    while True:
        nom_utilisateur = input("Entrez un nom d'utilisateur (lettres suivies éventuellement de chiffres, pas de caractères spéciaux) : ").strip()
        
        # Vérification avec l'expression régulière
        if not re.fullmatch(r"[a-zA-Z]+[0-9]*", nom_utilisateur):
            print("Nom d'utilisateur invalide. Il doit commencer par des lettres et ne peut contenir que des chiffres après celles-ci.")
            continue

        # Vérification : longueur
        if len(nom_utilisateur) < 3 or len(nom_utilisateur) > 20:
            print("Le nom d'utilisateur doit contenir entre 3 et 20 caractères.")
            continue

        # Vérification : noms interdits
        if nom_utilisateur.lower() in noms_interdits:
            print(f"Le nom d'utilisateur '{nom_utilisateur}' est réservé. Veuillez en choisir un autre.")
            continue
        
        # Si toutes les vérifications sont passées
        return nom_utilisateur

def menu_principal():
    print("Bienvenue dans le coffre-fort numérique!") 
    nbre_tentatives = 0     #Initialise le nombre de tentatives du client
    cles_coffre = utilitaire.charger_cle(chemin_cles_coffre_json)
    cle_ca = utilitaire.charger_cle(chemin_cles_ca_json)
    cle_priv_ca = cle_ca["cle_privee"] 
    cle_publique_coffre = cles_coffre["cle_publique"]
    signature, _ = certificat.generer_certificat(cle_publique_coffre, cle_priv_ca, "coffre_fort", chemin_cert_coffre_fort)
    while True:
        print("1. Inscription")
        print("2. Connexion")
        print("3. Quitter")
        choix = input("Votre choix: ")

        if choix == "1":
            contexte.nom_utilisateur = demander_nom_utilisateur()
            while utilisateur_existe(contexte.nom_utilisateur):
                contexte.nom_utilisateur = input("Le nom que vous avez choisi existe déjà. Veuillez saisir un autre nom ou connectez-vous au compte existant: ")
            mot_de_passe = input("Entrez un mot de passe: ")
            while not utilitaire.verifier_mot_de_passe(mot_de_passe):
                mot_de_passe = input("Le mot de passe n'est pas robuste. Veuillez recommencer: ")
            sel = utilitaire.generer_sel()
            contexte.cle_derivee = dérivation.derivee_cle(mot_de_passe, sel, iterations = 1000, longueur_cle = 16)
            hash_mdp = dérivation.sha256(mot_de_passe.encode("utf-8"))
            cle_privee, cle_publique, expiration, p = generer_cle_RSA()
            chemin_utilisateur = creer_arborescence_utilisateur(contexte.nom_utilisateur)
            utilitaire.ajouter_utilisateur(contexte.nom_utilisateur, hash_mdp, sel, contexte.cle_derivee, cle_privee, cle_publique, expiration, p)
            certificat.generer_certificat(cle_publique, cle_privee, contexte.nom_utilisateur, f"{chemin_utilisateur}\\certificat.cert" )
            journaliser_action("Inscription", contexte.nom_utilisateur, "Nouvel utilisateur inscrit", "vous vous etes inscrit.")
            print("Inscription réussie!")
            
        elif choix == "2":
            if os.path.exists(chemin_cert_coffre_fort):
                with open(chemin_cert_coffre_fort, "r") as fichier:
                    certificat_contenu = fichier.read()
                cle_pub_ca = cle_ca["cle_publique"]
                if not certificat.verifier_certificat(certificat_contenu, cle_pub_ca):
                    print("Échec de la vérification du certificat.")
                else:
                    print("Certificat vérifié avec succès.")
                    contexte.nom_utilisateur = input("Nom d'utilisateur: ")
                    contexte.hash_mdp = input("Mots de passe: ")
                    if authentification.authentification_double_sens(contexte.nom_utilisateur, contexte.hash_mdp, signature) is None:
                        journaliser_action("Connexion", contexte.nom_utilisateur, "un nouvel utilisateur connecte", "vous vous êtes connecte.")
                        gestion_fichier.menu_general(contexte.nom_utilisateur)
                    else:
                        print("Échec de la connexion.")
                        nbre_tentatives += 1
                        if nbre_tentatives == 3:
                            print("###############Trop de tentatives, veuillez attendre un instant!################")
                            time.sleep(10)
                            nbre_tentatives = 0
            else:
                print("##############  Coffre fort non valide  ##############")
        elif choix == "3":
            print("À bientôt!")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    initialiser_repertoires()  
    menu_principal() 

