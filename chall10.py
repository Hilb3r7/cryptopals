from utils import AES
from utils.padding import unpad
from base64 import b64decode

def parse_input(filename):
    with open(filename) as f:
        data = f.read().replace('\n', '')

    return b64decode(data)

def main():
    key = b'YELLOW SUBMARINE'
    IV = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, IV)

    ct = parse_input('./resources/chall10.txt')
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    print(pt.decode())

if __name__ == '__main__':
    main()