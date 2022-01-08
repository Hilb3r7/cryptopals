import string
from base64 import b64encode

def hex2b64(data: str) -> bytes:
    if not all(c in string.hexdigits for c in data):
        raise ValueError("Not valid hexadecimal")

    return b64encode(bytes.fromhex(data))

def main():
    hex1 = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    ans = 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'

    result = hex2b64(hex1)
    print(f"correct? {ans == result.decode('utf-8')}, result: {result}")

if __name__ == '__main__':
    main()