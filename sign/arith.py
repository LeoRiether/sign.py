def fastexp(x: int, e: int, mod: int) -> int:
    """ Computes (x ** e) % mod in O(log e × log x) """
    ans = 1
    x %= mod
    while e > 0:
        if (e & 1) == 1:
            ans = ans * x % mod
        x = x * x % mod
        e >>= 1
    return ans

def egcd(x: int, y: int) -> tuple[int, int, int]:
    """
        Extended Euclidean Algorithm
        Returns (a, b, d) such that ax + bd = d,
        and d = gcd(x, y)
    """
    if y == 0:
        return 1, 0, x
    q, r = divmod(x, y)
    a, b, d = egcd(y, r)
    return (b, a-b*q, d)

def modinverse(x: int, m: int) -> int:
    """ Finds the inverse of `x` mod `m` """
    y, _, d = egcd(x, m)
    if d != 1:
        raise BaseException("modinverse called with non-coprime arguments!")
    return y % m

    
