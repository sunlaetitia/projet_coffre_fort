import random as rd
import json


#Conversion du fichier de caractères en fichier de binaires: // ok

def Text_To_Binary(Fichier_Text, Nom_fichier):
  with open(Fichier_Text, 'r', encoding='utf-8') as fichier:
   Message = fichier.read()
  Message_bin = ''.join(format(ord(caractere), '08b') for caractere in Message)
  with open('fichier_binaire.txt', 'w', encoding='utf-8') as fichier_binaire:
    fichier_binaire.write(Message_bin)
  return Message_bin



#Affichage d'un message binaire en message avec caractères // ok

def Bin_To_Text(Texte_binaire, Nom_fichier):
  Message_Code = ' '.join(Texte_binaire[i : i+8] for i in range(0, len(Texte_binaire), 8))
  Octets = Message_Code.split()
  Message_decode = ''.join(chr(int(groupe, 2)) for groupe in Octets)
  #On écrit le message décodé dans un fichier (Facultatif)
  with open(Nom_fichier, 'w', encoding='utf-8') as fichier_message:
    fichier_message.write(Message_decode)
  print(Message_decode)

#Bin_To_Text(Message_chiffre, "Faux_Message.txt")





# Cas d'un text // juste pour tester le dechiffrement 




def Text_To_Binary(text):
    """Convertit une chaîne de caractères en une chaîne binaire."""
    return ''.join(format(ord(char), '08b') for char in text)

def text_to_binary(text):
    """Convertit une chaîne de caractères en une chaîne binaire."""
    return ''.join(format(byte, '08b') for byte in text)

def binary_to_text(binary_string):
    #Convertit une chaîne binaire en une chaîne de caractères.
    chars = [chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8)]
    return ''.join(chars) 




def afficher_binaire_en_texte(binary_message):
    
    #Affiche un message binaire en une chaîne lisible.
    #Les caractères non imprimables sont représentés sous la forme \xHH (code hexadécimal).
    
    texte_clair = binary_to_text(binary_message)  # Conversion binaire -> texte
    texte_codé = ''
    
    for c in texte_clair:
        if c.isprintable():
            texte_codé += c  # Conserver les caractères imprimables
        else:
            texte_codé += f"\\x{ord(c):02x}"  # Représenter les non imprimables en hexadécimal
    
    return texte_codé

def convertir_texte_en_binaire(texte_codé):
    
    #Convertit un texte lisible (avec \xHH pour les non imprimables) en une chaîne binaire.
    
    i = 0
    binaire_restitué = ''
    
    while i < len(texte_codé):
        if texte_codé[i] == '\\' and i + 3 < len(texte_codé) and texte_codé[i+1] == 'x':
            # Lire le code hexadécimal
            code_hex = texte_codé[i+2:i+4]
            char = chr(int(code_hex, 16))
            binaire_restitué += format(ord(char), '08b')
            i += 4  # Sauter les 4 caractères (\x..)
        else:
            # Traiter les caractères imprimables
            binaire_restitué += format(ord(texte_codé[i]), '08b')
            i += 1
    
    return binaire_restitué




def xor_binary(bin1, bin2):
    """Effectue un XOR entre deux chaînes binaires de même longueur."""
    return ''.join(str(int(a) ^ int(b)) for a, b in zip(bin1, bin2))

def pad_binary(binary_message):
    """Ajoute du padding pour que la longueur du message soit un multiple de 128 bits."""
    padding_length = 128 - (len(binary_message) % 128)
    if padding_length == 128:
        return binary_message  # Pas de padding nécessaire
    return binary_message + '0' * padding_length

def unpad_binary(binary_message):
    """Supprime le padding ajouté lors du chiffrement."""
    return binary_message.rstrip('0')   





#Générer une clé de N bits // ok mais a modifier

def Key_of_N_bits(N): # Générer une clé de N bits
  return ''.join(str(rd.randint(0,1)) for i in range (N))

Key = Key_of_N_bits(256)   # pour cobra on utilisera une cle de 256 bits 
#Key


#2.   Substitution &   4. Transformation   Linéaire


