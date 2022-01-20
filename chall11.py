from utils.padding import pad, unpad
from utils import AES
from random import randint
from os import urandom

class EncryptionOracleInterface:
    def encrypt(self, data: bytes) -> bytes:
        pass

class encryptionOracle(EncryptionOracleInterface):
    def __init__(self):
        self.history = []
        self.key = urandom(16)

    def encrypt(self, data: bytes) -> bytes:
        pt = urandom(randint(5,10)) + data + urandom(randint(5,10))

        if randint(0,1):
            self.history.append('CBC')
            cipher = AES.new(self.key, AES.MODE_CBC)
        else:
            self.history.append('ECB')
            cipher = AES.new(self.key, AES.MODE_ECB)
            
        return cipher.encrypt(pad(pt, AES.block_size))



def ECB_CBC_detector(oracle: type[EncryptionOracleInterface]) -> str:
    data = b'A' * 48
    ct = oracle.encrypt(data)

    blocks = [ct[i:i+AES.block_size] for i in range(0, len(ct), AES.block_size)]

    return 'ECB' if len(blocks) != len(set(blocks)) else 'CBC'

def main():
    oracle = encryptionOracle()
    detections = []

    for _ in range(10):
        detections.append(ECB_CBC_detector(oracle))

    print(f"correct? {detections == oracle.history}\nactaul: {oracle.history}\nexpect: {detections}")


if __name__ == '__main__':
    main()