from phe import paillier

# Generate keys (for demo — in production, securely manage these)
public_key, private_key = paillier.generate_paillier_keypair()

def encrypt_column(column):
    return [public_key.encrypt(float(x)) for x in column]

def encrypt_row(row):
    return [public_key.encrypt(float(x)) for x in row]

def decrypt_column(column):
    return [private_key.decrypt(x) for x in column]

def decrypt_single(value):
    return private_key.decrypt(value)
