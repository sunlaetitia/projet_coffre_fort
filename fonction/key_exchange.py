import random

def text_to_binary(text):
    """Convertit une chaîne de caractères en une chaîne binaire."""
    return ''.join(format(ord(char), '08b') for char in text)

# Fonction pour vérifier si un nombre est premier
def est_premier(x):
    if x < 2:
        return False
    for i in range(2, int(x**0.5) + 1):
        if x % i == 0:
            return False
    return True

# Fonction pour trouver un nombre premier plus grand qu'un certain nombre
def trouver_premier(n):
    while not est_premier(n):
        n += 1
    return n

# Fonction pour trouver un générateur valide pour un nombre premier donné
def trouver_generateur(prime):
    """Trouve un générateur valide pour un nombre premier."""
    for g in range(2, prime):
        if all(pow(g, k, prime) != 1 for k in range(1, prime - 1)):
            return g
    raise ValueError("Aucun générateur valide trouvé.")

def diffie_hellmann(cle_privee_coffre, cle_publique_coffre, cle_privee_utilisateur, cle_publique_utilisateur):
    # Étape 1 : Génération des paramètres Diffie-Hellman
    prime = trouver_premier(2**128)  # Générer un grand nombre premier (p) pour garantir une clé de 128 bits
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

    # Étape 4 : Transformation de la clé en binaire
    cle_partagee_binaire = text_to_binary(str(cle_de_session_coffre))

    # Vérification de la longueur de la clé binaire
    if len(cle_partagee_binaire) < 128:
        print("Attention : la clé générée est inférieure à 128 bits.")
    else:
        cle_partagee_binaire = cle_partagee_binaire[:128]  # Tronquer à 128 bits si nécessaire

    print(f"Paramètres : p = {prime}, g = {generator}")
    print(f"Clé partagée (en binaire) : {cle_partagee_binaire}")
    print(f"Taille de la clé : {len(cle_partagee_binaire)} bits")

# Appel de la fonction
diffie_hellmann()
