import secrets
import sign.oaep as oaep

def test_oaep_inversibility():
    for _ in range(100):
        data = secrets.randbits(512).to_bytes(512 // 8, 'big')
        
        output = oaep.mask(data)
        assert len(output) == len(data) + oaep.K0 + oaep.K1

        input = oaep.unmask(output)
        assert input == data
