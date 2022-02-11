from utils import AES
from utils.utils import xor
from base64 import b64decode
from chall03 import get_single_byte_xor
from os import urandom

def parse_input(filename: str) -> list[bytes]:
    with open(filename, 'r') as f:
        pts = [b64decode(line.strip()) for line in f]

    return pts

def CTR_encrypt_pts(pts: list[bytes]) -> list[bytes]:
    key = urandom(16)
    nonce = b'\x00' * 8
    cts = []
    for pt in pts:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        cts.append(cipher.encrypt(pt))

    return cts

def main():
    pts = parse_input('./resources/chall20.txt')
    cts = CTR_encrypt_pts(pts)
    key_length = min(len(ct) for ct in cts)

    key = b''
    for i in range(key_length):
        ct = bytes([ct[i] for ct in cts])
        key += get_single_byte_xor(ct)

    for i, ct in enumerate(cts):
        print(f"Actual: {pts[i]}\nRecvrd: {xor(key, ct, length='min')}\n")

if __name__ == '__main__':
    main()