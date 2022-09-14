from . import rsa, oaep, aes
from .sign import get_aes
from .util import bitsz
from base64 import b64decode
from sha3 import sha3_512
import argparse
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Verify a criptographically signed document')
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-k', '--key', help='Secret key file', required=True)
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Shows more stuff')
    return parser.parse_args()

def read_input(file):
    if not file:
        return input().encode('utf-8'), input().encode('utf-8')
    with open(file, 'br') as f:
        aes_msg = b64decode(f.readline())
        rsa_msg = b64decode(f.readline())
        return aes_msg, rsa_msg

def read_key(file):
    with open(file, 'rb') as f:
        n = int.from_bytes(b64decode(f.readline()), 'big')
        d = int.from_bytes(b64decode(f.readline()), 'big')
        return rsa.SecretKey(n, d)

def get_rsa(msg: bytes, sk: rsa.SecretKey) -> tuple[bytes, bytes, bytes]:
    rsa_res = rsa.process(int.from_bytes(msg, 'big'), sk)
    res = oaep.unmask(rsa_res.to_bytes(96 + 64, 'big'))
    return res[:64], res[64:80], res[80:] # hash, key, nonce

if __name__ == '__main__':
    args = parse_args()
    def log(a):
        if args.verbose:
            sys.stderr.write(str(a))

    sk = read_key(args.key)
    aes_msg, rsa_msg = read_input(args.input)
    hash, key, nonce_bytes = get_rsa(rsa_msg, sk)
    nonce = int.from_bytes(nonce_bytes, 'big')
    msg = get_aes(aes_msg, key, nonce)
    hash = sha3_512(msg).digest()

    # Log some variable values
    logged_vars = "key nonce sk msg aes_msg hash rsa_msg".split()
    values = locals()
    for k in logged_vars:
        log(f"{k} = {values[k]} ({bitsz(values[k])} bits)\n\n")

    log("message:".ljust(80, '-') + '\n')
    print(msg)
    log('-' * 80 + '\n')

