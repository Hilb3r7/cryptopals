from utils.padding import pad, unpad

def main():
    example = b"YELLOW SUBMARINE"
    ans = b"YELLOW SUBMARINE\x04\x04\x04\x04"

    result = pad(example, 20)
    print(f"correct? {ans == result}, result: {result}")

    result = unpad(result, 20)
    print(f"correct? {result == example}, result: {result}")

if __name__ == '__main__':
    main()