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



def sha256(data):
    # Padding
    length_bits = len(data) * 8
    data += b'\x80'
    while (len(data) + 8) % 64 != 0:
        data += b'\x00'
    data += length_bits.to_bytes(8, 'big')

    # Initial hash values (constants for SHA-256)
    h0 = 0x6A09E667
    h1 = 0xBB67AE85
    h2 = 0x3C6EF372
    h3 = 0xA54FF53A
    h4 = 0x510E527F
    h5 = 0x9B05688C
    h6 = 0x1F83D9AB
    h7 = 0x5BE0CD19

    # Round constants (first 32 bits of the fractional parts of the cube roots of the first 64 primes)
    k = [
        0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
        0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
        0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
        0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
        0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
        0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
        0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
        0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
    ]

    # Helper functions
    def right_rotate(n, b):
        return ((n >> b) | (n << (32 - b))) & 0xFFFFFFFF

    # Process the message in 512-bit blocks
    for i in range(0, len(data), 64):
        block = data[i:i+64]

        # Break the block into 16 32-bit big-endian words
        words = [int.from_bytes(block[j:j+4], 'big') for j in range(0, 64, 4)]

        # Extend the 16 words into 64 words
        for j in range(16, 64):
            s0 = right_rotate(words[j-15], 7) ^ right_rotate(words[j-15], 18) ^ (words[j-15] >> 3)
            s1 = right_rotate(words[j-2], 17) ^ right_rotate(words[j-2], 19) ^ (words[j-2] >> 10)
            words.append((words[j-16] + s0 + words[j-7] + s1) & 0xFFFFFFFF)

        # Initialize hash values for this block
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7

        # Main loop
        for j in range(64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + S1 + ch + k[j] + words[j]) & 0xFFFFFFFF
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF

            h, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF

        # Update hash values for this block
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    # Produce the final hash value
    hash_value = (h0 << 224) | (h1 << 192) | (h2 << 160) | (h3 << 128) | (h4 << 96) | (h5 << 64) | (h6 << 32) | h7

    return "{:064x}".format(hash_value)
