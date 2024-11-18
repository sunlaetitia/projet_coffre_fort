import os
import hashlib
from Crypto.PublicKey import RSA


# ===========================================
# Section 1: Enregistrement des utilisateurs
# ===========================================

def creer_utilisateur(nom_utilisateur, base_path="coffre_fort_utilisateurs"):
    """
    Enregistre un utilisateur en générant un couple de clés RSA et un répertoire sécurisé.

    Args:
        nom_utilisateur (str): Nom unique de l'utilisateur.
        base_path (str): Chemin de base pour les utilisateurs.

    Returns:
        dict: Informations utilisateur (chemin, clés).
    """
    chemin_utilisateur = os.path.join(base_path, nom_utilisateur)
    
    # Créer le répertoire utilisateur
    os.makedirs(chemin_utilisateur, exist_ok=True)

    # Génération des clés RSA
    cle_rsa = RSA.generate(2048)
    chemin_cle_privee = os.path.join(chemin_utilisateur, "cle_privee.pem")
    chemin_cle_publique = os.path.join(chemin_utilisateur, "cle_publique.pem")
    
    with open(chemin_cle_privee, "wb") as f:
        f.write(cle_rsa.export_key())
    with open(chemin_cle_publique, "wb") as f:
        f.write(cle_rsa.publickey().export_key())
    
    return {
        "chemin": chemin_utilisateur,
        "cle_privee": chemin_cle_privee,
        "cle_publique": chemin_cle_publique
    }

# ===========================================
# Section 2: Dérivation de clé (KDF)
# ===========================================

def derivee_cle(mot_de_passe, sel=None, iterations=100000, taille_cle=32):
    """
    Dérive une clé cryptographique robuste à partir d'un mot de passe.

    Arguments:
        mot_de_passe (str): Mot de passe fourni par l'utilisateur.
        sel (bytes): Valeur aléatoire ajoutée pour renforcer la clé. Si None, il sera généré.
        iterations (int): Nombre d'itérations pour renforcer la clé.
        taille_cle (int): Taille de la clé dérivée.

    Returns:
           Clé dérivée et sel.
    """
    if sel is None:
        sel = os.urandom(16)  # Génération d'un sel aléatoire
    
    mot_de_passe_bytes = mot_de_passe.encode('utf-8')
    cle_derivée = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=mot_de_passe_bytes,
        salt=sel,
        iterations=iterations,
        dklen=taille_cle
    )
    return {
        "cle_derivée": cle_derivée,
        "sel": sel
    }

