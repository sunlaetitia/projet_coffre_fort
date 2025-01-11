import json
import os
from contexte import chemin_Utilisateurs, chemin_doc_crypté
from journalisation import journaliser_action
import cobra
import utilitaire
from coffrefort_blockchain import Blockchain

blockchain =  Blockchain(debug=True) # creation d'une instance de classe 

def ajouter_fichier(fichier, utilisateur:str, cle_derivee):
    """Ajoute un fichier au coffre-fort avec des permissions personnalisées."""
    if not os.path.exists(fichier):
        print(f"Le fichier {fichier} n'existe pas.")
        return None

    try:
        # Demander les permissions à l'utilisateur
        base_de_donnees = utilitaire.charger_base_de_donnee()
        utilisateurs = list(base_de_donnees.keys())
        viewers = [utilisateur]
        print("Paramètres de permissions pour le fichier :")
        rendre_public = input("Voulez-vous rendre ce fichier consultable par tout le monde ? (oui/non) : ").strip().lower() == "oui"
        permettre_modification = input("Voulez-vous permettre à tout le monde de modifier ce fichier ? (oui/non) : ").strip().lower() == "oui"
        all_or_one_user = input("Voulez vous partager ce fichier avec tous les utilisateurs? (oui/non) : ").strip().lower() == "oui"

        if rendre_public:
            if all_or_one_user:
                viewers = "all"
            else:
                print("Avec qui voulez vous partager ce fichier? : " , " ,".join(utilisateurs))
                viewers = input("Entrez votre choix (exactement comme affiché) : ")
                viewers = viewers.split(" ,")
                viewers.append(utilisateur)
        else:
            viewers = [utilisateur]

        if permettre_modification:
            editors = "all"
        else:
            editors = [utilisateur]

        permissions = {
            'owner': utilisateur,
            'viewers': viewers,
            'editors': editors
        }
        if "all" in viewers:
            for user in utilisateurs:
                repertoire_utilisateur = os.path.join(chemin_Utilisateurs, user, "fichiers_cryptes")
                fichier_nom = os.path.basename(fichier)
                chemin_fichier_chiffre = os.path.join(repertoire_utilisateur, fichier_nom + ".chiffre")
                chemin_fichier_chiffre_coffre = os.path.join(chemin_doc_crypté, fichier_nom + ".chiffre")
                # repertoire_utilisateur = os.path.join(chemin_Utilisateurs, utilisateur, "fichiers_cryptes")        # Créer le répertoire de l'utilisateur s'il n'existe pas
        

                # Sauvegarder le fichier dans le répertoire de l'utilisateur
                # fichier_nom = os.path.basename(fichier)
                # chemin_fichier_chiffre = os.path.join(repertoire_utilisateur, fichier_nom + ".chiffre")
                # chemin_fichier_chiffre_coffre = os.path.join(chemin_doc_crypté, fichier_nom + ".chiffre")

                # Chiffrer le contenu
                contenu_chiffre = cobra.chiffrer_fichier(fichier, cle_derivee)
            
                ecriture_dans_fichier(chemin_fichier_chiffre, contenu_chiffre)
                ecriture_dans_fichier(chemin_fichier_chiffre_coffre, contenu_chiffre)
            
            
                # Créer le fichier metadata dans le même répertoire
                metadata_file = chemin_fichier_chiffre + ".meta"
                metadata_file_coffre = os.path.join(chemin_doc_crypté, "fichier_metadonnee" + ".meta")
                metadata = {
                    'permissions': permissions,
                    'fichier_original': fichier_nom
                }
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f)
                with open(metadata_file_coffre, 'a') as f:
                    json.dump(metadata, f)
                    f.write('\n')
                journaliser_action("Ajout de fichier", permissions.get("owner"), f"Fichier {fichier} ajouté.", f"Fichier {fichier} ajouté.")
                print(f"Fichier chiffré sauvegardé sous : {chemin_fichier_chiffre}")
            return chemin_fichier_chiffre
        else:
            print(viewers)
            for user in viewers:
                repertoire_utilisateur = os.path.join(chemin_Utilisateurs, user, "fichiers_cryptes")
                fichier_nom = os.path.basename(fichier)
                chemin_fichier_chiffre = os.path.join(repertoire_utilisateur, fichier_nom + ".chiffre")
                chemin_fichier_chiffre_coffre = os.path.join(chemin_doc_crypté, fichier_nom + ".chiffre")
                # repertoire_utilisateur = os.path.join(chemin_Utilisateurs, utilisateur, "fichiers_cryptes")        # Créer le répertoire de l'utilisateur s'il n'existe pas
        

                # Sauvegarder le fichier dans le répertoire de l'utilisateur
                # fichier_nom = os.path.basename(fichier)
                # chemin_fichier_chiffre = os.path.join(repertoire_utilisateur, fichier_nom + ".chiffre")
                # chemin_fichier_chiffre_coffre = os.path.join(chemin_doc_crypté, fichier_nom + ".chiffre")

                # Chiffrer le contenu
                contenu_chiffre = cobra.chiffrer_fichier(fichier, cle_derivee)
            
                ecriture_dans_fichier(chemin_fichier_chiffre, contenu_chiffre)
                ecriture_dans_fichier(chemin_fichier_chiffre_coffre, contenu_chiffre)
            
            
                # Créer le fichier metadata dans le même répertoire
                metadata_file = chemin_fichier_chiffre + ".meta"
                metadata_file_coffre = os.path.join(chemin_doc_crypté, "fichier_metadonnee" + ".meta")
                metadata = {
                    'permissions': permissions,
                    'fichier_original': fichier_nom
                }
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f)
                with open(metadata_file_coffre, 'a') as f:
                    json.dump(metadata, f)
                    f.write('\n')
                journaliser_action("Ajout de fichier", permissions.get("owner"), f"Fichier {fichier} ajouté.", f"Fichier {fichier} ajouté.")
                print(f"Fichier chiffré sauvegardé sous : {chemin_fichier_chiffre}")
            return chemin_fichier_chiffre
            
    except Exception as e:
        print(f"Erreur lors de l'ajout du fichier : {e}")
        journaliser_action("Ajout de fichier échoue", permissions.get("owner"), f"Erreur : {e}", f"Erreur : {e}")
        return None

