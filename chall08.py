def parse_input(filename):
    with open(filename) as f:
        data = f.read().split('\n')

    return data

def contains_dupe_blocks(ct: bytes) -> bool:
    blocks = [ct[i:i+32] for i in range(0, len(ct), 32)]

    return len(blocks) != len(set(blocks))

def main():
    cts = parse_input('./resources/chall08.txt')

    ECB = [ct for ct in cts if contains_dupe_blocks(ct)]
    print(ECB)

if __name__ == '__main__':
    main()