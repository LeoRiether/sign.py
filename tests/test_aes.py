from random import randint
import sign.aes as aes
import secrets

# Credits to https://blog.nindalf.com/posts/implementing-aes/
# for a lot of the test cases

def to_bytearray(x, n):
    y = x.to_bytes(n, byteorder='big')
    return bytearray(y)

def rand_bytearray(n):
    return bytearray(secrets.token_bytes(n))

def test_sub_bytes():
    # only 1 testcase actually /shrug
    testcases = [
        (0x8e9ff1c64ddce1c7a158d1c8bc9dc1c9,
         0x19dba1b4e386f8c6326a3ee8655e78dd)
    ]

    for input, output in testcases:
        i = to_bytearray(input, 16)
        o = to_bytearray(output, 16)

        i_ = bytearray(i)
        aes.sub_bytes(i_)
        assert i_ == o

        o_ = bytearray(o)
        aes.inv_sub_bytes(o_)
        assert i == o_

def test_shift_rows():
    testcases = [
        (0x01020304050607080910111213141516,
         0x01061116051015040914030813020712)
    ]

    for input, output in testcases:
        i = to_bytearray(input, 16)
        o = to_bytearray(output, 16)

        i_ = bytearray(i)
        aes.shift_rows(i_)
        assert i_ == o

        o_ = bytearray(o)
        aes.inv_shift_rows(o_)
        assert i == o_

def do_inversibility_test(gen, forwards, backwards):
    """
        Generates a bytearray with `gen()`, then passes it
        through `forwards` and `backwards`. The final bytearray
        should be the same as the original
    """
    for _ in range(20):
        i = gen()
        e = bytearray(i)
        forwards(i)
        backwards(i)
        assert i == e

def test_sub_bytes_inversibility():
    do_inversibility_test(
       lambda: rand_bytearray(16),
       aes.sub_bytes, aes.inv_sub_bytes)

def test_shift_rows_inversibility():
    do_inversibility_test(
       lambda: rand_bytearray(16),
       aes.shift_rows, aes.inv_shift_rows)

def test_mix_columns_inversibility():
    do_inversibility_test(
       lambda: rand_bytearray(16),
       aes.mix_columns, aes.inv_mix_columns)

def test_block_encription_inversibility():
    for _ in range(20):
        i = bytearray(secrets.token_bytes(16))
        k = secrets.token_bytes(128 // 8)
        e = bytearray(i)

        aes.encrypt_block(i, k)
        aes.decrypt_block(i, k)
        assert i == e

def test_ctr_inversibility():
    for _ in range(20):
        i = bytearray(secrets.token_bytes(1024 // 8))
        k = secrets.token_bytes(128 // 8)
        nonce = secrets.randbits(16)
        e = bytearray(i)

        aes.encrypt_ctr(i, k, nonce)
        aes.encrypt_ctr(i, k, nonce)
        assert i == e

def test_ctr_size():
    for _ in range(30):
        n = randint(1, 200)
        i = bytearray(secrets.token_bytes(n))
        k = secrets.token_bytes(16)
        nonce = secrets.randbits(16)

        expected_size = (n + 15) // 16 * 16
        aes.encrypt_ctr(i, k, nonce)
        assert len(i) == expected_size 

