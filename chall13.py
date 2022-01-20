from utils import AES
from utils.padding import pad, unpad
from os import urandom

class someService:
    def __init__(self):
        self.cipher = AES.new(urandom(16), AES.MODE_ECB)
        self.next_uid = 10

    def encrypt_profile_for(self, address: str) -> bytes:
        profile = self._profile_for(address)
        return self.cipher.encrypt(pad(profile.encode(), AES.block_size))

    def decrypt_profile(self, profile: bytes) -> dict:
        params = unpad(self.cipher.decrypt(profile), AES.block_size).decode()
        return self._param_parse(params)

    def _param_parse(self, params: str) -> dict:
        return dict(param.split('=') for param in params.split('&'))

    def _profile_for(self, address: str) -> str:
        if '&' in address or '=' in address:
            raise ValueError("Address can not contain '&' or '='")

        profile = f"email={address}&uid={self.next_uid}&role=user"
        self.next_uid += 1

        return profile

def main():
    oracle = someService()

    blah = oracle.encrypt_profile_for("blah@blah.com")
    print(oracle.decrypt_profile(blah))

    garbage = b'AAAAAAAAAAadmin' + b'\x0b' * 11 + b'@haha.com'
    garbage_acc = oracle.encrypt_profile_for(garbage.decode())
    print(oracle.decrypt_profile(garbage_acc))

    pwned = blah[:32] + garbage_acc[16:32]
    print(oracle.decrypt_profile(pwned))


if __name__ == '__main__':
    main()