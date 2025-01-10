import cobra
from contexte import contexte
import utilitaire
import main
import dérivation
from journalisation import journaliser_action
from main import creer_arborescence_utilisateur
# en cour  de codage 
def interface():  #interface pour montrer les fonctions de façon unitaire 
    contexte.nom_utilisateur = input(" Entrer votre nom:")
    print("Bonjour ",contexte.nom_utilisateur ,"! Que souhaitez vous faire aujourd'hui ?")
    print("-->1<-- Création de repertoire")
    print("-->2<-- Générer un couple de clés publique / privée")
    print("-->3<-- Dériver le mot de passe")
    print("-->4<-- Connexion")
    print("-->5<-- Chiffrer un message")
    print("-->6<-- Déchiffrer un message")
    print("-->7<-- Hacher un message")
    print("-->7<-- Vérifier une preuve de travail")
    print("-->8<-- Générer et vérifier une signature numérique")
    print("-->9<-- Créer une blockchain")
    print("-->10<-- Ajouter un bloc à une blockchain")
    print("-->11<-- Vérifier l'intégrité d'une blockchain")
    print("-->12<-- Quitter")
    
     #switcher entre les cas 
    cas = int(input())

    if cas ==  1:
       main.initialiser_repertoires()
       main.creer_arborescence_utilisateur(contexte.nom_utilisateur)
    elif cas == 2:
       cle_privee, cle_publique, expiration, p = utilitaire.generer_cle_RSA()
       print("votre clé publique est :", cle_publique)
       print("votre clé privee est :", cle_privee)
    elif cas == 3:
        mot_de_passe = input("Entrez un mot de passe: ")
        while not utilitaire.verifier_mot_de_passe(mot_de_passe):
            mot_de_passe = input("Le mot de passe n'est pas robuste. Veuillez recommencer: ")
        sel = utilitaire.generer_sel()
        contexte.cle_derivee = dérivation.derivee_cle(mot_de_passe, sel, iterations = 1000, longueur_cle = 16)
        utilitaire.ajouter_utilisateur(contexte.nom_utilisateur, sel, contexte.cle_derivee, cle_privee, cle_publique)
        journaliser_action("Inscription", contexte.nom_utilisateur, "Nouvel utilisateur inscrit", "vous vous etes inscrit.")
    elif cas == 4:
        base_de_donnee = utilitaire.charger_base_de_donnee()
        utilisateur = contexte.nom_utilisateur
        cle_derivee = base_de_donnee[utilisateur]["cle_derivee"]
        first_12_keys = cobra.extract_first_12_keys(cobra.text_to_binary(bytes.fromhex(cle_derivee)))
        print("\n\n------------------------------------------------------------------------------------------------------------------\n\n")
        print("-->1<-- Chiffrer \n\n"+"-->2<-- dechiffrer")
        cas = int(input())
        if cas == 1:
             
             binary_message = cobra.Text_To_Binary(input("Message clair"))
             Blocks = [binary_message[i:i + 128] for i in range(0, len(binary_message), 128)] 
             encrypted_message=''
             for block in Blocks:
                 message = cobra.feistel_encrypt(block,first_12_keys)
                 encrypted_message += message  

             print(f"Message chiffré: {cobra.afficher_binaire_en_texte(encrypted_message)}") 

             


        elif cas == 2:
             encrypt_binary_message = cobra.convertir_texte_en_binaire(input("Message chiffré"))
             Blocks = [encrypt_binary_message[i:i + 128] for i in range(0, len(encrypt_binary_message), 128)]
             Blocks[len(Blocks)-1] = cobra.pad_binary(Blocks[len(Blocks)-1])
             decrypted_message =''
             for block in Blocks:
              message = cobra.feistel_decrypt(block, first_12_keys) 
              decrypted_message += message

             print("\n") 
             print(f"Message déchiffré: {cobra.binary_to_text(decrypted_message)}") 
        else :
           print() 
    elif cas == 2:
        print('')  
    elif cas == 2:
        print('') 
    elif cas == 2:
        print('')  
    else:
      print("Cas non trouvé")
    
interface()