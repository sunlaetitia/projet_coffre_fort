# contexte.py
import os
import json
from datetime import datetime


class variable:
    def __init__(self):
        self.nom_utilisateur = None
        self.hash_mdp = None
        self.cle_publique_coffre = None
        self.cle_privee_coffre = None

        # Chargement des clés RSA du coffre-fort
        chemin_cle_coffre = os.path.join("coffre_fort", "cles_coffre.json")
        if os.path.exists(chemin_cle_coffre):
            with open(chemin_cle_coffre, "r") as fichier:
                cles = json.load(fichier)
                self.cle_publique_coffre = tuple(cles["cle_publique"])
                self.cle_privee_coffre = tuple(cles["cle_privee"])
                self.expiration_coffre = datetime.fromisoformat(cles["expiration"])
                
        self.cle_publique = None
        self.cle_privee = None
        self.cle_derivee = None # simplifié pour désigner l'utilisateur simple  

chemin_coffre_fort = "coffre_fort"
chemin_ca = "CA"
chemin_Utilisateurs ="coffre_fort\\Utilisateurs"
chemin_doc_crypté = "coffre_fort\\doc_crypté"
chemin_historique = "coffre_fort\\historique"
chemin_bd_json =  "coffre_fort\\base_de_donnee.json"
chemin_cles_coffre_json =  "coffre_fort\\cles_coffre.json"
chemin_cles_ca_json =  "CA\\CA.json"
chemin_cert_coffre_fort = "coffre_fort\\certificat.cert"

contexte = variable()