import sign.aes as aes
import secrets

with open('requirements.txt', 'rb') as f:
    key = secrets.randbits(128).to_bytes(16, 'big')
    nonce = secrets.randbits(128)
    g = aes.stream_ctr(f, key, nonce)
    print(bytes.join(b'', g).hex())

