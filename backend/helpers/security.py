"""
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def load_public_key_from_pem(pem_data):
    return RSA.import_key(pem_data)

def load_private_key_from_pem(pem_data):
    return RSA.import_key(pem_data)

def verify_rsa_key_pair(public_key_pem, private_key_pem):
    public_key = load_public_key_from_pem(public_key_pem)
    private_key = load_private_key_from_pem(private_key_pem)

    if public_key.n != private_key.n:
        return False

    test_message = b"Test message for RSA key pair verification"

    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_msg = cipher_rsa.encrypt(test_message)
    
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_msg = cipher_rsa.decrypt(encrypted_msg)

    return decrypted_msg == test_message
"""
