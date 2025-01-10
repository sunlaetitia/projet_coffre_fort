#authentification.py
import certificat
import json
from datetime import datetime, timedelta
import ZKP
from contexte import contexte, chemin_Utilisateurs
import utilitaire
import dérivation
from journalisation import journaliser_action

MAX_TENTATIVES = 5
DUREE_BLOCAGE = timedelta(minutes=2)

def authentification_double_sens(utilisateur, mdp):
    base_de_donnee = utilitaire.charger_base_de_donnee()
    cles_coffre = utilitaire.charger_cles_coffre()
    if utilisateur not in base_de_donnee:
        print("Utilisateur inconnu.")
        journaliser_action("Connexion echouee", utilisateur, "Utilisateur inconnu", "Utilisateur inconnu")
        return False
    elif mdp != base_de_donnee[utilisateur]["hash_mdp"]:
        print("Mots de passe incorrect!")
        journaliser_action("Connexion echouee", utilisateur, "Mots de passe incorrect", "Mots de passe incorrect")
        return False
    
    donnee_utilisateur = base_de_donnee[utilisateur]
        # Vérifier si l'utilisateur est bloqué
    if "bloque_jusqu_a" in donnee_utilisateur and donnee_utilisateur["bloque_jusqu_a"]:
        bloque_jusqu_a = datetime.fromisoformat(donnee_utilisateur["bloque_jusqu_a"])
        if datetime.utcnow() < bloque_jusqu_a:
            print(f"L'utilisateur est temporairement bloqué jusqu'à {bloque_jusqu_a}.")
            journaliser_action("Connexion echouee", utilisateur, "Utilisateur bloque", "vous etes bloque")
            return False
        else:
            # Réinitialiser le statut de blocage
            donnee_utilisateur["bloque_jusqu_a"] = None
            donnee_utilisateur["tentatives"] = 0

    expiration = datetime.fromisoformat(donnee_utilisateur.get("expiration", ""))
    if expiration < datetime.utcnow():
        print(f"Les clés de l'utilisateur {utilisateur} sont expirées. Veuillez les renouveler.")
        return False
    userdoc = f"coffre_fort\\Utilisateurs\\{utilisateur}\\cles.pem"
    with open(userdoc, "r") as fichier:
        cle_privee_utilisateur = fichier.read()
    print("Phase d'authentification à double sens commencée.")
    cle_publique_utilisateur = base_de_donnee[utilisateur]["cle_publique"]
    p = base_de_donnee[utilisateur]["p"]
    cle_privee_coffre = cles_coffre["cle_privee"]
    cle_publique_coffre = cles_coffre["cle_publique"]



    # Génération et enregistrement du certificat
    certificat_utilisateur, certificat_signature = certificat.generer_certificat(chemin_Utilisateurs, cle_publique_utilisateur, cle_privee_coffre, contexte.nom_utilisateur)
    certificat.enregistrer_certificat_utilisateur(utilisateur, certificat_utilisateur)

    chemin_certificat = certificat.generer_chemin_certificat(utilisateur)
    with open(chemin_certificat, "r") as fichier:
        certificat_contenu = fichier.read()

    if not certificat.verifier_certificat(certificat_contenu, cle_publique_coffre):
        print("Échec de la vérification du certificat.")
        return False

    print("Certificat vérifié avec succès.")
    verification_ca = certificat.demander_verification_ca(
        certificat_contenu, cle_publique_coffre
    )
    if verification_ca != cle_publique_utilisateur[0]:
        print("Échec de la vérification du certificat par la CA.")
        return False

    print("Certificat vérifié par la CA avec succès.")

    if  ZKP.protocole_guillou_quisquater(utilisateur, cle_publique_utilisateur, certificat_signature, p):
        print("Authentification réussie.")
        """
        utilisateur_data["tentatives"] = 0
        utilitaire.sauvegarder_base_de_donnee(base_de_donnee)
        enregistrer_action("Connexion", utilisateur)
        journaliser_action("Connexion reussie", utilisateur, "Authentification reussie", "Authentification reussie")
        return True
        """
    else:
        print("Tentative d'authentification échouée.")
        """utilisateur_data["tentatives"] = utilisateur_data.get("tentatives", 0) + 1
        if utilisateur_data["tentatives"] >= MAX_TENTATIVES:
            utilisateur_data["bloque_jusqu_a"] = (datetime.utcnow() + DUREE_BLOCAGE).isoformat()
            print("Trop de tentatives infructueuses. Utilisateur bloqué temporairement.")
        """
        """
        utilitaire.sauvegarder_base_de_donnee(base_de_donnee)
        journaliser_action("Connexion échouee", utilisateur, "Erreur d'authentification", "Erreur d'authentification")
        return False
        """
