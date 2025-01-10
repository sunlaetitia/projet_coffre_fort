import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calcule le hash du bloc avec une fonction personnalisée."""
        block_string = (
            str(self.index) +
            self.previous_hash +
            str(self.timestamp) +
            self.data +
            str(self.proof)
        )
        return self.simple_hash(block_string)

    @staticmethod

    def simple_hash(input_string):
        """Fonction de hachage personnalisée (non cryptographique)."""
        hash_value = 0
        for char in input_string:
            hash_value = (hash_value * 31 + ord(char)) % (2 ** 32)
        return format(hash_value, '08x')

class Blockchain:
    def __init__(self, debug=True):
        self.debug = debug
        if self.debug:
            print("Initialisation de la blockchain...")
        self.chain = [self.create_genesis_block()]
        self.difficulty = 0  # Réduire temporairement la difficulté pour les tests
        self.proof_storage = {0: 0}  # Stockage des preuves de travail avec une preuve par défaut pour le bloc genesis

    def create_genesis_block(self):
        if self.debug:
            print("Création du bloc genesis...")
        return Block(0, "0", time.time(), "Genesis Block", 0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        if self.debug:
            print(f"Ajout du bloc {new_block.index}...")
        new_block.hash = new_block.calculate_hash()
        if self.is_valid_proof(new_block, new_block.proof):
            self.chain.append(new_block)
            self.proof_storage[new_block.index] = new_block.proof
            if self.debug:
                print(f"Bloc {new_block.index} ajouté avec succès.")
        else:
            print(f"Échec de la validation du bloc {new_block.index}.")

    def proof_of_work(self, block, time_limit=15):
        if self.debug:
            print(f"Calcul de la preuve de travail pour le bloc {block.index}...")
        block.proof = 0
        start_time = time.time()
        iterations = 0
        while not self.is_valid_proof(block, block.proof):
            block.proof += 10  # Augmentation par pas de 10 pour accélérer
            iterations += 1
            if time.time() - start_time > time_limit:
                print(f"Nombre d'itérations effectuées : {iterations}")
                raise TimeoutError("Preuve de travail non trouvée dans le temps imparti.")
        if self.debug:
            print(f"Preuve de travail trouvée pour le bloc {block.index}: {block.proof} après {iterations} itérations.")
        return block.proof

    def is_valid_proof(self, block, proof):
        block.proof = proof
        hash_attempt = block.calculate_hash()
        return hash_attempt[:self.difficulty] == "0" * self.difficulty

    def is_chain_valid(self):
        if self.debug:
            print("Vérification de l'intégrité de la blockchain...")
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                print(f"Le hash du bloc {current_block.index} est invalide.")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Le lien entre les blocs {previous_block.index} et {current_block.index} est invalide.")
                return False
        if self.debug:
            print("Blockchain valide.")
        return True

    def add_data(self, data):
        if self.debug:
            print(f"Ajout des données : {data}")
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            timestamp=time.time(),
            data=data,
            proof=0
        )
        try:
            proof = self.proof_of_work(new_block)
            new_block.proof = proof
            self.add_block(new_block)
        except TimeoutError as e:
            print(f"Erreur : {e}")

    def get_proof_for_block(self, index):
        return self.proof_storage.get(index, None)

# Exemple d'utilisation
print("Démarrage du programme...")
blockchain = Blockchain(debug=True)
print("Blockchain initialisée avec le bloc genesis.")

try:
    blockchain.add_data("Données sensibles 1")
    blockchain.add_data("Données sensibles 2")
    blockchain.add_data("Données sensibles 3")
    blockchain.add_data("Données sensibles 4")

    if blockchain.is_chain_valid():
        print("La blockchain est valide.")

    print("Affichage des blocs dans la blockchain :")
    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Data: {block.data}, Proof: {block.proof}")

    print("\nRécupération des preuves de travail :")
    for i in range(len(blockchain.chain)):
        proof = blockchain.get_proof_for_block(i)
        if proof is not None:
            print(f"Preuve de travail pour le bloc {i}: {proof}")
        else:
            print(f"Aucune preuve de travail trouvée pour le bloc {i}.")

except Exception as e:
    print(f"Erreur rencontrée : {e}")
