from random import randint
import sign.miller_rabin as mr

def is_prime(x):
    if x == 1:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True

def test_primes():
    for _ in range(1000):
        x = randint(1, 10_000)
        assert mr.probably_prime(x) == is_prime(x)
