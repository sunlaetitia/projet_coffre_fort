def derivee_cle(mot_de_passe: str, sel: str, iterations: int = 1000, longueur_cle: int = 16):
    """
    Dérive une clé privée à partir d'un mot de passe en utilisant une fonction éponge personnalisée.

    :param mot_de_passe: Le mot de passe en clair fourni par l'utilisateur.
    :param sel: Une valeur unique pour éviter les attaques par dictionnaire.
    :param iterations: Nombre d'itérations pour renforcer la dérivation.
    :param longueur_cle: Longueur de la clé dérivée (en octets).
    :return: La clé dérivée sous forme d'un tableau d'octets.
    """
    if not isinstance(mot_de_passe, str) or not isinstance(sel, str):
        raise ValueError("Le mot de passe et le sel doivent être des chaînes de caractères.")

    # Convertir le mot de passe et le sel en octets
    mot_de_passe_octets = mot_de_passe.encode('utf-8')
    sel_octets = sel.encode('utf-8')

    # Initialiser un tampon avec le mot de passe et le sel combinés
    etat = bytearray(mot_de_passe_octets + sel_octets)

    # Phase d'absorption: Mélange initial
    for i in range(len(etat)):
        etat[i] ^= (etat[i] + i) % 256

    # Phase d'essorage: Appliquer plusieurs itérations de mélange
    for _ in range(iterations):
        tampon_temporaire = bytearray(len(etat))
        for i in range(len(etat)):
            tampon_temporaire[i] = (etat[i - 1] ^ etat[i] ^ (etat[(i + 1) % len(etat)])) % 256
        etat = tampon_temporaire

    # Extraction de la clé dérivée
    cle = bytearray()
    while len(cle) < longueur_cle:
        for i in range(0, len(etat), 2):
            if len(cle) < longueur_cle:
                cle.append((etat[i] + etat[(i + 1) % len(etat)]) % 256)

    return bytes(cle)

