from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends.openssl.backend import backend as openssl_backend


def generate_ssh_key(passphrase=None, key_size=4096):
    key = rsa.generate_private_key(
        backend=openssl_backend,
        public_exponent=65537,
        key_size=key_size
    )

    encryption = crypto_serialization.BestAvailableEncryption(passphrase.encode('utf-8')) if passphrase \
        else crypto_serialization.NoEncryption()

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        encryption
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

    return public_key.decode('utf-8'), private_key.decode('utf-8')