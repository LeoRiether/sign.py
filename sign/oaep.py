import secrets
from .util import bitwise_xor
from sha3 import sha3_256

def mgf1(input: bytes, size: int) -> bytes:
    res = bytearray()
    counter = 0
    while len(res) < size:
        counter_bytes = counter.to_bytes(16, 'big')
        res += sha3_256(input + counter_bytes).digest()
        counter += 1
    return bytes(res[:size])

K0 = K1 = 256 // 8

def mask(msg: bytes) -> bytes:
    padded = bytearray(msg.ljust(len(msg) + K1, b'\0'))
    rng = bytearray(secrets.randbits(K0 * 8).to_bytes(K0, 'big'))

    G = mgf1(rng, len(padded))
    bitwise_xor(padded, G)
    H = mgf1(padded, len(rng))
    bitwise_xor(rng, H)

    return bytes(padded + rng) 

def unmask(msg: bytes) -> bytes:
    padded, rng = bytearray(msg[:len(msg)-K0]), bytearray(msg[len(msg)-K0:])

    H = mgf1(padded, len(rng))
    bitwise_xor(rng, H)
    G = mgf1(rng, len(padded))
    bitwise_xor(padded, G)

    return bytes(padded[:len(padded)-K1])
