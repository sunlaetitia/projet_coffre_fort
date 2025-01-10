'''
message = "\x0dü\x1e\x17l%gó\x08F\x915pRXësè+ÈGªÊ2h¢\x95\x1bS~3qe et ¼á¿\x06Zd\x00\x00\x00\x00\x00"

# Nom du fichier
nom_fichier = "contenu_fichier_suivi.txt"

# Ouvrir le fichier une seule fois
with open(nom_fichier, 'w', encoding='utf-8') as fichier:
    # Parcourir chaque caractère du message
    for i in message:
        if i.isprintable():
            # Afficher le caractère imprimable et l'écrire dans le fichier
           # print(i, end='')  # Affiche sans retour à la ligne
            print(i, file=fichier, end='')  # Écrit sans retour à la ligne
        else:
            # Convertir le caractère non imprimable en code hexadécimal
            code_hex = f"\\x{ord(i):02x}"
           # print(code_hex, end='')  # Affiche sans retour à la ligne
            print(code_hex, file=fichier, end='')  # Écrit sans retour à la ligne


with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()  # Lire tout le contenu du fichier
print(f"Contenu du fichier '{nom_fichier}' :\n{contenu}")

'''
# Nom du fichier contenant les données encodées
nom_fichier = "contenu_fichier_suivi.txt"

# Ouvrir et lire le contenu du fichier
with open(nom_fichier, 'r', encoding='utf-8') as fichier:
    contenu = fichier.read()

# Initialiser une variable pour reconstruire la chaîne originale
message_reconstruit = ""
i = 0

# Parcourir le contenu pour détecter les séquences encodées
while i < len(contenu):
    if contenu[i] == '\\' and i + 3 < len(contenu) and contenu[i + 1] == 'x':
        # Extraire les deux caractères suivants (hexadécimal)
        code_hex = contenu[i + 2:i + 4]
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
            message_reconstruit += contenu[i:i + 4]
        i += 4  # Sauter la séquence "\xNN"
    else:
        # Ajouter directement les caractères imprimables
        message_reconstruit += contenu[i]
        i += 1

# Afficher la chaîne reconstruite, caractère par caractère, sans guillemets
#print(message_reconstruit)