def ecriture_dans_fichier(chemin, contenu):
    with open(chemin, 'w', encoding='utf-8') as fichier:
            # Parcourir chaque caractère du message
            for i in contenu:
                if i.isprintable():
                    # Afficher le caractère imprimable et l'écrire dans le fichier
                # print(i, end='')  # Affiche sans retour à la ligne
                    print(i, file=fichier, end='')  # Écrit sans retour à la ligne
                else:
                    # Convertir le caractère non imprimable en code hexadécimal
                    code_hex = f"\\x{ord(i):02x}"
                # print(code_hex, end='')  # Affiche sans retour à la ligne
                    print(code_hex, file=fichier, end='')  # Écrit sans retour à la ligne


def afficher_fichier(fichier_chiffre, cle_derivee, utilisateur):
    """Affiche le contenu d'un fichier déchiffré si l'utilisateur a les permissions."""
    if not os.path.exists(fichier_chiffre + ".meta"):
        print(f"Le fichier {fichier_chiffre} n'existe pas.")
        journaliser_action("Consultation echouee", utilisateur, f"Fichier {fichier_chiffre} introuvable.", f"Fichier {fichier_chiffre} introuvable.")
        return

    try:
        with open(fichier_chiffre + ".meta", 'r') as f:
            metadata = json.load(f)

        viewers = metadata['permissions']['viewers']
        if viewers != "all" and utilisateur not in viewers:
            print(f"Vous n'avez pas la permission de voir ce fichier.")
            return

        fichier_dechiffre = cobra.dechiffrer_fichier(fichier_chiffre, cle_derivee)
        print(f"Contenu du fichier {fichier_dechiffre} :")
        with open(fichier_dechiffre, 'r') as f:
            print(f.read())

        journaliser_action("Consultation de fichier", utilisateur, f"Fichier {fichier_chiffre} consulte.", f"Fichier {fichier_chiffre} consulte.")
    except Exception as e:
        print(f"Erreur lors de l'affichage du fichier : {e}")

def supprimer_fichier(fichier_chiffre, utilisateur):
    """Supprime un fichier du coffre-fort si l'utilisateur est le propriétaire."""
    if not os.path.exists(fichier_chiffre + ".meta"):
        print(f"Le fichier {fichier_chiffre} n'existe pas.")
        journaliser_action("Suppression echouee", utilisateur, f"Fichier {fichier_chiffre} introuvable.", f"Fichier {fichier_chiffre} introuvable.")
        return

    try:
        with open(fichier_chiffre + ".meta", 'r') as f:
            metadata = json.load(f)

        if utilisateur != metadata['permissions']['owner']:
            print(f"Vous n'avez pas la permission de supprimer ce fichier.")
            return
        nom_fichier = os.path.basename(fichier_chiffre)
        fichier_arbo_admin = os.path.join(chemin_doc_crypté, nom_fichier)
        os.remove(fichier_chiffre)
        os.remove(fichier_chiffre + ".meta")
        os.remove(fichier_arbo_admin)
        print(f"Fichier supprimé : {fichier_chiffre}")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier : {e}")

def lister_fichiers(utilisateur):
    """Liste les fichiers accessibles à l'utilisateur."""
    fichiers = []
    chemin_utilisateur = os.path.join(chemin_Utilisateurs, utilisateur, "fichiers_cryptes")
    for fichier in os.listdir(chemin_utilisateur):
        if fichier.endswith(".meta"):
            with open(os.path.join(chemin_utilisateur, fichier), 'r') as f:
                metadata = json.load(f)
                viewers = metadata['permissions']['viewers']
                if viewers == "all" or utilisateur in viewers:
                    fichiers.append(metadata['fichier_original'])
    if fichiers:
        print("Fichiers accessibles :")
        for fichier in fichiers:
            print(f"- {fichier}")
    else:
        print("Aucun fichier accessible.")
        
