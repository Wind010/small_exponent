from cryptography.hazmat.primitives.asymmetric import rsa

def generate_large_prime(bits, e=65537):
    return rsa.generate_private_key(
        public_exponent=e,
        key_size=bits
    ).private_numbers().p

# Size of each prime in bits
prime_bits = 1024

# Generate primes p and q
p = generate_large_prime(prime_bits)
q = generate_large_prime(prime_bits)

# Calculate n
n = p * q

# Output n
print(f"p: {p}")
print(f"q: {q}")
print(f"n: {n}")
print(f"Bit length of n: {n.bit_length()}")