from models.block import Block
from models.transaction import Transaction
from utils.crypto_utils import get_timestamp
import json


class Blockchain:
    def __init__(self, difficulty=4):
        """
        Initialise une nouvelle blockchain

        Args:
            difficulty: Difficulté de minage (nombre de zéros requis)
        """
        self.chain = []
        self.difficulty = difficulty

        # Créer le bloc genesis
        self.create_genesis_block()

    def create_genesis_block(self):
        """Crée le bloc genesis (premier bloc de la chaîne)"""
        # Créer une transaction coinbase pour le bloc genesis
        coinbase_tx = Transaction("COINBASE", "GENESIS", 50)

        # Créer le bloc genesis
        genesis_block = Block(0, "0", [coinbase_tx], get_timestamp())
        genesis_block.hash = genesis_block.calculate_hash()

        # Ajouter le bloc à la chaîne
        self.chain.append(genesis_block)

    def get_latest_block(self):
        """Récupère le dernier bloc de la chaîne"""
        return self.chain[-1]

    def add_block(self, transactions):
        """
        Crée et ajoute un nouveau bloc à la chaîne

        Args:
            transactions: Liste des transactions à inclure dans le bloc

        Returns:
            Le bloc ajouté
        """
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            previous_hash=latest_block.hash,
            transactions=transactions
        )

        # Miner le bloc
        new_block.mine_block(self.difficulty)

        # Ajouter le bloc à la chaîne
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """
        Vérifie l'intégrité de la chaîne

        Returns:
            bool: True si la chaîne est valide, False sinon
        """
        # Parcourir tous les blocs de la chaîne (sauf le bloc genesis)
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Vérifier si le hash du bloc est valide
            if current_block.hash != current_block.calculate_hash():
                print(f"Hash invalide pour le bloc {current_block.index}")
                return False

            # Vérifier si le lien avec le bloc précédent est valide
            if current_block.previous_hash != previous_block.hash:
                print(f"Lien invalide pour le bloc {current_block.index}")
                return False

            # Vérifier si toutes les transactions du bloc sont valides
            if not current_block.has_valid_transactions():
                print(f"Transactions invalides pour le bloc {current_block.index}")
                return False

        return True

    def adjust_difficulty(self):
        """
        Ajuste la difficulté de minage en fonction du temps moyen de bloc
        Note: Cette méthode est simplifiée pour le TP
        """
        # Cette méthode pourrait être implémentée pour ajuster la difficulté
        # en fonction du temps de minage des blocs récents
        pass

    def get_balance(self, address):
        """
        Calcule le solde d'une adresse (clé publique)

        Args:
            address: Adresse dont on veut calculer le solde

        Returns:
            float: Solde de l'adresse
        """
        balance = 0

        # Parcourir tous les blocs de la chaîne
        for block in self.chain:
            # Parcourir toutes les transactions du bloc
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount

        return balance

    def __str__(self):
        """Représentation en chaîne de caractères de la blockchain"""
        return f"Blockchain({len(self.chain)} blocs, difficulté={self.difficulty})"