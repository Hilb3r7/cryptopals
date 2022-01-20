from utils.padding import unpad

def main():
    test = b"ICE ICE BABY\x04\x04\x04\x04"
    ans = b"ICE ICE BABY"

    result = unpad(test, 16)
    print(f"correct?: {ans == result}, result: {result}")

    try:
        test = unpad(b"ICE ICE BABY\x05\x05\x05\x05", 16)
    except ValueError as err:
        print(err)

    try:
        test = unpad(b"ICE ICE BABY\x01\x02\x03\x04", 16)
    except ValueError as err:
        print(err)

if __name__ == '__main__':
    main()