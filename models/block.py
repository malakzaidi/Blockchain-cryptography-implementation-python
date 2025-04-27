from utils.crypto_utils import calculate_hash, get_timestamp
import json


class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        """
        Initialise un nouveau bloc

        Args:
            index: Position du bloc dans la chaîne
            previous_hash: Hash du bloc précédent
            transactions: Liste des transactions incluses dans le bloc
            timestamp: Horodatage du bloc (optionnel)
            nonce: Valeur utilisée pour le minage (optionnel)
        """
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp if timestamp else get_timestamp()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def to_dict(self):
        """Convertit le bloc en dictionnaire"""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "transactions": [tx.to_dict() for tx in self.transactions]
        }

    def calculate_hash(self):
        """Calcule le hash du bloc"""
        block_dict = self.to_dict()
        return calculate_hash(block_dict)

    def mine_block(self, difficulty):
        """
        Mine le bloc avec la difficulté spécifiée

        Args:
            difficulty: Nombre de zéros en début de hash requis

        Returns:
            Le hash du bloc miné
        """
        target = "0" * difficulty

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Bloc miné! Hash: {self.hash}")
        return self.hash

    def has_valid_transactions(self):
        """Vérifie si toutes les transactions du bloc sont valides"""
        return all(tx.is_valid() for tx in self.transactions)

    def __str__(self):
        """Représentation en chaîne de caractères du bloc"""
        return f"Block(index={self.index}, hash={self.hash[:10]}..., {len(self.transactions)} transactions)"