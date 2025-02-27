#!/usr/bin/python3

from factordb.factordb import FactorDB
#import gmpy2

c = 421345306292040663864066688931456845278496274597031632020995583473619804626233684
n = 631371953793368771804570727896887140714495090919073481680274581226742748040342637
e = 65537

def decrypt(ciphertext, e, n) -> str:
    f = FactorDB(n)
    f.connect()
    
    factors = f.get_factor_list() 
    
    # Debug information 
    print(f"Factors from FactorDB: {factors}")

    if len(factors) != 2: 
        raise ValueError(f"Failed to get exactly two prime factors for n from FactorDB. {factors}")

    p, q = factors

    ph = (p-1)*(q-1)
    #d = gmpy2.invert(e, ph)
    d = pow(e, -1, ph)
    plaintext = pow(ciphertext, d, n)
    return f"{bytearray.fromhex(format(plaintext, 'x')).decode()}"

def encrypt(plaintext, e, n) -> int:
    bytes_representation = plaintext.encode()
    hex_representation = bytes_representation.hex()
    int_bytes = int(hex_representation, 16)
    cipher_text = pow(int_bytes, e, n)
    return cipher_text

def decrypt(ciphertext, e, p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d = pow(e, -1, phi_n)
    
    plaintext_int = pow(ciphertext, d, n)

    # Convert the plaintext integer to a byte array and then decode to string
    plaintext_hex = format(plaintext_int, 'x')
    if len(plaintext_hex) % 2:  # Ensure even number of hex digits
        plaintext_hex = '0' + plaintext_hex
    plaintext = bytearray.fromhex(plaintext_hex).decode()

    return plaintext


plaintext = decrypt(c, e, n)
print(f"Flag: {plaintext}")
