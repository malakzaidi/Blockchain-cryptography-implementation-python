from utils.crypto_utils import calculate_hash, get_timestamp, verify_signature
import json


class Transaction:
    def __init__(self, sender, recipient, amount, signature=None, timestamp=None):
        """
        Initialise une nouvelle transaction

        Args:
            sender: Adresse publique de l'émetteur (clé publique en format PEM)
            recipient: Adresse publique du destinataire (clé publique en format PEM)
            amount: Montant de la transaction
            signature: Signature de la transaction (optionnel)
            timestamp: Horodatage de la transaction (optionnel)
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp if timestamp else get_timestamp()
        self.signature = signature

        # Validation des paramètres
        self._validate_parameters()

    def _validate_parameters(self):
        """Valide les paramètres de la transaction"""
        if not self.sender or not isinstance(self.sender, bytes):
            raise ValueError("L'émetteur doit être une clé publique valide")

        if not self.recipient or not isinstance(self.recipient, bytes):
            raise ValueError("Le destinataire doit être une clé publique valide")

        if not isinstance(self.amount, (int, float)) or self.amount <= 0:
            raise ValueError("Le montant doit être un nombre positif")

    def to_dict(self):
        """Convertit la transaction en dictionnaire"""
        return {
            "sender": self.sender.decode('utf-8') if isinstance(self.sender, bytes) else self.sender,
            "recipient": self.recipient.decode('utf-8') if isinstance(self.recipient, bytes) else self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

    def calculate_hash(self):
        """Calcule le hash de la transaction"""
        return calculate_hash(self.to_dict())

    def sign(self, private_key, signature_function):
        """
        Signe la transaction avec la clé privée de l'émetteur

        Args:
            private_key: Clé privée de l'émetteur
            signature_function: Fonction pour signer les données
        """
        if self.signature:
            raise ValueError("Cette transaction est déjà signée")

        self.signature = signature_function(private_key, self.to_dict())
        return self.signature

    def is_valid(self):
        """Vérifie si la transaction est valide"""
        # Si c'est une transaction de récompense (coinbase), pas besoin de signature
        if self.sender == "COINBASE":
            return True

        # Vérifier que la transaction a une signature
        if not self.signature:
            return False

        # Vérifier la signature
        return verify_signature(self.sender, self.to_dict(), self.signature)

    def __str__(self):
        """Représentation en chaîne de caractères de la transaction"""
        return f"Transaction(de={self.sender[:20]}..., à={self.recipient[:20]}..., montant={self.amount})"