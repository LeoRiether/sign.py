import sign.arith as arith
from random import randint
from math import gcd

def test_egcd():
    for _ in range(100):
        x = randint(1, 1000)
        y = randint(1, 1000)
        a, b, d = arith.egcd(x, y)
        assert a*x + b*y == d
        assert d == gcd(x, y)

def test_modinverse():
    for _ in range(20):
        x = randint(1, 1000)
        m = randint(1, 1000)
        while gcd(x, m) != 1:
            m += 1
        y = arith.modinverse(x, m)
        assert 0 <= y < m
        assert x * y % m == 1
