import os
from datetime import datetime
import utilitaire
from contexte import chemin_historique, chemin_Utilisateurs
"""
def configurer_journal_utilisateur(nom_utilisateur):
    chemin_journal_utilisateur = os.path.join(chemin_Utilisateurs, nom_utilisateur, "journal.log")
    #os.makedirs(chemin_historique, exist_ok=True)
    #os.makedirs(chemin_journal_utilisateur, exist_ok=True)
    return chemin_journal_utilisateur
"""
def ecrire_journal_global(message):
    fichier_global = os.path.join(chemin_historique, "journal_global.log")
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