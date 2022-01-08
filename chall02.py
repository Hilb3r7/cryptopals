def xor(a: str, b: str) -> str:
    if len(a) != len(b):
        raise ValueError("Input strings not equal length")

    return hex(int(a, 16) ^ int(b, 16))[2:]

def main():
    hex1 = '1c0111001f010100061a024b53535009181c'
    hex2 = '686974207468652062756c6c277320657965'
    ans = '746865206b696420646f6e277420706c6179'

    result = xor(hex1, hex2)

    print(f"correct? {ans == result}, result: {result}")

if __name__ == '__main__':
    main()