# SBOX 
# Quatre S-boxes de 4 bits (16 valeurs possibles pour chaque S-box)
# Creation de SBOX  en fonction de celle de DES  // en cour de codage    4 types de S-BOX
S_BOXES = [
    ['0110', '0100', '1100', '0101', '0000', '0111', '0010', '1110', '0001', '1111', '0011', '1101', '1010', '1001', '1011', '1000'],  # S-box 1
    ['1111', '1100', '0010', '1000', '0100', '1001', '0001', '1010', '0000', '1110', '0110', '0111', '1011', '0101', '0011', '1101'],  # S-box 2
    ['1000', '0110', '0111', '1001', '0011', '1100', '1010', '0010', '0101', '1111', '0100', '0000', '1101', '1110', '0001', '1011'],  # S-box 3
    ['1010', '0100', '0001', '1101', '0000', '0101', '1100', '0111', '0110', '1111', '1000', '1110', '1011', '1001', '0011', '0010']   # S-box 4
]


#compter les bits des cles // OK
def count_bits(binary_key):
    """
    Compte tous les bits d'une clé binaire.
    :param binary_key: Clé sous forme de chaîne binaire (ex. '1010').
    :return: Nombre total de bits.
    """
    if all(c in '01' for c in binary_key):  # Vérifie que la chaîne contient uniquement '0' ou '1'
        return len(binary_key)
    else:
        raise ValueError("La clé doit contenir uniquement des caractères '0' et '1'.")
    


    
def substitute_using_sbox(word, sbox):
    """
    Applique la substitution à une sous-clé de 32 bits (8 blocs de 4 bits) en utilisant une S-box.
    :param word: Une sous-clé de 32 bits (chaîne binaire).
    :param sbox: La S-box à utiliser (liste de chaînes binaires de 4 bits).
    :return: La sous-clé après substitution.
    """
    substituted = ""
    for i in range(8):  # Découper en 8 blocs de 4 bits
        block = word[i*4:(i+1)*4]  # Récupère le bloc de 4 bits
        index = int(block, 2)  # Convertir le bloc en entier pour l'utiliser comme index dans la S-box
        substituted += sbox[index]  # Applique la S-box (chaque entrée est une chaîne binaire de 4 bits)
    return substituted





def apply_sbox_to_group(subkey_group, sbox):
    """
    Applique la substitution via la S-box à un groupe de 4 sous-clés de 32 bits.
    :param subkey_group: Un groupe de 4 sous-clés de 32 bits (liste de chaînes binaires).
    :param sbox: La S-box à utiliser pour la substitution.
    :return: Le groupe de sous-clés après substitution.
    """
    return [substitute_using_sbox(word, sbox) for word in subkey_group]




# le key scheduling permettra de generer 33 cles pour les 32 tours de chiffrement a partir de la cle secrete initiale(256 bits par des 0 padding ou pas)
# ok
def key_expansion(initial_key):
    """
    Génère 132 sous-clés de 32 bits pour l'algorithme COBRA basé sur Serpent.

    :param initial_key: La clé initiale (sous forme de chaîne binaire).
    :return: Une liste contenant 132 sous-clés de 32 bits sous forme binaire.
    """
    # Constantes
    PHI = "10011110001101110111100110111001"  # Approximation binaire du nombre d'or (32 bits)
    ROTATE_BITS = 11  # Rotation circulaire à gauche de 11 bits.

    key_size = count_bits(initial_key)

    # Étape 1 : Initialisation de la clé (padding si nécessaire)
    if key_size == 128:
        padded_key = initial_key.ljust(256, '0')  # Compléter par des zéros pour obtenir 256 bits
    elif key_size == 192:
        padded_key = initial_key.ljust(256, '0')  # Compléter par des zéros pour obtenir 256 bits
    elif key_size == 256:
        padded_key = initial_key  # Utiliser telle quelle
    else:
        raise ValueError("Invalid key size. Must be 128, 192, or 256 bits.")

    # Diviser la clé de 256 bits en 8 blocs de 32 bits
    K = [padded_key[i:i+32] for i in range(0, 256, 32)]  # 8 blocs de 32 bits
    K.reverse()  # Les bits les moins significatifs sont à gauche

    # Étape 2 : Génération des sous-clés (wi)
    W = K.copy()
    for i in range(8, 132):  # On génère w8 à w131
        # XOR des 4 derniers éléments de W et ajout de PHI et de l'index
        new_w = format(int(W[i - 8], 2) ^ int(W[i - 5], 2) ^ int(W[i - 3], 2) ^ int(W[i - 1], 2) ^ int(PHI, 2) ^ i, '032b')

        # Rotation circulaire à gauche de 11 bits
        rotated_w = new_w[ROTATE_BITS:] + new_w[:ROTATE_BITS]
        W.append(rotated_w)

    # Étape 3 : Retourner seulement les sous-clés de 32 bits
    return W[8:]  # On retourne les sous-clés générées de w8 à w131



