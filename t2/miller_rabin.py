from random import randint
import multiprocessing
import os

# Computes (x ** e) % mod in O(log e × log x)
def fastexp(x, e, mod):
    ans = 1
    x %= mod
    while e > 0:
        if (e & 1) == 1:
            ans = ans * x % mod
        x = x * x % mod
        e >>= 1
    return ans

def check_composite(n, a, d, s):
    x = fastexp(a, d, n)
    if x == 1 or x == n-1:
        return False
    for r in range(1, s):
        x = x * x % n
        if x == n-1:
            return False
    return True

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
def miller_rabin(n, iterations=10):
    if n < 4:
        return n == 2 or n == 3

    s = 0
    d = n-1
    while d % 2 == 0:
        d >>= 1
        s += 1

    for p in small_primes:
        if n % p == 0:
            return False

    for _ in range(iterations):
        a = randint(2, n-2)
        if check_composite(n, a, d, s):
            return False

    return True

def new_prime_sync(bits, flag, result):
    seed = randint(0, 2**bits - 1)
    if seed % 2 == 0: # seed should be odd
        seed += 1

    while True:
        if miller_rabin(seed):
            result.value = seed
            flag.set()
        seed += 2

# Generates a random prime number with 1024 bits
def new_prime(bits=2096):
    with multiprocessing.Pool() as pool:
        manager = multiprocessing.Manager()
        flag = manager.Event()
        result = manager.Value(int, 0)
        for _ in range(pool._processes):
            pool.apply_async(new_prime_sync, (bits, flag, result))

        pool.close()
        flag.wait()
        pool.terminate()

    return result.value

def primes():
    while True:
        yield new_prime()

if __name__ == '__main__':
    print(new_prime())
