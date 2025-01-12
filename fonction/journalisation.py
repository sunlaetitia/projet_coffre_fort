import os
from datetime import datetime
import utilitaire
from contexte import chemin_coffre_fort, chemin_Utilisateurs


def ecrire_journal_global(message):
    fichier_global = os.path.join(chemin_coffre_fort, "journal_global.log")
    with open(fichier_global, "a") as fichier:
        fichier.write(f"{datetime.utcnow()} - {message}\n")

def ecrire_journal_utilisateur(nom_utilisateur, message):
    base_de_donnee = utilitaire.charger_base_de_donnee()
    if nom_utilisateur in base_de_donnee:
        fichier_utilisateur = os.path.join(chemin_Utilisateurs, nom_utilisateur, "journal.log")
        with open(fichier_utilisateur, "a") as fichier:
            fichier.write(f"{datetime.utcnow()} - {message}\n")


def journaliser_action(action, nom_utilisateur=None, details_global="", details_utilisateur=""):
    message_global = f"Action: {action} | Utilisateur: {nom_utilisateur or 'Global'} | Details: {details_global}"
    message_utilisateur = f"Action: {action} | Utilisateur: {nom_utilisateur or 'Global'} | Details: {details_utilisateur}"
    ecrire_journal_global(message_global)
    if nom_utilisateur:
        ecrire_journal_utilisateur(nom_utilisateur, message_utilisateur)