def generate_round_keys(W):
    """
    Génère les 33 clés de tour de 128 bits chacune, en appliquant les S-Boxes appropriées.
    :param W: Liste des sous-clés générées (en binaire).
    :return: Une liste de 33 clés de tour de 128 bits chacune.
    """
    round_keys = []
    for i in range(33):  # 33 clés de tour
        subkey_group = W[4*i:4*i+4]  # Chaque clé de tour utilise 4 sous-clés de 32 bits

        # Sélectionner la S-Box en fonction de l'indice de la clé de tour
        if i < 8:
            sbox = S_BOXES[0]  # S-Box 1 pour les clés de tour 0 à 7
        elif i < 16:
            sbox = S_BOXES[1]  # S-Box 2 pour les clés de tour 8 à 15
        elif i < 24:
            sbox = S_BOXES[2]  # S-Box 3 pour les clés de tour 16 à 23
        else:
            sbox = S_BOXES[3]  # S-Box 4 pour les clés de tour 24 à 31

        # Appliquer la S-Box au groupe de sous-clés
        substituted_group = apply_sbox_to_group(subkey_group, sbox)

        # Concaténer les 4 sous-clés pour produire une clé de 128 bits
        round_keys.append(''.join(substituted_group))

    return round_keys


# A LA FIN IL Y A 30 CLES DE TOUR DE 128 bits 

def extract_first_12_keys(initial_key): # extrait les 12 premieres cles pour reduire a 12 rounds 

    #Étape 1 : Génération des sous-clés
    round_subkeys = key_expansion(initial_key)

    # Étape 2 : Génération des clés de tour de 128 bits avec application des S-Boxes
    all_keys = generate_round_keys(round_subkeys)

    return all_keys[:12]



#3. La-Feistel-de-Réré


def inverse_bits_in_byte(byte):
    """
    Inverse l'ordre des bits dans un octet (8 bits).
    :param byte: Un entier entre 0 et 255.
    :return: Entier avec les bits inversés.
    """
    return int(f"{byte:08b}"[::-1], 2)

def modular_inverse(x, mod=257):
    """
    Calcule l'inverse modulaire de (x+1) modulo 257, puis soustrait 1.
    :param x: Un entier entre 0 et 255.
    :param mod: Modulo (257 par défaut).
    :return: Résultat de la fonction f(x) = ((x+1)^(-1) mod 257) - 1
    """
    x_plus_1 = (x + 1) % mod
    inverse = pow(x_plus_1, -1, mod)  # Inverse modulaire
    return (inverse - 1) % mod

def process_block_r(block_r):
    """
    Prend un bloc R de 64 bits, inverse les bits dans chaque sous-bloc de 8 bits,
    puis applique la fonction inverse f(x).
    :param block_r: Chaîne binaire de 64 bits.
    :return: Nouveau bloc Z après transformation.
    """
    if len(block_r) != 64 or not set(block_r).issubset({"0", "1"}):
        raise ValueError("Le bloc doit être une chaîne binaire de 64 bits.")

    # Diviser en sous-blocs de 8 bits
    blocks = [int(block_r[i:i+8], 2) for i in range(0, 64, 8)]

    # Inverser les bits dans chaque octet et appliquer la fonction inverse
    transformed_blocks = [modular_inverse(inverse_bits_in_byte(b)) for b in blocks]

    # Reconstituer le bloc final
    return ''.join(f"{b:08b}" for b in transformed_blocks)

