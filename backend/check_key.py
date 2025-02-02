from Crypto.PublicKey import RSA

def load_public_key_from_pem(pem_data):
    return RSA.import_key(pem_data)

def load_private_key_from_pem(pem_data):
    return RSA.import_key(pem_data)

def verify_rsa_key_pair(public_key_pem, private_key_pem):
    public_key = load_public_key_from_pem(public_key_pem)
    private_key = load_private_key_from_pem(private_key_pem)
    return public_key.n == private_key.n