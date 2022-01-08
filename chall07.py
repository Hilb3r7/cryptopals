from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

def parse_input(filename):
    with open(filename) as f:
        data = f.read().replace('\n', '')

    return b64decode(data)

def main():
    key = b'YELLOW SUBMARINE'
    ct = parse_input('./resources/chall07.txt')
    cipher = AES.new(key, AES.MODE_ECB)

    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print(pt.decode())

if __name__ == '__main__':
    main()