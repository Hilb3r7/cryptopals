from utils.padding import pad, unpad
from utils import AES
from base64 import b64decode
from chall11 import EncryptionOracleInterface, ECB_CBC_detector
from os import urandom


class encryptionOracle(EncryptionOracleInterface):
    def __init__(self):
        self.key = urandom(16)
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.secret = b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

    def encrypt(self, data: bytes) -> bytes:
        pt = data + self.secret
            
        return self.cipher.encrypt(pad(pt, AES.block_size))


def get_block_size(oracle: type[EncryptionOracleInterface]) -> int:
    test = b''
    base_len = len(oracle.encrypt(test))
    new_len = base_len

    while new_len == base_len:
        test += b'A'
        new_len = len(oracle.encrypt(test))

    return new_len - base_len

def recover_secret(oracle: type[EncryptionOracleInterface], secret_size: int) -> bytes:
    assert(ECB_CBC_detector(oracle) == 'ECB')

    feed = b'A' * secret_size
    recovered = b''
    for i in range(secret_size):
        pt = feed[:-i]
        ct = oracle.encrypt(pt)
        to_match = ct[:secret_size]
        for b in range(256):
            test = pt + recovered + bytes([b])
            if oracle.encrypt(test)[:secret_size] == to_match:
                recovered += bytes([b])
                break

    return recovered

def main():
    oracle = encryptionOracle()
    secret_size = len(oracle.encrypt(b''))
    secret = recover_secret(oracle, secret_size)

    print(secret.decode())

if __name__ == '__main__':
    main()