#coffrefort_blockchain.py
import time
import json
class Bloc:
    def __init__(self, indice, hash_precedent, horodatage, donnees, preuve):
        self.indice = indice
        self.hash_precedent = hash_precedent
        self.horodatage = horodatage
        self.donnees = donnees
        self.preuve = preuve
        self.hash = self.calculer_hash()

    def calculer_hash(self):
        """Calcule le hash du bloc avec une fonction personnalisée."""
        chaine_bloc = (
            str(self.indice) +
            self.hash_precedent +
            str(self.horodatage) +
            self.donnees +
            str(self.preuve)
        )
        return self.hash_simple(chaine_bloc)

    @staticmethod
    def hash_simple(chaine_entree):
        """Fonction de hachage personnalisée (non cryptographique)."""
        valeur_hash = 0
        for caractere in chaine_entree:
            valeur_hash = (valeur_hash * 31 + ord(caractere)) % (2 ** 32)
        return format(valeur_hash, '08x')

class Blockchain:
    def __init__(self, debug=True):
        self.debug = debug
        if self.debug:
            print("Initialisation de la chaîne de blocs...")
        self.chaine = [self.creer_bloc_genese()]
        self.difficulte = 0  # Réduire temporairement la difficulté pour les tests
        self.stockage_preuves = {0: 0}  # Stockage des preuves avec une preuve par défaut pour le bloc genèse

    def creer_bloc_genese(self):
        if self.debug:
            print("Création du bloc genèse...")
        return Bloc(0, "0", time.time(), "Bloc Genèse", 0)

    def obtenir_dernier_bloc(self):
        return self.chaine[-1]

    def ajouter_bloc(self, nouveau_bloc):
        if self.debug:
            print(f"Ajout du bloc {nouveau_bloc.indice}...")
        nouveau_bloc.hash = nouveau_bloc.calculer_hash()
        if self.preuve_valide(nouveau_bloc, nouveau_bloc.preuve):
            self.chaine.append(nouveau_bloc)
            self.stockage_preuves[nouveau_bloc.indice] = nouveau_bloc.preuve
            if self.debug:
                print(f"Bloc {nouveau_bloc.indice} ajouté avec succès.")
        else:
            print(f"Échec de la validation du bloc {nouveau_bloc.indice}.")

    def preuve_de_travail(self, bloc, limite_temps=15):
        if self.debug:
            print(f"Calcul de la preuve de travail pour le bloc {bloc.indice}...")
        bloc.preuve = 0
        temps_debut = time.time()
        iterations = 0
        while not self.preuve_valide(bloc, bloc.preuve):
            bloc.preuve += 10  # Augmentation par pas de 10 pour accélérer
            iterations += 1
            if time.time() - temps_debut > limite_temps:
                print(f"Nombre d'itérations effectuées : {iterations}")
                raise TimeoutError("Preuve de travail non trouvée dans le temps imparti.")
        if self.debug:
            print(f"Preuve de travail trouvée pour le bloc {bloc.indice}: {bloc.preuve} après {iterations} itérations.")
        return bloc.preuve

    def preuve_valide(self, bloc, preuve):
        bloc.preuve = preuve
        tentative_hash = bloc.calculer_hash()
        return tentative_hash[:self.difficulte] == "0" * self.difficulte

    def chaine_valide(self):
        if self.debug:
            print("Vérification de l'intégrité de la chaîne de blocs...")
        for i in range(1, len(self.chaine)):
            bloc_courant = self.chaine[i]
            bloc_precedent = self.chaine[i - 1]

            if bloc_courant.hash != bloc_courant.calculer_hash():
                print(f"Le hash du bloc {bloc_courant.indice} est invalide.")
                return False
            if bloc_courant.hash_precedent != bloc_precedent.hash:
                print(f"Le lien entre les blocs {bloc_precedent.indice} et {bloc_courant.indice} est invalide.")
                return False
        if self.debug:
            print("Chaîne de blocs valide.")
        return True

    def ajouter_donnees(self, donnees):
        if self.debug:
            print(f"Ajout des données : {donnees}")
        dernier_bloc = self.obtenir_dernier_bloc()
        nouveau_bloc = Bloc(
            indice=dernier_bloc.indice + 1,
            hash_precedent=dernier_bloc.hash,
            horodatage=time.time(),
            donnees=donnees,
            preuve=0
        )
        try:
            preuve = self.preuve_de_travail(nouveau_bloc)
            nouveau_bloc.preuve = preuve
            self.ajouter_bloc(nouveau_bloc)
        except TimeoutError as e:
            print(f"Erreur : {e}")

    def obtenir_preuve_pour_bloc(self, indice):
        return self.stockage_preuves.get(indice, None)

    def deposer_fichier(self, nom_fichier, contenu_fichier):
        """Ajoute un fichier au coffre-fort."""
        donnees = f"FICHIER:{nom_fichier}|CONTENU:{contenu_fichier}"
        self.ajouter_donnees(donnees)

    def recuperer_fichier(self, nom_fichier):
        """Récupère un fichier du coffre-fort."""
        for bloc in self.chaine:
            if bloc.donnees.startswith(f"FICHIER:{nom_fichier}"):
                contenu = bloc.donnees.split("|CONTENU:")[1]
                return contenu
        return None
     #ajout sun================================
    def sauvegarder_blockchain(self, chemin_fichier="blockchain.json"):
        """
        Sauvegarde la blockchain dans un fichier JSON.
        """
        try:
            with open(chemin_fichier, "w") as fichier:
                chaine_serialisee = [
                    {
                        "indice": bloc.indice,
                        "hash_precedent": bloc.hash_precedent,
                        "horodatage": bloc.horodatage,
                        "donnees": bloc.donnees,
                        "preuve": bloc.preuve,
                        "hash": bloc.hash
                    }
                    for bloc in self.chaine
                ]
                json.dump(chaine_serialisee, fichier, indent=4)
            print(f"Blockchain sauvegardée dans {chemin_fichier}.")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la blockchain : {e}")

    @classmethod
    def charger_blockchain(cls, chemin_fichier="blockchain.json", debug=True):
        """
        Charge la blockchain depuis un fichier JSON.
        Si le fichier n'existe pas, initialise une nouvelle blockchain.
        """
        try:
            with open(chemin_fichier, "r") as fichier:
                chaine_serialisee = json.load(fichier)
            blockchain = cls(debug=debug)
            blockchain.chaine = [
                Bloc(
                    indice=bloc["indice"],
                    hash_precedent=bloc["hash_precedent"],
                    horodatage=bloc["horodatage"],
                    donnees=bloc["donnees"],
                    preuve=bloc["preuve"]
                )
                for bloc in chaine_serialisee
            ]
            print(f"Blockchain chargée depuis {chemin_fichier}.")
            return blockchain
        except FileNotFoundError:
            print(f"Fichier {chemin_fichier} introuvable. Création d'une nouvelle blockchain.")
            return cls(debug=debug)
        except Exception as e:
            print(f"Erreur lors du chargement de la blockchain : {e}")
            return cls(debug=debug)
        
    def ajouter_fichier_au_bloc(self, fichier_nom, contenu_fichier, utilisateur):
        """
        Ajoute un fichier au coffre-fort numérique en l'intégrant à la blockchain.
        """
        donnees = f"FICHIER:{fichier_nom}|UTILISATEUR:{utilisateur}|CONTENU:{contenu_fichier}"
        self.ajouter_donnees(donnees)
        print(f"Fichier '{fichier_nom}' ajouté à la blockchain par l'utilisateur '{utilisateur}'.")

'''
# Exemple d'utilisation
print("Démarrage du programme...")
blockchain = Blockchain(debug=True)
print("Chaîne de blocs initialisée avec le bloc genèse.")

try:
    # Dépôt de fichiers dans le coffre-fort
    blockchain.deposer_fichier("document1.txt", "Ceci est le contenu du fichier 1.")
    blockchain.deposer_fichier("document2.txt", "Ceci est le contenu du fichier 2.")

    # Récupération des fichiers
    contenu1 = blockchain.recuperer_fichier("document1.txt")
    contenu2 = blockchain.recuperer_fichier("document2.txt")

    print("\nFichiers récupérés depuis la chaîne de blocs :")
    print(f"document1.txt : {contenu1}")
    print(f"document2.txt : {contenu2}")

    if blockchain.chaine_valide():
        print("\nLa chaîne de blocs est valide.")

    print("\nAffichage des blocs dans la chaîne de blocs :")
    for bloc in blockchain.chaine:
        print(f"Indice: {bloc.indice}, Hash: {bloc.hash}, Hash précédent: {bloc.hash_precedent}, Données: {bloc.donnees}, Preuve: {bloc.preuve}")

except Exception as e:
    print(f"Erreur rencontrée : {e}")
'''