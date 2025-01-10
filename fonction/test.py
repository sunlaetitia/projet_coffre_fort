userdoc = f"coffre_fort\\Utilisateurs\\sun\\cles.pem"
with open(userdoc, "r") as fichier:
        cle_pri_utilisateur = fichier.read()
cle_pri_utilisateur = cle_pri_utilisateur.strip("[] \n")
cle_pri_utilisateur = [int(x.strip()) for x in cle_pri_utilisateur.split(",")]
print(cle_pri_utilisateur)    
    # Étape 1 : Initialisation des clés