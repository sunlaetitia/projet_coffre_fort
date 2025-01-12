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
        contenu = f"{self.indice}{self.hash_precedent}{self.horodatage}{self.donnees}{self.preuve}"
        return self.hash_simple(contenu)

    @staticmethod
    def hash_simple(chaine_entree):
        """Fonction de hachage personnalisée (non cryptographique)."""
        hash_value = 0
        prime = 31
        for i, char in enumerate(chaine_entree):
         hash_value += (ord(char) * (prime ** i)) % 10**8
        return str(hash_value % 10**8).zfill(8)

class Blockchain:
    def __init__(self, debug=True):
        self.debug = debug
        if self.debug:
            print("Initialisation de la chaîne de blocs...")
        self.chaine = [self.creer_bloc_genese()]
        self.difficulte = 1  # Réduire temporairement la difficulté pour les tests
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
        
        p=0
        while not self.preuve_valide(bloc, bloc.preuve):

            p+=1
            bloc.preuve += 2*p*p
            iterations += 1
            if iterations % 100000 == 0:
                print(f"Progression : {iterations} itérations, Preuve : {bloc.preuve}, Hash : {bloc.calculer_hash()}")
            if time.time() - temps_debut > limite_temps:
                print(f"Nombre d'itérations effectuées : {iterations}")
                raise TimeoutError("Preuve de travail non trouvée dans le temps imparti.")
        
        if self.debug:
            print(f"Preuve trouvée pour le bloc {bloc.indice}: {bloc.preuve} après {iterations} itérations.")
        return bloc.preuve
    
    #
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
    
    def recuperer_preuve(self, chemin_fichier, indice_bloc):
    
     try:
         with open(chemin_fichier, "r") as fichier:
             chaine_serialisee = json.load(fichier)
             for bloc in chaine_serialisee:
                 if bloc["indice"] == indice_bloc:
                    return bloc["preuve"]
             print(f"Bloc avec l'indice {indice_bloc} introuvable dans la blockchain.")
             return None
     except FileNotFoundError:
         print(f"Fichier {chemin_fichier} introuvable.")
         return None
     except json.JSONDecodeError:
         print(f"Erreur de décodage JSON dans le fichier {chemin_fichier}.")
         return None
     except KeyError as e:
        print(f"Clé manquante dans les données JSON : {e}")
        return None
    
   


    def sauvegarder_blockchain(self, chemin_fichier):
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
    def charger_blockchain(cls, chemin_fichier, debug=True):
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

    