def permute_bits(block, permutation_vector):
    """
    Applique une permutation des bits selon un vecteur de permutation donné.
    :param block: Chaîne binaire de 64 bits.
    :param permutation_vector: Liste des positions pour la permutation.
    :return: Bloc binaire permuté.
    """
    if len(block) != 64 or len(permutation_vector) != 64:
        raise ValueError("Le bloc et le vecteur de permutation doivent avoir 64 bits.")
    
    return ''.join(block[permutation_vector[i]] for i in range(64))


def function_F(bloc_r,round_key):
    permutation_vector = list(range(63, -1, -1))  # Exemple : Inversion des bits

    # Étape 1 : Transformation du bloc R en bloc Z
    bloc_z = process_block_r(bloc_r)
    #print("Bloc Z (transformé) :", bloc_z)

    # Étape 2 : Permutation des bits pour obtenir Y
    bloc_y = permute_bits(bloc_z, permutation_vector)
    #print("Bloc Y (permuté) :", bloc_y) 
    
    F=bloc_y
    return F


#------------------------------ La-Feistel-de-Réré--------------------------------------------#


def feistel_encrypt(binary_message, round_keys):
    """
    Implémente une structure de chiffrement de type Feistel où toutes les opérations sont binaires.
    
    :param binary_message: Message clair en binaire.
    :param key: Clé en binaire.
    :param rounds: Nombre de tours de chiffrement.
    :return: Message chiffré en binaire.
    """
    # Ajouter du padding pour que la longueur soit un multiple de 128 bits
    binary_message = pad_binary(binary_message)
    
    L, R = binary_message[:64], binary_message[64:]

    for round_key in round_keys:
        # Appliquer la fonction Feistel (ici un XOR simple avec la sous-clé)
        #F = xor_binary(R, round_key[:len(R)])  # Sous-clé de la taille de R
        F=function_F(R,round_key)
        L, R = R, xor_binary(L, F)
       
    return L + R


################################################################ Dechiffrement cobra ########################################################################


#--------------------------------- inverse function F de fiestel----------------------------------#


def reverse_process_block_z(block_z):
    """
    Inverse les étapes pour revenir au bloc R original à partir du bloc Z.
    :param block_z: Chaîne binaire de 64 bits transformées.
    :return: Bloc R original.
    """
    if len(block_z) != 64 or not set(block_z).issubset({"0", "1"}):
        raise ValueError("Le bloc doit être une chaîne binaire de 64 bits.")

    # Diviser en sous-blocs de 8 bits
    blocks = [int(block_z[i:i+8], 2) for i in range(0, 64, 8)]

    # Appliquer l'inverse de la fonction inverse et réinverser les bits
    original_blocks = [inverse_bits_in_byte((pow((b + 1) % 257, -1, 257) - 1) % 257) for b in blocks]

    # Reconstituer le bloc original
    return ''.join(f"{b:08b}" for b in original_blocks)

def reverse_permute_bits(block, permutation_vector):
    """
    Applique l'inverse d'une permutation des bits pour revenir au bloc d'origine.
    :param block: Chaîne binaire de 64 bits permutée.
    :param permutation_vector: Liste des positions pour inverser la permutation.
    :return: Bloc binaire original.
    """
    if len(block) != 64 or len(permutation_vector) != 64:
        raise ValueError("Le bloc et le vecteur de permutation doivent avoir 64 bits.")

    reverse_vector = [0] * 64
    for i, pos in enumerate(permutation_vector):
        reverse_vector[pos] = i
    
    return ''.join(block[reverse_vector[i]] for i in range(64))


def i_function_F(bloc_y):

    permutation_vector = list(range(63, -1, -1))  # Exemple : Inversion des bits vecteur
    bloc_z_restaurer = reverse_permute_bits(bloc_y, permutation_vector)
    
    bloc_restaurer = reverse_process_block_z(bloc_z_restaurer)
   

    return bloc_restaurer


def feistel_decrypt(binary_message, key):
    """
    Implémente le déchiffrement de type Feistel où toutes les opérations sont binaires.
    
    :param binary_message: Message chiffré en binaire.
    :param key: Clé en binaire.
    :param rounds: Nombre de tours de déchiffrement.
    :return: Message clair en binaire.
    """
    L, R = binary_message[:64], binary_message[64:]

    # Générer les sous-clés dans l'ordre inverse
   
    round_keys = key[::-1]
    
    for round_key in round_keys:
        # Appliquer la fonction Feistel à l'envers
       # F = xor_binary(L, round_key[:len(L)])  # Sous-clé de la taille de L
        F2=i_function_F(L)
        L, R = xor_binary(R, F2), L

    
    # Retirer le padding ajouté lors du chiffrement
   # return unpad_binary(L + R)
    return L + R

