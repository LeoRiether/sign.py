from base64 import b64encode
import argparse
import hashlib
import sha3 # monkey patches hashlib...
import rsa
import struct
import sys

def parse_args():
    parser = argparse.ArgumentParser(description='Cryptographically sign a document')
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Shows more stuff')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    def log(a):
        if args.verbose:
            sys.stderr.write(str(a))

    # Hash input file
    sha = hashlib.sha3_512()
    if args.input:
        with open(args.input, 'br') as f:
            sha.update(f.read())
    else:
        sha.update(input().encode('utf-8'))
    
    # Generate digest and interpret as integer
    digest = sha.digest()
    digest_as_int = 0
    for byte in digest:
        digest_as_int *= 256
        digest_as_int += int(byte)

    log(f"hexdigest = {sha.hexdigest()}\n\n")
    log(f"digest_as_int = {digest_as_int}\n\n")

    # Encrypt SHA3 sum using RSA 
    pk, sk, _ = rsa.gen_keys()
    log(f'{sk}\n\n')

    C = rsa.process(digest_as_int, sk)
    print(f"{pk}\n")
    print(f"C = <{C}>\n")

    log(f"Decoded message = <{rsa.process(C, pk)}>\n\n")


