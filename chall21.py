from utils import MT19937

def parse_testfile(filename: str) -> dict:
    with open(filename, 'r') as f:
        seed = int(f.readline().split('seed = ')[1])
        output = [int(line) for line in f]

    return {'seed':seed, 'output':output}

def test_MT19937(rng: MT19937._MT19937, expected: list[int]) -> bool:
    generated = [rng.genrand_int() for _ in range(len(expected))]

    return generated == expected

def test_implementations():
    test_info_32 = parse_testfile('./resources/mt19937-32.out')
    rng_32 = MT19937.new(32, test_info_32['seed'])
    passed32 = test_MT19937(rng_32, test_info_32['output'])

    test_info_64 = parse_testfile('./resources/mt19937-64.out')
    rng_64 = MT19937.new(64, test_info_64['seed'])
    passed64 = test_MT19937(rng_64, test_info_64['output'])

    print("Testing MT19937 implentations...")
    print(f"  32 bit test: {'Passed' if passed32 else 'Failed'}")
    print(f"  64 bit test: {'Passed' if passed64 else 'Failed'}")

def main():
    test_implementations()

if __name__ == '__main__':
    main()