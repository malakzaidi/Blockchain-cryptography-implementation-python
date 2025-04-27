import hashlib
import time
import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def generate_key_pair():
    """Génère une paire de clés RSA (privée et publique)"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Convertir en format PEM pour stockage/transmission
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem, public_pem


def sign_data(private_key_pem, data):
    """Signe des données avec une clé privée"""
    # Charger la clé privée
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None
    )

    # Convertir les données en bytes si nécessaire
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')

    # Signer les données
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature


def verify_signature(public_key_pem, data, signature):
    """Vérifie une signature avec une clé publique"""
    # Charger la clé publique
    public_key = serialization.load_pem_public_key(public_key_pem)

    # Convertir les données en bytes si nécessaire
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')

    try:
        # Vérifier la signature
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def calculate_hash(data):
    """Calcule le hash SHA-256 de données"""
    # Convertir les données en bytes si nécessaire
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif not isinstance(data, bytes):
        data = json.dumps(data, sort_keys=True).encode('utf-8')

    return hashlib.sha256(data).hexdigest()


def get_timestamp():
    """Retourne l'horodatage actuel"""
    return int(time.time())