from hashlib import sha1, sha256
from random import randint
from sha3 import sha3_256
import secrets
import sign.oaep as oaep

def test_oaep_inversibility():
    for _ in range(100):
        data = secrets.token_bytes(512 // 8)
        
        output = oaep.mask(data)
        assert len(output) == len(data) + oaep.K0 + oaep.K1

        input = oaep.unmask(output)
        assert input == data

# Doesn't use s.copy()
def less_efficient_mgf1(input: bytes, size: int) -> bytes:
    """
        Mask Generation Function 1
        Uses sha3_256 as the primitive hash function
        Returns `size` bytes
    """
    res = bytearray()
    counter = 0
    while len(res) < size:
        counter_bytes = counter.to_bytes(4, 'big')
        res += sha3_256(input + counter_bytes).digest()
        counter += 1
    return bytes(res[:size])

def test_efficient_mgf1():
    for _ in range(20):
        data = secrets.token_bytes(512 // 8)
        output = oaep.mgf1(data, 1024)
        expected = less_efficient_mgf1(data, 1024)
        assert output == expected

def test_wikipedia_mgf1():
    testcases = [
        (oaep.mgf1(b'bar', 50, hasher=sha256).hex(),
        '382576a7841021cc28fc4c0948753fb8312090cea942ea4c4e735d10dc724b155f9f6069f289d61daca0cb814502ef04eae1'),
        (oaep.mgf1(b'foo', 5, hasher=sha1).hex(),
        '1ac9075cd4')
    ]

    for (output, expected) in testcases:
        assert output == expected
