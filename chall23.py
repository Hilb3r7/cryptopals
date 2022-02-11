from utils import MT19937
import random

def untemper(y: int, consts: dict) -> int:
    size = consts['w']
    y = invert_right_transform(y, consts['l'], size)
    y = invert_left_transform(y, consts['t'], size, consts['c'])
    y = invert_left_transform(y, consts['s'], size, consts['b'])
    y = invert_right_transform(y, consts['u'], size, consts['d'])

    return y & ((1 << size) - 1)

def invert_right_transform(y1: int, shift: int, size: int, mask: int=0) -> int:
    mask = mask or ((1 << size) - 1)

    if shift >= size / 2:
        return y1 ^ ((y1 >> shift) & mask)
    else:
        y0 = (y1 >> (size - shift)) << (size - shift)
        for _ in range(shift, size, shift):
            y0 = y1 ^ ((y0 >> shift) & mask)
        return y0

def invert_left_transform(y1: int, shift: int, size: int, mask: int=0) -> int:
    mask = mask or ((1 << size) - 1)

    if shift >= size / 2:
        return y1 ^ ((y1 << shift) & mask)
    else:
        y0 = y1
        for _ in range(shift, size, shift):
            y0 = y1 ^ ((y0 << shift) & mask)
        return y0

def clone_MT19937(rng):
    consts = MT19937.CONSTANTS_32 if rng.version == 32 else MT19937.CONSTANTS_64
    state = [untemper(rng.genrand_int(), consts) for _ in range(consts['n'])]
    cloned = MT19937.new(rng.version)
    cloned.set_state(state)

    return cloned

def test_MT19937_cloning(version: int) -> bool:
    seed = random.randrange(1, 2**version)
    rng = MT19937.new(version, seed)
    cloned = clone_MT19937(rng)

    for _ in range(1000):
        if cloned.genrand_int() != rng.genrand_int():
            return False

    return True

def main():
    passed32 = test_MT19937_cloning(32)
    passed64 = test_MT19937_cloning(64)

    print(f"Performing MT19937 Cloning Tests...")
    print(f"  32 Bit: {'Passed' if passed32 else 'Failed'}")
    print(f"  64 Bit: {'Passed' if passed64 else 'Failed'}")

if __name__ == '__main__':
    main()