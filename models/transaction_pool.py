class TransactionPool:
    def __init__(self):
        """Initialise un nouveau pool de transactions"""
        self.pending_transactions = []

    def add_transaction(self, transaction):
        """
        Ajoute une transaction au pool après validation

        Args:
            transaction: Transaction à ajouter au pool

        Returns:
            bool: True si la transaction a été ajoutée, False sinon
        """
        # Vérifier si la transaction est valide
        if not transaction.is_valid():
            raise ValueError("Impossible d'ajouter une transaction non valide au pool")

        # Vérifier si la transaction existe déjà dans le pool
        for tx in self.pending_transactions:
            if tx.calculate_hash() == transaction.calculate_hash():
                return False

        # Ajouter la transaction au pool
        self.pending_transactions.append(transaction)
        return True

    def clear_transactions(self, transactions):
        """
        Supprime les transactions spécifiées du pool

        Args:
            transactions: Liste des transactions à supprimer
        """
        transaction_hashes = [tx.calculate_hash() for tx in transactions]
        self.pending_transactions = [tx for tx in self.pending_transactions
                                     if tx.calculate_hash() not in transaction_hashes]

    def get_transactions(self, max_count=10):
        """
        Récupère un nombre limité de transactions du pool

        Args:
            max_count: Nombre maximum de transactions à récupérer

        Returns:
            Liste des transactions à traiter
        """
        return self.pending_transactions[:max_count]

    def transaction_exists(self, transaction_hash):
        """
        Vérifie si une transaction existe dans le pool

        Args:
            transaction_hash: Hash de la transaction à vérifier

        Returns:
            bool: True si la transaction existe, False sinon
        """
        for tx in self.pending_transactions:
            if tx.calculate_hash() == transaction_hash:
                return True
        return False

    def get_transaction_count(self):
        """
        Retourne le nombre de transactions dans le pool

        Returns:
            int: Nombre de transactions en attente
        """
        return len(self.pending_transactions)

    def __str__(self):
        """Représentation en chaîne de caractères du pool de transactions"""
        return f"TransactionPool({self.get_transaction_count()} transactions en attente)"