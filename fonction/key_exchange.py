import random
from  utilitaire import miller_rabin


def generer_premier(bits, k=10):
    """
    Génère un nombre premier de la taille spécifiée en bits.
    k : nombre d'itérations pour le test de Miller-Rabin.
    """
    while True:
        # Générer un candidat aléatoire de la taille spécifiée
        candidat = random.getrandbits(bits)
        candidat |= (1 << bits - 1) | 1  # S'assurer qu'il est impair et a le bon nombre de bits
        if miller_rabin(candidat, k):
            return candidat


def trouver_generateur(prime):
    """
    Trouve un générateur valide pour un nombre premier donné.
    """
    for g in range(2, prime):
        if pow(g, 2, prime) != 1 and pow(g, prime - 1, prime) == 1:
            return g
    raise ValueError("Aucun générateur valide trouvé.")


def diffie_hellmann(cle_privee_coffre, cle_publique_coffre, cle_privee_utilisateur, cle_publique_utilisateur):
    # Étape 1 : Génération des paramètres Diffie-Hellman
    prime = generer_premier(256)  # Générer un nombre premier de 2048 bits
    generator = trouver_generateur(prime)  # Trouver un générateur valide (g)

    # Étape 2 : Génération des clés privées et publiques
    cle_privee_coffre = random.randint(1, prime - 1)  # Clé privée du coffre
    cle_publique_coffre = pow(generator, cle_privee_coffre, prime)  # Clé publique du coffre

    cle_privee_utilisateur = random.randint(1, prime - 1)  # Clé privée de l'utilisateur
    cle_publique_utilisateur = pow(generator, cle_privee_utilisateur, prime)  # Clé publique de l'utilisateur

    # Étape 3 : Calcul des clés partagées
    cle_de_session_coffre = pow(cle_publique_utilisateur, cle_privee_coffre, prime)  # Clé partagée du coffre
    cle_de_session_client = pow(cle_publique_coffre, cle_privee_utilisateur, prime)  # Clé partagée de l'utilisateur

    # Vérification : Les clés partagées doivent être identiques
    assert cle_de_session_coffre == cle_de_session_client, "Les clés de session ne correspondent pas !"

    return cle_de_session_coffre