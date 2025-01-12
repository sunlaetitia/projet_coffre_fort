#certificat.py
import os
import random
import datetime


def generer_certificat(cle_pub_utilisateur, cle_pri_coffre_fort, utilisateur, chemin_fichier_utilisateur):
    e, n = cle_pub_utilisateur
    d_coffre_fort, n_coffre_fort = cle_pri_coffre_fort
    signature = pow(e, d_coffre_fort, n_coffre_fort)

    date_emission = datetime.datetime.utcnow()
    date_expiration = date_emission + datetime.timedelta(days=365)
    certificat = f"""-----BEGIN CERTIFICATE-----
Version: 1
Serie: {random.randint(1000, 9999)}
Sujet: {utilisateur}
Cle_publique: {cle_pub_utilisateur}
Date_emission: {date_emission}
Date_expiration: {date_expiration}
Emetteur: Coffre-Fort
Signature: {signature}
-----END CERTIFICATE-----"""
    cert_pem = os.path.join(chemin_fichier_utilisateur)
    with open(cert_pem, "w") as certfile:
        certfile.write(certificat)
    return signature, cert_pem

def verifier_certificat(certificat, cle_publique_coffre_fort):
    signature = int(certificat.split("Signature: ")[1].split("\n")[0])
    e_vault, n_vault = cle_publique_coffre_fort
    decrypted_e = pow(signature, e_vault, n_vault)
    return decrypted_e

def demander_verification_ca(certificat, cle_publique_coffre_fort):
    return verifier_certificat(certificat, cle_publique_coffre_fort)

def generer_chemin_certificat(nom_utilisateur):
    chemin_repertoire_utilisateur = os.path.join("coffre_fort", "Utilisateurs", nom_utilisateur)
    chemin_certificat = os.path.join(chemin_repertoire_utilisateur, f"{nom_utilisateur}_certificat.pem")
    return chemin_certificat

def enregistrer_certificat_utilisateur(nom_utilisateur, certificat_pem):
    chemin_certificat = generer_chemin_certificat(nom_utilisateur)
    with open(chemin_certificat, "w") as fichier_certificat:
        fichier_certificat.write(certificat_pem)
        
