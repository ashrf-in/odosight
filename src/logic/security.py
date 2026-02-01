import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_key(passphrase: str, salt: bytes):
    """Generate a cryptographic key from a passphrase and salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    return key

def encrypt_data(data: str, passphrase: str):
    """Encrypt data using a passphrase."""
    salt = os.urandom(16)
    key = generate_key(passphrase, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    # Return salt + encrypted data combined
    return base64.b64encode(salt + encrypted_data).decode()

def decrypt_data(token: str, passphrase: str):
    """Decrypt data using a passphrase."""
    try:
        decoded = base64.b64decode(token)
        salt = decoded[:16]
        encrypted_data = decoded[16:]
        key = generate_key(passphrase, salt)
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
    except Exception:
        return None
