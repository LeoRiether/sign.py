import secrets
import multiprocessing
import os

def randint(lo, hi):
    return lo + secrets.randbelow(hi - lo + 1)

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

def check_composite(n, a, q, s):
    x = fastexp(a, q, n)
    if x == 1 or x == n-1:
        return False
    for r in range(1, s):
        x = x * x % n
        if x == n-1:
            return False
    return True

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

# Returns whether the Miller-Rabin primality test thinks an integer
# `n` is prime
def probably_prime(n, iterations=10):
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
def new_prime_sync(bits, when_found=lambda x: x):
    seed = randint(0, 2**bits - 1)
    if seed % 2 == 0: # seed should be odd
        seed += 1

    while True:
        if probably_prime(seed):
            when_found(seed)
            return
        seed += 2

def _new_prime_process(bits, flag, result):
    def when_found(prime):
        result.value = prime
        flag.set()
    new_prime_sync(bits, when_found)

# Generates a random prime number with `bits` bits.
# Does it concurrently
def new_prime(bits=1024):
    with multiprocessing.Pool() as pool, multiprocessing.Manager() as manager:
        flag = manager.Event()
        result = manager.Value(int, 0)
        for _ in range(pool._processes):
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
        for i in range(50):
            tic = time.perf_counter()
            p = new_prime(b)
            toc = time.perf_counter()
            data.append(toc - tic)
        
        with open(f'data/time.{b}.dat', 'w') as f:
            f.write(str.join('\n', map(str, data)))

if __name__ == '__main__':
    # benchmark()
    print(new_prime())

