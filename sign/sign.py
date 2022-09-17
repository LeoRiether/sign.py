from . import rsa, oaep, aes
from .util import bitsz, colors as C
from base64 import b64encode
from sha3 import sha3_512
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Cryptographically sign a document')
    parser.add_argument('-i', '--input', help='File you want to sign')
    parser.add_argument('-k', '--key', help='Output (secret) key file')
    return parser.parse_args()

def gen_keys():
    pk, sk, _ = rsa.gen_keys()
    key, nonce = aes.gen_key()
    return key, nonce, pk, sk

def read_input(file):
    if not file:
        return input().encode('utf-8')
    with open(file, 'br') as f:
        return f.read()

def get_aes(msg: bytes, key: bytes, nonce: int) -> bytes:
    msg1 = bytearray(msg)
    aes.encrypt_ctr(msg1, key, nonce)
    return bytes(msg1)

def get_rsa(msg: bytes, pk: rsa.PublicKey) -> bytes:
    masked = oaep.mask(msg)
    res = rsa.process(int.from_bytes(masked, 'big'), pk)
    return res.to_bytes(2048 // 8, 'big')

if __name__ == '__main__':
    args = parse_args()
    def log(a):
        sys.stderr.write(str(a))

    key, nonce, pk, sk = gen_keys()
    nonce_bytes = nonce.to_bytes(128 // 8, 'big')
    msg = read_input(args.input)
    aes_msg = get_aes(msg, key, nonce)
    hash = sha3_512(msg).digest()
    rsa_msg = get_rsa(hash + key + nonce_bytes, pk) # len(hash+key+nonce) == 96 bytes, 768 bits

    # Log some variable values
    logged_vars = "key nonce pk sk msg aes_msg hash rsa_msg".split()
    values = locals()
    for k in logged_vars:
        log(f"{k} = {values[k]} {C.cyan}({bitsz(values[k])} bits){C.reset}\n\n")

    if args.key:
        with open(args.key, 'wb') as f:
            n = int.to_bytes(sk.n, 2048 // 8, 'big')
            d = int.to_bytes(sk.d, 2048 // 8, 'big')
            f.write(b64encode(n) + b'\n' + b64encode(d))

    log(C.cyan + "output:".ljust(80, '-') + C.reset + '\n')
    print(b64encode(aes_msg).decode('utf-8'))
    print(b64encode(rsa_msg).decode('utf-8'))
    # print(b64encode(int.to_bytes(pk.n, 2048 // 8, 'big')).decode('utf-8'))
    log(C.cyan + '-' * 80 + C.reset + '\n')
    
