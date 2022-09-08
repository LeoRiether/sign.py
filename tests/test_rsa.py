from random import randint
import sign.rsa as rsa

pk, sk, phi = rsa.gen_keys()

def test_genkey():
    assert pk.n == sk.n
    assert pk.e * sk.d % phi == 1

def test_inversibility():
    for _ in range(10):
        pk0, sk0, _ = rsa.gen_keys(512)
        data = randint(10, 100000)
        e = rsa.process(data, pk0)
        d = rsa.process(e, sk0)
        assert d == data, str(sk0)
