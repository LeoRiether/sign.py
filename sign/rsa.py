import miller_rabin
from arith import fastexp, modinverse
from collections import namedtuple

KEY_LEN = 1024 # bits
PublicKey = namedtuple("PublicKey", ['n', 'e'])
SecretKey = namedtuple("SecretKey", ['n', 'd'])

def gen_keys(key_size=KEY_LEN):
    p = miller_rabin.new_prime(key_size)
    q = miller_rabin.new_prime(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 1
    while phi % e == 0:
        e = miller_rabin.new_prime(16)
    d = modinverse(e, phi)
    return PublicKey(n, e), SecretKey(n, d), phi

def process(m: int, key: PublicKey | SecretKey):
    assert(m < key.n)
    return fastexp(m, key[1], key.n)

