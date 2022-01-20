from utils.padding import pad, unpad
from utils import AES
from base64 import b64decode
from chall11 import EncryptionOracleInterface
from os import urandom
from random import randint


class encryptionOracle(EncryptionOracleInterface):
    def __init__(self):
        self.key = urandom(16)
        self.cipher = AES.new(self.key, AES.MODE_ECB)
        self.prefix = urandom(randint(1,42))
        self.secret = b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

    def encrypt(self, data: bytes) -> bytes:
        pt = self.prefix + data + self.secret
            
        return self.cipher.encrypt(pad(pt, AES.block_size))
        

def get_start_index_final_prefix_block(oracle: type[EncryptionOracleInterface]) -> int:
    no_add = oracle.encrypt(b'')
    added = oracle.encrypt(b'A')

    return next((i for i, (a,b) in enumerate(zip(no_add, added)) if a != b), 0)

def get_prefix_size(oracle: type[EncryptionOracleInterface]) -> int:
    start = get_start_index_final_prefix_block(oracle)

    prev_enc = oracle.encrypt(b'')[start:start+16]
    feed = b'A'
    while (current_enc := oracle.encrypt(feed)[start:start+16]) != prev_enc:
        feed += b'A'
        prev_enc = current_enc

    return (start + 16) - (len(feed) - 1)

def recover_prefixed_secret(oracle: type[EncryptionOracleInterface]) -> bytes:
    prefix_size = get_prefix_size(oracle)
    prefix_fill = b'P' * (-(prefix_size//-16) - prefix_size)
    secret_size = len(oracle.encrypt(prefix_fill)) - (prefix_size + len(prefix_fill))

    feed = prefix_fill + b'A' * secret_size
    compare_len = prefix_size + len(feed)
    recovered = b''
    for i in range(secret_size):
        pt = feed[:-i]
        ct = oracle.encrypt(pt)
        to_match = ct[:compare_len]
        for b in range(256):
            test = pt + recovered + bytes([b])
            if oracle.encrypt(test)[:compare_len] == to_match:
                recovered += bytes([b])
                break

    return recovered

def main():
    oracle = encryptionOracle()
    secret = recover_prefixed_secret(oracle)
    print(secret.decode())


if __name__ == '__main__':
    main()