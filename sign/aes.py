from . import galois_field as gf
from .util import once, bitwise_xor
import secrets

def gen_key(bits: int = 128):
    key = secrets.token_bytes(bits // 8)
    nonce = secrets.randbits(128)
    return key, nonce

################################################################################
#                                  Sub Bytes {{{                               #
################################################################################
def build_sbox(s):
    """ Split the string and parse hexadecimal integers """
    return list(map(lambda x: int(x, 16), s.split()))

def invert(sbox):
    """ Compute the inverse SBOX """
    inv = [0] * 256
    for i in range(256):
        inv[sbox[i]] = i
    return inv

SBOX = build_sbox("""
63	7c	77	7b	f2	6b	6f	c5	30	01	67	2b	fe	d7	ab	76
ca	82	c9	7d	fa	59	47	f0	ad	d4	a2	af	9c	a4	72	c0
b7	fd	93	26	36	3f	f7	cc	34	a5	e5	f1	71	d8	31	15
04	c7	23	c3	18	96	05	9a	07	12	80	e2	eb	27	b2	75
09	83	2c	1a	1b	6e	5a	a0	52	3b	d6	b3	29	e3	2f	84
53	d1	00	ed	20	fc	b1	5b	6a	cb	be	39	4a	4c	58	cf
d0	ef	aa	fb	43	4d	33	85	45	f9	02	7f	50	3c	9f	a8
51	a3	40	8f	92	9d	38	f5	bc	b6	da	21	10	ff	f3	d2
cd	0c	13	ec	5f	97	44	17	c4	a7	7e	3d	64	5d	19	73
60	81	4f	dc	22	2a	90	88	46	ee	b8	14	de	5e	0b	db
e0	32	3a	0a	49	06	24	5c	c2	d3	ac	62	91	95	e4	79
e7	c8	37	6d	8d	d5	4e	a9	6c	56	f4	ea	65	7a	ae	08
ba	78	25	2e	1c	a6	b4	c6	e8	dd	74	1f	4b	bd	8b	8a
70	3e	b5	66	48	03	f6	0e	61	35	57	b9	86	c1	1d	9e
e1	f8	98	11	69	d9	8e	94	9b	1e	87	e9	ce	55	28	df
8c	a1	89	0d	bf	e6	42	68	41	99	2d	0f	b0	54	bb	16
""")
INVSBOX = invert(SBOX)

def sub_bytes(block: bytearray):
    """ Confusion """
    for i in range(len(block)):
        block[i] = SBOX[block[i]]

def inv_sub_bytes(block: bytearray):
    """ Elucidation? """
    for i in range(len(block)):
        block[i] = INVSBOX[block[i]]

# }}}

################################################################################
#                                  Shift Rows {{{                              #
################################################################################
def shift_rows(x: bytearray):
    """ Diffusion """
    for i in range(1, 4):
        x[i], x[4+i], x[8+i], x[12+i] = \
            x[4*i+i], x[4*((i+1)%4)+i], x[4*((i+2)%4)+i], x[4*((i+3)%4)+i]

def inv_shift_rows(x: bytearray):
    """ Fusion? """
    for i in range(1, 4):
        x[4*i+i], x[4*((i+1)%4)+i], x[4*((i+2)%4)+i], x[4*((i+3)%4)+i] = \
            x[i], x[4+i], x[8+i], x[12+i]

# }}}

################################################################################
#                                 Mix Columns {{{                              #
################################################################################
MIX = [[2, 3, 1, 1],
       [1, 2, 3, 1],
       [1, 1, 2, 3],
       [3, 1, 1, 2]]
def mix_columns(x: bytearray):
    """ More diffusion """
    for i in range(0, 16, 4):
        x[i:i+4] = gf.matrix_mult(MIX, x[i:i+4])

INVMIX = [[14, 11, 13, 9],
          [9, 14, 11, 13],
          [13, 9, 14, 11],
          [11, 13, 9, 14]]
def inv_mix_columns(x: bytearray):
    """ More fusion? """
    for i in range(0, 16, 4):
        x[i:i+4] = gf.matrix_mult(INVMIX, x[i:i+4])

# }}}

################################################################################
#                                  Expand Key {{{                              #
################################################################################
def expand_key(key: bytes, rounds: int) -> bytes:
    """ Takes a 16-byte key and expands it to 16*(rounds+1) bytes """
    assert len(key) == 16
    exp = bytearray(16 * (rounds+1))

    # round constant
    rc = [0] * (rounds+1)
    rc[0] = 1
    for i in range(1, len(rc)):
        rc[i] = 2*rc[i-1]
        if rc[i-1] >= 0x80:
            rc[i] ^= 0x11b
    rc = bytearray(rc)

    for i in range(0, 16, 4):
        exp[i:i+4] = key[i:i+4]

    def sub(word):
        return bytearray(SBOX[b] for b in word)
    def rot(word):
        a,b,c,d = word
        return bytearray([b,c,d,a])

    for i in range(16, len(exp), 4):
        t = exp[i-4:i]
        if i % 16 == 0:
            t = sub(rot(t))
            t[0] ^= rc[i//16]

        for j in range(i, i+4):
            exp[j] ^= t[j-i]

    return bytes(exp)

# }}}

################################################################################
#                     Full Encription/Decription Procedure {{{                 #
################################################################################
def encrypt_block(block: bytearray, key: bytes, rounds: int = 10):
    """ Encrypts a 16-byte block with AES """
    assert len(block) == 16
    assert len(key) == 16

    expkey = expand_key(key, rounds)
    bitwise_xor(block, expkey[:16])
    for i in range(1, rounds+1):
        sub_bytes(block)
        shift_rows(block)
        mix_columns(block)
        bitwise_xor(block, expkey[16*i:16*(i+1)])
    sub_bytes(block)
    shift_rows(block)
    bitwise_xor(block, expkey[16*rounds:16*(rounds+1)])

# I don't use this anywhere, actually
def decrypt_block(block: bytearray, key: bytes, rounds: int = 10):
    """ Decrypts a 16-byte block with AES """
    assert len(block) == 16
    assert len(key) == 16

    expkey = expand_key(key, rounds)
    bitwise_xor(block, expkey[16*rounds:16*(rounds+1)])
    inv_shift_rows(block)
    inv_sub_bytes(block)
    for i in range(rounds, 0, -1):
        bitwise_xor(block, expkey[16*i:16*(i+1)])
        inv_mix_columns(block)
        inv_shift_rows(block)
        inv_sub_bytes(block)
    bitwise_xor(block, expkey[:16])

def encrypt_ctr(data: bytearray, key: bytes, nonce: int, rounds: int = 10):
    """ Encrypts (or decrypts) an arbitrary blob of data with AES """

    # Pad data to a length multiple of 16 bytes
    while len(data) % 16 != 0:
        data.append(0)

    for i in range(0, len(data), 16):
        # Encrypt the nonce
        block = bytearray(nonce.to_bytes(16, byteorder='big'))
        encrypt_block(block, key, rounds)

        # xor it with the original data
        bitwise_xor(block, data[i:i+16])
        data[i:i+16] = block

        nonce += 1

def stream_ctr(stream, key: bytes, nonce: int, rounds: int = 10):
    """ Encrypts (or decrypts) a stream of bytes with AES """
    while True:
        data = bytearray(stream.read(16))
        if len(data) == 0:
            break

        encrypt_ctr(data, key, nonce, rounds)
        yield data
        nonce += 1

# }}}
