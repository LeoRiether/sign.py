from . import miller_rabin
from .arith import fastexp, modinverse
from base64 import b64encode, b64decode
from collections import namedtuple

KEY_SIZE = 1024 # bits
PublicKey = namedtuple("PrivateKey", ['n', 'e'])
SecretKey = namedtuple("SecretKey", ['n', 'd', 'p', 'q'])

def gen_keys(key_size=KEY_SIZE):
    p = miller_rabin.new_prime(key_size)
    q = miller_rabin.new_prime(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 1
    while phi % e == 0:
        e = miller_rabin.new_prime(16)
    d = modinverse(e, phi)
    return PublicKey(n, e), SecretKey(n, d, p, q), phi

def encrypt_block(m: int, pk: PublicKey):
    assert(m < pk.n)
    return fastexp(m, pk.e, pk.n)

def decrypt_block(m: int, sk: SecretKey):
    assert(m < sk.n)
    return fastexp(m, sk.d, sk.n)
