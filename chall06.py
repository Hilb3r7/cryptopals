from utils.utils import xor
from base64 import b64decode
from chall03 import get_single_byte_xor

def parse_input(filename):
    with open(filename) as f:
        data = f.read().replace('\n', '')

    return b64decode(data.encode())

def hamming_distance(a: bytes, b: bytes) -> int:
    return sum([bin(b1 ^ b2).count('1') for b1, b2 in zip(a,b)])

def get_key(ct: bytes, size: int) -> bytes:
    key = b''
    for i in range(size):
        block = ct[i:-1:size]
        key += get_single_byte_xor(block)

    return key

def get_key_size(ct: bytes) -> int:
    hamming_distances = [hamming_distance(ct[-i:] + ct[:-i], ct) for i in range(41)]

    return hamming_distances.index(min(hamming_distances[2:]))

def main():
    ct = parse_input('./resources/chall06.txt')
    key_size = get_key_size(ct)
    key = get_key(ct, key_size)
    pt = xor(ct, key)

    print(f"key: {key.decode()}\npt: {pt.decode()}")


if __name__ == '__main__':
    main()