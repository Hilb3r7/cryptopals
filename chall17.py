from utils import AES #from Crypto.Cipher import AES
from utils.padding import pad, unpad
from utils.utils import xor
from os import urandom
from base64 import b64decode
import random


class paddingOracle:
    def __init__(self):
        self.key = urandom(16)
        self.messages = [
            "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
            "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
            "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
            "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
            "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
            "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
            "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
            "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
            "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
            "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"
        ]

    def get_encrypted_message(self) -> bytes:
        message = b64decode(random.choice(self.messages))
        cipher = AES.new(self.key, AES.MODE_CBC)

        return cipher.encrypt(pad(message, AES.block_size))

    def is_valid_padding(self, message: bytes) -> bool:
        iv = message[:16]
        ct = message[16:]

        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        try:
            unpad(cipher.decrypt(ct), AES.block_size)
        except:
            return False

        return True

def recover_plaintext(oracle: paddingOracle, message: bytes) -> bytes:
    ct_blocks = [message[i:i+16] for i in range(16, len(message), 16)]

    pt = b''
    prev_block = message[:16]
    for block in ct_blocks:
        iv = urandom(16)
        keystream = b''
        for i in range(1, 17):
            for b in range(256):
                iv = iv[:16-i] + bytes([b]) + xor(bytes([i]), keystream, length=len(keystream))
                if oracle.is_valid_padding(iv + block):
                    keystream = bytes([b ^ i]) + keystream
                    break
        pt += xor(keystream, prev_block)
        prev_block = block

    return pt 

def main():
    oracle = paddingOracle()
    message = oracle.get_encrypted_message()
    pt = recover_plaintext(oracle, message)

    print(unpad(pt, AES.block_size))

if __name__ == '__main__':
    main()