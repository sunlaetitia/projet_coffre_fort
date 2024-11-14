import os
import hashlib
import random

#  Section : Gestion des Utilisateurs 
class Utilisateur:
    """
    Classe représentant un utilisateur du coffre-fort numérique.
    Elle contient les informations d'authentification et les clés de chiffrement.
    """
    
    def __init__(self, nom_utilisateur, mot_de_passe):
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.cle_publique, self.cle_privee = generer_cle_RSA()
        self.cle_dérivée = derivee_cle_du_mot_de_passe(mot_de_passe)
    
    def sauvegarder_donnees_utilisateur(self):
        """
        Sauvegarde les informations de l'utilisateur dans un fichier texte.
        À développer : Ajouter des sécurités pour protéger le fichier utilisateur.
        """
        if not os.path.exists("utilisateurs"):
            os.makedirs("utilisateurs")
        with open(f"utilisateurs/{self.nom_utilisateur}.txt", "w") as fichier:
            fichier.write(f"Nom d'utilisateur: {self.nom_utilisateur}\n")
            fichier.write(f"Clé publique: {self.cle_publique.hex()}\n")
            fichier.write(f"Clé privée: {self.cle_privee.hex()}\n")

    def charger_donnees_utilisateur(self):
        """
        Charge les informations utilisateur depuis un fichier texte.
        À développer : Ajouter des mécanismes pour vérifier l'intégrité des données.
        """
        try:
            with open(f"utilisateurs/{self.nom_utilisateur}.txt", "r") as fichier:
                data = fichier.read()
            return data
        except FileNotFoundError:
            return None

#  Section : Fonctions de Chiffrement et Échange de Clés 
def generer_cle_RSA():
    """
    Génère un couple de clés (publique et privée) simplifié pour l'utilisateur.
    À développer : Utiliser un algorithme de génération de clés sécurisé.
    """
    cle_publique = os.urandom(64)
    cle_privee = os.urandom(64)
    return cle_publique, cle_privee

def derivee_cle_du_mot_de_passe(mot_de_passe):
    """
    Dérive une clé à partir d'un mot de passe en utilisant SHA-256.
    À développer : Ajouter des techniques de hachage plus avancées, comme les KDF.
    """
    return hashlib.sha256(mot_de_passe.encode()).digest()

def generer_cle_partagee(cle_privee, cle_publique_autre):
    """
    Génère une clé partagée avec Diffie-Hellman.
    À développer : Utiliser des valeurs de clé et un modulo adapté pour sécuriser l'échange.
    """
    cle_partagee = int.from_bytes(cle_privee, 'big') * int.from_bytes(cle_publique_autre, 'big') % 101
    return cle_partagee.to_bytes((cle_partagee.bit_length() + 7) // 8, 'big')

#  Section : Authentification Zero-Knowledge Proof (Preuve à divulgation nulle) 
def authentification_zkp(cle_publique, cle_privee):
    """
    Implémente une preuve de connaissance sans divulgation de la clé privée (simplifiée).
    À développer : Ajouter des fonctions de vérification et de sécurité selon le protocole Schnorr.
    """
    m = random.randint(1, 10**6)
    M = (int.from_bytes(cle_publique, 'big') * m) % 101
    r = random.randint(1, 10**3)
    preuve = (m - r * int.from_bytes(cle_privee, 'big')) % 101
    return M, preuve, r

def verifier_zkp(cle_publique, M, preuve, r):
    """
    Vérifie la preuve de connaissance pour l'authentification.
    À développer : Vérifier que le calcul de M est exact et sécuriser le protocole.
    """
    M_calcule = (preuve * int.from_bytes(cle_publique, 'big') ** r) % 101
    return M == M_calcule

#  Section : Fonctions Utilitaires de Hashing 
def hacher_message(message):
    """
    Hache un message avec SHA-256 pour le vérifier plus tard.
    À développer : Ajouter la possibilité d'utiliser d'autres algorithmes de hachage.
    """
    return hashlib.sha256(message.encode()).hexdigest()

def verifier_hachage(message, valeur_hachage):
    """
    Vérifie si le hachage d'un message correspond à une valeur donnée.
    """
    return hacher_message(message) == valeur_hachage

#  Section : Script Principal 
def main():
    print("Bienvenue dans le coffre-fort numérique !")

    # Création d'un utilisateur
    nom_utilisateur = input("Entrez le nom d'utilisateur : ")
    mot_de_passe = input("Entrez le mot de passe : ")
    utilisateur = Utilisateur(nom_utilisateur, mot_de_passe)
    utilisateur.sauvegarder_donnees_utilisateur()

    # Authentification Zero-Knowledge Proof
    M, preuve, r = authentification_zkp(utilisateur.cle_publique, utilisateur.cle_privee)
    print("Preuve d'authentification ZKP :")
    if verifier_zkp(utilisateur.cle_publique, M, preuve, r):
        print("Authentification réussie avec ZKP.")
    else:
        print("Échec de l'authentification ZKP.")

    # Échange de clé
    print("\nGénération de clé partagée (Diffie-Hellman) :")
    cle_partagee = generer_cle_partagee(utilisateur.cle_privee, utilisateur.cle_publique)
    print("Clé partagée générée :", cle_partagee.hex())

if __name__ == "__main__":
    main()