def binary_to_bytes(binary_message):
    """
    Convertit un message binaire (chaîne de '0' et '1') en bytes.
    """
    return int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, byteorder='big')

def chiffrer_fichier(fichier, cle_derivee):
    first_12_keys = extract_first_12_keys(text_to_binary(bytes.fromhex(cle_derivee)))
    if fichier.endswith((".json", ".ipynb")):
        with open(fichier, "r") as f:
            contenu_fichier_init = json.load(f)
            contenu_fichier = json.dumps(contenu_fichier_init)
    elif fichier.endswith(("txt", "log", "csv", "py", "c", "cpp", "html")):
        with open(fichier, "r") as f:
            contenu_fichier = f.read()
    else:
        # Lecture en mode binaire pour les autres types de fichiers
        with open(fichier, "rb") as f:
            contenu_fichier = f.read()
    binary_message = Text_To_Binary(contenu_fichier)
    Blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)] 
    encrypted_message = ''
    for block in Blocks:
        message = feistel_encrypt(block,first_12_keys)
        encrypted_message += message
    print(f"Message chiffré: {afficher_binaire_en_texte(encrypted_message)}")
    message_chiffre = afficher_binaire_en_texte(encrypted_message)
    #message_chiffre_bytes = binary_to_bytes(encrypted_message)
    return message_chiffre

'''chemin = "C:\\Users\\Master\\GS15\\arena.txt"
cle = "a730785f2079ed777583738797f68aa7"
chiffrer_fichier(chemin, cle)
'''
def dechiffrer_fichier(fichier, cle_derivee):
    first_12_keys = extract_first_12_keys(text_to_binary(bytes.fromhex(cle_derivee)))
    '''
    if fichier.endswith(".json.chiffre"):
        with open(fichier, "r") as f:
            contenu_chiffre = json.load(f)
            contenu_fichier = json.dumps(contenu_chiffre)  # Convertir en chaîne pour le traitement
    elif fichier.endswith(".chiffre"):
        with open(fichier, "rb") as f:
            contenu_fichier = f.read() #.decode('utf-8', errors='ignore')
    '''
    #====================================================================================
    # Ouvrir et lire le contenu du fichier
    with open(fichier, 'r', encoding='utf-8') as fichier_sortie:
        contenu_fichier = fichier_sortie.read()

    # Initialiser une variable pour reconstruire la chaîne originale
    message_reconstruit = ""
    i = 0
    # Parcourir le contenu pour détecter les séquences encodées
    while i < len(contenu_fichier):
        if contenu_fichier[i] == '\\' and i + 3 < len(contenu_fichier) and contenu_fichier[i + 1] == 'x':
            # Extraire les deux caractères suivants (hexadécimal)
            code_hex = contenu_fichier[i + 2:i + 4]
            # Convertir le code hexadécimal en caractère
            try:
                char = chr(int(code_hex, 16))
                # Ajouter le caractère ou le code "\xNN" selon qu'il est imprimable ou non
                if char.isprintable():
                    message_reconstruit += char
                else:
                    message_reconstruit += f"\\x{code_hex}"
            except ValueError:
                # Si la conversion échoue, ajouter tel quel
                message_reconstruit += contenu_fichier[i:i + 4]
            i += 4  # Sauter la séquence "\xNN"
        else:
            # Ajouter directement les caractères imprimables
            message_reconstruit += contenu_fichier[i]
            i += 1
    print(message_reconstruit)
    #===================================================================================
    encrypt_binary_message = convertir_texte_en_binaire(message_reconstruit)
    Blocks = [encrypt_binary_message[i:i + 128] for i in range(0, len(encrypt_binary_message), 128)]
    Blocks[len(Blocks)-1] = pad_binary(Blocks[len(Blocks)-1])
    decrypted_message =''
    for block in Blocks:
        message = feistel_decrypt(block, first_12_keys) 
        decrypted_message += message
    message_clair = binary_to_text(decrypted_message)
    return message_clair