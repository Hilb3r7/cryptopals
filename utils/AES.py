from utils.utils import xor
from Crypto.Cipher import AES as AES_primitive
from os import urandom

block_size = 16
MODE_ECB = 1
MODE_CBC = 2
MODE_CTR = 3


class _AES():
    def __init__(self, key: bytes, mode: int, *args, **kwargs):
        if isinstance(key, bytes) and len(key) == 16:
            self.cipher = AES_primitive.new(key, AES_primitive.MODE_ECB)
        else:
            raise ValueError("Key must be 16 bytes")

        if mode in (1,2,3):
            self.mode = mode
        else:
            raise ValueError("Invalid AES mode")

        if self.mode == MODE_CBC:
            IV = args and args[0] or urandom(16)
            if isinstance(IV, bytes) and len(IV) == 16:
                self.IV = IV
            else:
                raise ValueError("IV must be 16 bytes")

        elif self.mode == MODE_CTR:
            nonce = kwargs.pop('nonce', urandom(8))
            initial_value = kwargs.pop('initial_value', 0)
            if kwargs:
                raise TypeError(f"Invalid parameters for CTR mode: {kwargs}")
            if isinstance(nonce, bytes) and len(nonce) == 8:
                self.nonce = nonce
            else:
                raise ValueError("Nonce must be 8 bytes")
            if isinstance(initial_value, int):
                initial_value = initial_value.to_bytes(8, 'little')
            if isinstance(initial_value, bytes) and len(initial_value) == 8:
                self.initial_value = initial_value
            else:
                raise ValueError("Initial Value must be 8 bytes")
            self.counter = int.from_bytes(self.initial_value, 'little')
            self.CTR_can_encrypt, self.CTR_can_decrypt = True, True

    def encrypt(self, plaintext: bytes) -> bytes:
        if not isinstance(plaintext, bytes):
            raise ValueError("Plaintext must be in bytes")
        if self.mode != MODE_CTR and len(plaintext) % block_size != 0:
            raise ValueError("Plaintext must be a multiple of the block size")

        blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]

        if self.mode == 1:
            return self._ECB_encrypt(blocks)
        elif self.mode == 2:
            return self._CBC_encrypt(blocks)
        elif self.mode == 3:
            if self.CTR_can_encrypt:
                self.CTR_can_decrypt = False
                return self._CTR_encrypt(blocks)
            else:
                raise TypeError("encrypt() can no tbe called after decrypt()")

    def decrypt(self, ciphertext: bytes) -> bytes:
        if not isinstance(ciphertext, bytes):
            raise ValueError("Ciphertext must by bytes")
        if self.mode != MODE_CTR and len(ciphertext) % block_size != 0:
            raise ValueError("Ciphertext must be a multiple of the block size")

        blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]

        if self.mode == 1:
            return self._ECB_decrypt(blocks)
        elif self.mode == 2:
            return self._CBC_decrypt(blocks)
        elif self.mode == 3:
            if self.CTR_can_decrypt:
                self.CTR_can_encrypt = False
                return self._CTR_decrypt(blocks)
            else:
                raise TypeError("decrypt() can not be called after encrypt()")

    def _encrypt_block(self, block: bytes) -> bytes:
        assert(len(block) == block_size)
        return self.cipher.encrypt(block)

    def _decrypt_block(self, block: bytes) -> bytes:
        assert(len(block) == block_size)
        return self.cipher.decrypt(block)

    def _ECB_encrypt(self, blocks: list[bytes]) -> bytes:
        return b''.join([self._encrypt_block(block) for block in blocks])

    def _ECB_decrypt(self, blocks: list[bytes]) -> bytes:
        return b''.join([self._decrypt_block(block) for block in blocks])

    def _CBC_encrypt(self, blocks: list[bytes]) -> bytes:
        prev_block = self.IV
        encrypted_blocks = []
        for block in blocks:
            ct = self._encrypt_block(xor(block, prev_block))
            encrypted_blocks.append(ct)
            prev_block = ct

        return self.IV + b''.join(encrypted_blocks)

    def _CBC_decrypt(self, blocks: list[bytes]) -> bytes:
        prev_block = self.IV
        decrypted_blocks = []
        for block in blocks:
            pt = xor(prev_block, self._decrypt_block(block))
            decrypted_blocks.append(pt)
            prev_block = block

        return b''.join(decrypted_blocks)

    def _CTR_encrypt(self, blocks: list[bytes]) -> bytes:
        ct = b''
        for block in blocks:
            key_steam = self._encrypt_block(self.nonce + self.counter.to_bytes(8, 'little'))
            self.counter += 1
            ct += xor(key_steam, block, length='min')

        return ct

    def _CTR_decrypt(self, blocks: list[bytes]) -> bytes:
        pt = b''
        for block in blocks:
            key_steam = self._encrypt_block(self.nonce + self.counter.to_bytes(8, 'little'))
            self.counter += 1
            pt += xor(key_steam, block, length='min')

        return pt

def new(key: bytes, mode: int, *args, **kwargs) -> _AES:
    return _AES(key, mode, *args, **kwargs)
