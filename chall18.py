from utils import AES
from base64 import b64decode

def main():
    ct = b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
    key = b'YELLOW SUBMARINE'
    nonce = b'\x00' * 8
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    pt = cipher.decrypt(ct)

    print(pt)
    
if __name__ == '__main__':
    main()