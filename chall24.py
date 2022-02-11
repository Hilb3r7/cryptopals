from utils import MT19937
from utils.utils import xor
from os import urandom
from hashlib import sha256
import random, time

class MT19937StreamCipher:
    def __init__(self, version: int, key: int):
        if version not in (32, 64):
            raise ValueError("Version must be 32 or 64 bit")

        self.rng = MT19937.new(version, key)
        self.num_bytes = version // 8
        self.can_encrypt, self.can_decrypt = True, True

    def encrypt(self, pt: bytes) -> bytes:
        if not self.can_encrypt:
            raise TypeError("encrypt() can not be called after decrypt()")
        else:
            self.can_decrypt = False

        num_generates = -(len(pt)//-self.num_bytes) #ceil div
        keystream = b''.join([self.rng.genrand_int().to_bytes(self.num_bytes, 'big') for _ in range(num_generates)])

        return xor(keystream, pt, length='min')

    def decrypt(self, ct: bytes) -> bytes:
        if not self.can_decrypt:
            raise TypeError("decrypt() can not be called after encrypt()")
        else:
            self.can_encrypt = False

        num_generates = -(len(ct)//-self.num_bytes) #ceil div
        keystream = b''.join([self.rng.genrand_int().to_bytes(self.num_bytes, 'big') for _ in range(num_generates)])

        return xor(keystream, ct, length='min')


def poorly_seeded_cipher(msg: bytes) -> (bytes, bytes):
    seed = random.getrandbits(12)
    cipher = MT19937StreamCipher(32, seed)
    pt = urandom(random.randrange(4,42)) + msg

    return seed, cipher.encrypt(pt)

def crack_poorly_seeded_cipher(ct: bytes, msg: bytes) -> int:
    pad_length = len(ct) - len(msg)
    prepended = b'P' * pad_length + msg

    print("Cracking...")
    for seed in range(2**12):
        test_ct = MT19937StreamCipher(32, seed).encrypt(prepended)
        if test_ct[pad_length:] == ct[pad_length:]:
            return seed

    return -1

def generate_reset_token():
    keystream = MT19937StreamCipher(32, int(time.time())).encrypt(b'\x00' * 32)

    return sha256(keystream).hexdigest()

def is_time_seeded_token(token: str) -> bool:
    seed = int(time.time())

    while seed > 0:
        test = MT19937StreamCipher(32, seed).encrypt(b'\x00' * 32)
        if sha256(test).hexdigest() == token:
            return True
        seed -= 1

    return False

def main():
    msg = b'A' * 14
    seed, ct = poorly_seeded_cipher(msg)

    cracked = crack_poorly_seeded_cipher(ct, msg)
    print(f"Cracked? {seed == cracked}; seed: {seed}, cracked: {cracked}")

    reset_token = generate_reset_token()
    print("testing token...")
    print(f"token {reset_token} was generated with current time? {is_time_seeded_token(reset_token)}")

if __name__ == '__main__':
    main()