def initialiser_blockchain(utilisateur):
    chemin_blockchain = os.path.join(chemin_Utilisateurs, utilisateur, f"{utilisateur}_blockchain.json")
    if not os.path.exists(chemin_blockchain):
        os.makedirs(os.path.dirname(chemin_blockchain), exist_ok=True)
        # Créer un fichier JSON vide pour la blockchain
        with open(chemin_blockchain, "w") as fichier:
            # Écrire une structure initiale pour une blockchain
            json.dump([], fichier, indent=4)
    return chemin_blockchain

def menu_general(utilisateur):
    while True:
        print(f"\nBienvenue {utilisateur}, que souhaitez-vous faire ?")
        print("1. Mode Normal")
        print("2. Mode Blockchain")
        print("3. Quitter")
        
        choix_mode = input("Votre choix : ")

        if choix_mode == "1":
            menu_gestion_fichiers(utilisateur)
        elif choix_mode == "2":
            # Initialisation ou chargement de la blockchain
            chemin_blockchain = initialiser_blockchain(utilisateur)
            # blockchain = Blockchain.charger_blockchain(chemin_blockchain)
            #menu_blockchain(utilisateur, blockchain, chemin_blockchain)
            menu_blockchain(utilisateur, chemin_blockchain)

        elif choix_mode == "3":
            print("Déconnexion réussie. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def menu_gestion_fichiers(utilisateur):
    """Menu principal pour la gestion des fichiers."""
    while True:
        print(f"Bienvenue {utilisateur}, que souhaitez-vous faire ?")
        print("1. Lister les fichiers")
        print("2. Ajouter et chiffrer un fichier")
        print("3. Supprimer un fichier")
        print("4. Déchiffrer et afficher un fichier")
        print("5. Déconnexion")
        base_de_donnee = utilitaire.charger_base_de_donnee()
        cle_derivee = base_de_donnee[utilisateur]["cle_derivee"]

        choix = input("Votre choix: ")

        if choix == '1':
            lister_fichiers(utilisateur)
        elif choix == '2':
            chemin_fichier = input("Entrez le chemin du fichier à ajouter : ")
            ajouter_fichier(chemin_fichier, utilisateur, cle_derivee)
         
        elif choix == '3':
            fichier_a_supprimer = input("Entrez le chemin du fichier chiffré à supprimer : ")
            supprimer_fichier(fichier_a_supprimer, utilisateur)
        elif choix == '4':
            fichier_a_supprimer = input("Entrez le chemin du fichier chiffré à déchiffrer  : ")
            message_clair = cobra.dechiffrer_fichier(fichier_a_supprimer, cle_derivee)
            print("\n") 
            print(f"{message_clair}")    
        elif choix == '5':
            print("affichage réussie. À bientôt!")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def menu_blockchain(utilisateur, chemin_blockchain):
    """Menu pour le mode blockchain."""
    while True:
        print("\nMode Blockchain : Que souhaitez-vous faire ?")
        print("1. Ajouter un fichier à la blockchain")
        print("2. Récupérer un fichier depuis la blockchain")
        #print("3. Valider la chaîne de blocs")
        print("4. Afficher tous les blocs de la blockchain")
        print("5. Retour au menu principal")
        
        choix = input("Votre choix : ")

        if choix == "1":
            chemin_fichier = input("Chemin du fichier : ")
            fichier_nom = os.path.basename(chemin_fichier)
            with open(chemin_fichier, "r") as f:
                contenu_fichier = f.read()
            blockchain.ajouter_fichier_au_bloc(fichier_nom, contenu_fichier, utilisateur)
            blockchain.sauvegarder_blockchain(chemin_blockchain)



        elif choix == "2":
            nom_fichier = input("Nom du fichier à récupérer : ")
            contenu = blockchain.charger_blockchain(chemin_blockchain).recuperer_fichier(nom_fichier)  # serialisation a partir du json
            if contenu:
                print(f"Contenu du fichier {nom_fichier} : {contenu}")
            else:
                print(f"Le fichier {nom_fichier} n'a pas été trouvé dans la blockchain.")
        elif choix == "3":
            if blockchain.chaine_valide():
                print("La chaîne de blocs est valide.")
            else:
                print("La chaîne de blocs est invalide.")
        elif choix == "4":
            print("\nAffichage des blocs dans la blockchain :")
            for bloc in blockchain.chaine:
                print(f"Indice: {bloc.indice}, Hash: {bloc.hash}, Données: {bloc.donnees}, Preuve: {bloc.preuve}")
        elif choix == "5":
            print("Retour au menu principal.")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")