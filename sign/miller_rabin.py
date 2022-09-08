import secrets
import multiprocessing
import os

from arith import fastexp

def randint(lo: int, hi: int):
    return lo + secrets.randbelow(hi - lo + 1)

def check_composite(n: int, a: int, q: int, s: int):
    x = fastexp(a, q, n)
    if x == 1 or x == n-1:
        return False
    for _ in range(1, s):
        x = x * x % n
        if x == n-1:
            return False
    return True

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

# Returns whether the Miller-Rabin primality test thinks an integer
# `n` is prime
def probably_prime(n: int, iterations=10):
    if n < 4:
        return n == 2 or n == 3

    if any(n % p == 0 for p in small_primes):
        return False
    
    # n-1 = 2^s × q, odd q
    s = 0
    q = n-1
    while q % 2 == 0:
        q >>= 1
        s += 1

    for _ in range(iterations):
        a = randint(2, n-2)
        if check_composite(n, a, q, s):
            return False

    return True

# Generates a random prime number with `bits` bits
# without any concurrency.
# Calls `when_found(prime)` when a prime is found
def new_prime_sync(bits: int, when_found=lambda x: x):
    seed = secrets.randbits(bits)
    if seed % 2 == 0: # seed should be odd
        seed += 1

    while True:
        if probably_prime(seed):
            when_found(seed)
            return
        seed += 2

def _new_prime_process(bits: int, flag, result):
    def when_found(prime):
        result.value = prime
        flag.set()
    new_prime_sync(bits, when_found)

# Generates a random prime number with `bits` bits.
# Does it concurrently
def new_prime(bits=1024):
    cpu_count = os.cpu_count() or 1
    with multiprocessing.Pool(cpu_count) as pool, multiprocessing.Manager() as manager:
        flag = manager.Event()
        result = manager.Value(int, 0)
        for _ in range(cpu_count):
            pool.apply_async(_new_prime_process, (bits, flag, result))

        pool.close()
        flag.wait()
        pool.terminate()

        return result.value

def primes(bits=1024):
    while True:
        yield new_prime(bits)

def benchmark(bits = [64, 128, 256, 512, 1024, 2048]):
    import time
    os.makedirs('data', exist_ok=True)
    for b in bits:
        print(f"b = {b}")
        data = []
        for _ in range(50):
            tic = time.perf_counter()
            new_prime(b)
            toc = time.perf_counter()
            data.append(toc - tic)
        
        with open(f'data/time.{b}.dat', 'w') as f:
            f.write(str.join('\n', map(str, data)))

if __name__ == '__main__':
    # benchmark()
    print(new_prime())


