from . import rsa
from functools import wraps

def bitwise_xor(x: bytearray, y: bytes):
    """ Does x[i] := x[i] ^ y[i] for every byte in x """
    assert len(x) == len(y)
    for i in range(len(x)):
        x[i] ^= y[i]

def bitsz(x):
    """ How many bits does it take to represent `x` in memory? """
    from math import log2, ceil
    if isinstance(x, int):
        return int(ceil(log2(x)))
    if isinstance(x, rsa.PublicKey) or isinstance(x, rsa.SecretKey):
        return int(ceil(log2(x.n)))
    return len(x) * 8

def once(f):
    """
        Used as a decorator to make a function run only once
        Ex:
            @once
            def build_sbox():
                print("I shall build this sbox")
                # *code that builds the sbox*
                return

            # This should only print "I shall build this sbox" once!
            build_sbox()
            build_sbox()
            build_sbox()
            build_sbox()
    """
    ran = False
    ret = None

    @wraps(f)
    def f_once(*args, **kwargs):
        nonlocal ran, ret
        if not ran:
            ran = True
            ret = f(*args, **kwargs)
        return ret 

    return f_once

