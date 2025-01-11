#authentification.py
import time
import certificat
import json
from datetime import datetime, timedelta
import ZKP
from contexte import contexte, chemin_Utilisateurs, chemin_cles_coffre_json, chemin_bd_json
import utilitaire
import dérivation
import key_exchange
from journalisation import journaliser_action



def authentification_double_sens(utilisateur, mdp):
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
    print("Phase d'authentification à double sens commencée.")
    cle_publique_utilisateur = base_de_donnee[utilisateur]["cle_publique"]
    p = base_de_donnee[utilisateur]["p"]
    cle_privee_coffre = cles_coffre["cle_privee"]
    cle_publique_coffre = cles_coffre["cle_publique"]

    base_de_donnee = utilitaire.charger_base_de_donnee()
    cle_publique_utilisateur= base_de_donnee[utilisateur]["cle_publique"][0]
    userdoc = f"coffre_fort\\Utilisateurs\\{utilisateur}\\cles.pem"
    with open(userdoc, "r") as fichier:
        cle_privee_utisateur = fichier.read()
    cle_privee_utisateur = cle_privee_utisateur.strip("[] \n")
    cle_privee_utisateur = [int(x.strip()) for x in cle_privee_utisateur.split(",")]
    cle_privee_utisateur = cle_privee_utisateur[0]
    cles_session = key_exchange.diffie_hellmann(cle_privee_coffre, cle_publique_coffre, cle_privee_utisateur, cle_publique_utilisateur)
    with open(chemin_bd_json, "r") as bd:
        donnee = json.load(bd)
    donnee[utilisateur]["session"] = cles_session
    with open(chemin_bd_json, "w") as fichier:
        json.dump(donnee, fichier, indent=4)
    # # Génération et enregistrement du certificat
    # certificat_utilisateur, certificat_signature = certificat.generer_certificat(chemin_Utilisateurs, cle_publique_utilisateur, cle_privee_coffre, contexte.nom_utilisateur)
    # certificat.enregistrer_certificat_utilisateur(utilisateur, certificat_utilisateur)

    # chemin_certificat = certificat.generer_chemin_certificat(utilisateur)
    # with open(chemin_certificat, "r") as fichier:
    #     certificat_contenu = fichier.read()

    # if not certificat.verifier_certificat(certificat_contenu, cle_publique_coffre):
    #     print("Échec de la vérification du certificat.")
    #     return False

    # print("Certificat vérifié avec succès.")
    # verification_ca = certificat.demander_verification_ca(
    #     certificat_contenu, cle_publique_coffre
    # )
    # if verification_ca != cle_publique_utilisateur[0]:
    #     print("Échec de la vérification du certificat par la CA.")
    #     return False

    # print("Certificat vérifié par la CA avec succès.")

    # if  ZKP.protocole_guillou_quisquater(utilisateur, cle_publique_utilisateur, certificat_signature, p):
    #     print("Authentification réussie.")
    #     """
    #     utilisateur_data["tentatives"] = 0
    #     utilitaire.sauvegarder_base_de_donnee(base_de_donnee)
    #     enregistrer_action("Connexion", utilisateur)
    #     journaliser_action("Connexion reussie", utilisateur, "Authentification reussie", "Authentification reussie")
    #     return True
    #     """
    # else:
    #     print("Tentative d'authentification échouée.")
    #     """utilisateur_data["tentatives"] = utilisateur_data.get("tentatives", 0) + 1
    #     if utilisateur_data["tentatives"] >= MAX_TENTATIVES:
    #         utilisateur_data["bloque_jusqu_a"] = (datetime.utcnow() + DUREE_BLOCAGE).isoformat()
    #         print("Trop de tentatives infructueuses. Utilisateur bloqué temporairement.")
    #     """
    #     """
    #     utilitaire.sauvegarder_base_de_donnee(base_de_donnee)
    #     journaliser_action("Connexion échouee", utilisateur, "Erreur d'authentification", "Erreur d'authentification")
    #     return False
    #     """
