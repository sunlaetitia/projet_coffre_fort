import random
from contexte import contexte
import certificat

def protocole_guillou_quisquater(utilisateur, cle_pub_utilisateur, certificat_signature, p):
    """
    Implémentation du protocole de Guillou-Quisquater.
    - cle_publique_utilisateur : (e_utilisateur, n_utilisateur)
    - cle_privee_utilisateur : (d_utilisateur, n_utilisateur)
    """
    userdoc = f"coffre_fort\\Utilisateurs\\{utilisateur}\\cles.pem"
    with open(userdoc, "r") as fichier:
        cle_pri_utilisateur = fichier.read()
    cle_pri_utilisateur = cle_pri_utilisateur.strip("[] \n")
    cle_pri_utilisateur = [int(x.strip()) for x in cle_pri_utilisateur.split(",")]
    # Étape 1 : Initialisation des clés
    e_utilisateur, n_utilisateur = cle_pub_utilisateur
    d_utilisateur = cle_pri_utilisateur[0]
 
    m = random.randint(1, p - 1)

    # Calcul de M = m^e (mod n)
    M = pow(m, e_utilisateur, n_utilisateur)
    r = random.randint(1, e_utilisateur - 1)

   
    S_N = pow(certificat_signature, -d_utilisateur, n_utilisateur)
    S_N_r = pow(S_N, r, n_utilisateur) 
    Preuve = (m * S_N_r) % n_utilisateur
    
    # vérification si Cert^r × Preuve^e ≡ M (mod n)
    verification = (pow(certificat_signature, r, n_utilisateur) * pow(Preuve, e_utilisateur, n_utilisateur)) % n_utilisateur
    if verification == M:
        print("Vérification réussie :Utilisateur authentifié.")
        return True
    else:
        print("Vérification échouée :Utilisateur non authentifié..")
        return False
