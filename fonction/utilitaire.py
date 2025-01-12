import random
import json
import os
from contexte import chemin_bd_json
import re
from datetime import datetime, timedelta

def generer_premier(min_val=2**1023, max_val=2**1024):
    """
    Génère un nombre premier dans une plage donnée à l'aide du test de primalité de Miller-Rabin.
    """
    while True:
        p = random.randint(min_val, max_val)
        if miller_rabin(p):
            return p

def miller_rabin(n, k=10):
    # Cas de base pour les petits nombres
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Écrire n-1 comme 2^s * d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Effectuer k tests de Miller-Rabin
    for _ in range(k):
        a = random.randint(2, n - 2)  # Choisir un nombre aléatoire entre 2 et n-2
        x = pow(a, d, n)  # Calculer a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)  # Calculer x^2 % n
            if x == n - 1:
                break
        else:
            return False
    return True

def generer_sel():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))

def charger_base_de_donnee():
    if os.path.exists(chemin_bd_json):
        with open(chemin_bd_json, 'r') as fichier:
            return json.load(fichier)
    return {}

def charger_cle(chemin):
    if os.path.exists(chemin):
        with open(chemin, 'r') as fichier:
            return json.load(fichier)
    return {}


def ajouter_utilisateur(nom_utilisateur,hash_mdp, sel, cle_derivee, cle_privee, cle_publique,expiration, p):
    expiration = (datetime.utcnow() + timedelta(days=365)).isoformat()
    base_de_donnee = charger_base_de_donnee()
    base_de_donnee[nom_utilisateur] = {
        "sel": sel,
        "cle_derivee": cle_derivee.hex(),
        # "cle_privee": cle_privee,
        "cle_publique": cle_publique,
        "p": p,
        "hash_mdp": hash_mdp,
        "expiration": expiration,
        "session": 0

    }
    with open(chemin_bd_json, "w") as fichier:
        json.dump(base_de_donnee, fichier, indent=4)
    print(f"Utilisateur {nom_utilisateur} ajouté à la base de données.")
    chemin_utilisateurx = f"coffre_fort\\Utilisateurs\\{nom_utilisateur}\\cles.pem"
    with open(chemin_utilisateurx, "w") as fichier_sortie:
        json.dump(cle_privee, fichier_sortie, indent=4)


def generer_cle_RSA():
    """
    Génère dynamiquement un couple de clés RSA (publique et privée).
    - La clé publique est (e, n)
    - La clé privée est (d, n)
    """
    # Étape 1 : Générer deux nombres premiers distincts p et q
    p = generer_premier(2**1023, 2**1024)
    q = generer_premier(2**1023, 2**1024)
    while p == q:  # S'assurer que p et q sont distincts
        q = generer_premier(2**1023, 2**1024)

    # Calcul de n et φ(n) (phi de n)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Étape 2 : Choisir e tel que pgcd(e, φ(n)) = 1
    e = random.randint(2, phi_n - 1)  # Choix aléatoire de e
    while pgcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)

    # Étape 3 : Calculer d, l'inverse modulaire de e modulo φ(n)
    d = inverse_modulaire(e, phi_n)

    # Vérification de la relation fondamentale
    if (e * d) % phi_n != 1:
        raise ValueError("Erreur : Les clés générées ne respectent pas la relation e * d ≡ 1 mod φ(n)")
    
    expiration = datetime.utcnow() + timedelta(days=365)
    # Retour des clés publique et privée
    return (e, n), (d, n), expiration, p

def renouveler_cle_RSA():
    return generer_cle_RSA()

# Fonction pour générer l'inverse modulaire (d)
def inverse_modulaire(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Fonction pour calculer le pgcd (plus grand commun diviseur)
def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a
# Calcul de la puissance modulaire : m^e mod n
def puissance_modulaire(m, e, n):
    return pow(m, e, n)

# Vérifier la robustesse du mot de passe
def verifier_mot_de_passe(mot_de_passe):
    """Vérifie si un mot de passe est robuste."""
    regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&^#()+=\-_{}[\]|\\:;\"'<>,.?/])[A-Za-z\d@$!%*?&^#()+=\-_{}[\]|\\:;\"'<>,.?/]{5,}$"
    return re.match(regex, mot_de_passe) is not None
