### Small Exponent

Code to factor and exploit the cipher text or private key based off small exponent used with RSA.  Seen a challenge in [picoCTF](https://picoctf.org/)

### Usage for `reconstruct_private_key.py`

Generate public and private key from `p` and `q` from factored `n` and small `e`:
```sh
python ./reconstruct_private_key.py --n 631371953793368771804570727896887140714495090919073481680274581226742748040342637
```

Use [FactorDB](https://factordb.com/) instead of SymPy:
```sh
python ./reconstruct_private_key.py --n 631371953793368771804570727896887140714495090919073481680274581226742748040342637 --use_factor_db
```

Generate a `JWT` with the private key with payload (hardcoded):
```sh
python ./reconstruct_private_key.py --n 631371953793368771804570727896887140714495090919073481680274581226742748040342637 --jwt
```


### Mind your Ps and Qs

In RSA, a small `e` value can be problematic, but what about `N`? Can you decrypt this? [values](https://mercury.picoctf.net/static/bf5e2c8811afb4669f4a6850e097e8aa/values)

```sh
Decrypt my super sick RSA:
c: 421345306292040663864066688931456845278496274597031632020995583473619804626233684
n: 631371953793368771804570727896887140714495090919073481680274581226742748040342637
e: 65537
```


Semi-Prime:  Numbers whose factors are prime numbers.  Factors of semi prime 21 is 1, 3 7, 21.  The product of two semi primes is always a semi prime.

RSA works by generating two prime numbers denoted as `p` and `q`.
1.  Calculate the `product` by multiply them together:  
	1. $p*q = n$ 
	2. $7*19 = 133$
2.  Calculate the `Totient`:
	1. $(p-1)*(q-1) = t$
	2. $6*18 = 108$
3. Select a `Public Key`, denoted as `e`:
	1. Must be a prime.
	2. Must be less than the totient.
	3. Must NOT be a factor of the totient. 
		1. This can be determined by taking the totient and taking the modulus of it with the public key:  $(p-1)*(q-1)\mod e$
		2. If you get a `0` then it's a factor of `e`.  If `e` was `3` it wouldn't work, but `5` would.
4. Select a `Private Key`, denoted as `d`:
	1. Product of `d` and `e`, divided by `t` must result in a remainder of 1:  $(d*e) \mod t = 1$

Once we have these values we can encrypt and decrypt a message.  Where `m` is plaintext message and `c` is ciphertext.
* Encryption:
	* $m^{e}\mod n = c$
* Decryption:
	* $ciphertext^{d} \mod n = m$


### Determine if number is `prime`:
```python
def first_prime_factor(n):
    if n & 1 == 0:
        return 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return d
        d = d + 2
    return n

def is_prime(n):
    return first_prime_factor == n


import sympy
sympy.isprime(n)
```


You can use this site to factor the product (n) to find `p` and `q`:
https://www.alpertron.com.ar/ECM.HTM

Straight up decode using:
https://www.dcode.fr/rsa-cipher
https://github.com/RsaCtfTool/RsaCtfTool

The inverse function:
https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm

Interesting to note that the textbook algorithm for RSA generates the same ciphertext because since there is no random number used.  
https://crypto.stackexchange.com/questions/101443/rsa-different-ciphertext-for-the-same-plaintext#:~:text=To%20ensure%20that%20every%20encryption,is%20the%20only%20practical%20choice.

https://stackoverflow.com/questions/33579782/java-rsa-why-different-cipher-text-every-time

