# Computes (x ** e) % mod in O(log e × log x)
def fastexp(x: int, e: int, mod: int):
    ans = 1
    x %= mod
    while e > 0:
        if (e & 1) == 1:
            ans = ans * x % mod
        x = x * x % mod
        e >>= 1
    return ans
