#authentification.py
import json
from datetime import datetime
import ZKP
from contexte import chemin_cles_coffre_json, chemin_bd_json
import utilitaire
import dérivation
import key_exchange
from journalisation import journaliser_action


# Processus d'authentification à deux facteurs
def authentification_double_sens(utilisateur, mdp, signature):
    base_de_donnee = utilitaire.charger_base_de_donnee()
    cles_coffre = utilitaire.charger_cle(chemin_cles_coffre_json)
    hash_mdp = dérivation.sha256(mdp.encode("utf-8"))
    if utilisateur not in base_de_donnee:
        print("Utilisateur inconnu.")
        journaliser_action("Connexion echouee", utilisateur, "Utilisateur inconnu", "Utilisateur inconnu")
        return False
    elif hash_mdp != base_de_donnee[utilisateur]["hash_mdp"]:
        print("Mots de passe incorrect!")
        journaliser_action("Connexion echouee", utilisateur, "Mots de passe incorrect", "Mots de passe incorrect")
        return False
    
    donnee_utilisateur = base_de_donnee[utilisateur]

    expiration = datetime.fromisoformat(donnee_utilisateur.get("expiration", ""))
    if expiration < datetime.utcnow():
        print(f"Les clés de l'utilisateur {utilisateur} sont expirées. Veuillez les renouveler.")
        return False
    userdoc = f"coffre_fort\\Utilisateurs\\{utilisateur}\\cles.pem"
    #Première phase d'authentification 
    print("Phase d'authentification à double sens commencée.")
    cle_publique_utilisateur = base_de_donnee[utilisateur]["cle_publique"]
    p = base_de_donnee[utilisateur]["p"]
    cle_privee_coffre = cles_coffre["cle_privee"]
    cle_publique_coffre = cles_coffre["cle_publique"]

    base_de_donnee = utilitaire.charger_base_de_donnee()
    cle_publique_utilisateur= base_de_donnee[utilisateur]["cle_publique"][0]
    userdoc = f"coffre_fort\\Utilisateurs\\{utilisateur}\\cles.pem"
    with open(userdoc, "r") as fichier:
        cle_privee_utilisateur = fichier.read()
    cle_privee_utilisateur = cle_privee_utilisateur.strip("[] \n")
    cle_privee_utilisateur = [int(x.strip()) for x in cle_privee_utilisateur.split(",")]
    cle_privee_utilisateur = cle_privee_utilisateur[0]
    cles_session = key_exchange.diffie_hellmann(cle_privee_coffre, cle_publique_coffre, cle_privee_utilisateur, cle_publique_utilisateur)
    with open(chemin_bd_json, "r") as bd:
        donnee = json.load(bd)
    donnee[utilisateur]["session"] = cles_session
    with open(chemin_bd_json, "w") as fichier:
        json.dump(donnee, fichier, indent=4)
    
    cle_publique_utilisateur= base_de_donnee[utilisateur]["cle_publique"]

    # Deuxième phases protocole de guillou_quisquater
    if  ZKP.protocole_guillou_quisquater(cle_publique_utilisateur, cle_privee_utilisateur, signature, p):
        print("Authentification réussie.")
    else:
        print("Tentative d'authentification échouée.")
