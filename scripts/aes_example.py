import sign.aes as aes
import secrets

data = bytearray(b'Helloooo Woooooorld!!!!!!!!!')
key = secrets.randbits(128).to_bytes(16, 'big')

aes.encrypt_ctr(data, key, nonce=1)
print(data)



