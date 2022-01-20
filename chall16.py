from utils import AES
from utils.padding import pad, unpad
from utils.utils import xor
from os import urandom

class someService:
    def __init__(self):
        self.key = urandom(16)

    def encrypt_user_data(self, data: str) -> bytes:
        final_data = self._parse_user_data(data)

        return self._encrypt(pad(final_data, AES.block_size))

    def is_admin(self, encrypted_data: bytes) -> bool:
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        user_data = self._decrypt(ct, iv)

        return b';admin=true;' in user_data

    def _parse_user_data(self, data: str) -> bytes:
        data = data.replace(';', '\\;').replace('=', '\\=')
        data = "comment1=cooking%20MCs;userdata=" + data + ";comment2=%20like%20a%20pound%20of%20bacon"

        return data.encode()

    def _encrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC)

        return cipher.encrypt(data)

    def _decrypt(self, data: bytes, iv: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return unpad(cipher.decrypt(data), AES.block_size)

def bit_flip(target_decryption: bytes, current_decryption: bytes, prev_ct: bytes) -> bytes:
    keystream = xor(current_decryption, prev_ct)
    new_prev_ct = xor(target_decryption, keystream)

    return new_prev_ct


def main():
    service = someService()
    dummy = "blaahXadminXtrue"
    target = "blaah;admin=true"

    encrypted_dummy = service.encrypt_user_data(dummy)

    flipped_block = bit_flip(target.encode(), dummy.encode(), encrypted_dummy[32:48])
    flipped_encryption = encrypted_dummy[:32] + flipped_block + encrypted_dummy[48:]

    admin = service.is_admin(flipped_encryption)
    print(f"Admin? {admin}")

if __name__ == '__main__':
    main()