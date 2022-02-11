import time, random
from utils import MT19937

def get_seed_simul():
    seed = random.randint(40,1000)
    seed += time.time()
    seed += random.randint(40,100)

    return int(seed)

def crack_seed_time_start(start: int, target: int) -> int:
    seed = start
    while True:
        rng = MT19937.new(32, seed)
        if rng.genrand_int() == target:
            return seed
        seed += 1

def get_seed_timesuck():
    print("ZzZz...")
    time.sleep(random.randint(40, 1000))
    seed = time.time()
    time.sleep(random.randint(40, 1000))

    return int(seed)

def crack_seed_time_end(end: int, target: int) -> int:
    seed = end
    while True:
        rng = MT19937.new(32, seed)
        if rng.genrand_int() == target:
            return seed
        seed -= 1

def time_suck():
    secret_seed = get_seed_timesuck()
    rng = MT19937.new(32, secret_seed)
    first = rng.genrand_int()

    print("Cracking...")
    cracked = crack_seed_time_end(int(time.time()), first)

    print(f"Cracked? {cracked == secret_seed}; seed: {secret_seed} cracked: {cracked}")


def main():
    secret_seed = get_seed_simul()
    rng = MT19937.new(32, secret_seed)
    first = rng.genrand_int()

    cracked = crack_seed_time_start(int(time.time()), first)
    print(f"Cracked? {cracked == secret_seed}; seed: {secret_seed} cracked: {cracked}")

    time_suck()

if __name__ == '__main__':
    main()