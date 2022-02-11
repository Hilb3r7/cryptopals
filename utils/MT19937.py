CONSTANTS_32 = {
    'w': 32,
    'n': 624,
    'm': 397,
    'r': 31,
    'a': 0x9908B0DF,
    'u': 11,
    'd': 0xFFFFFFFF,
    's': 7,
    'b': 0x9D2C5680,
    't': 15,
    'c': 0xEFC60000,  
    'l': 18,
    'f': 1812433253
}

CONSTANTS_64 = {
    'w': 64,
    'n': 312,
    'm': 156,
    'r': 31,
    'a': 0xB5026F5AA96619E9,
    'u': 29,
    'd': 0x5555555555555555,
    's': 17,
    'b': 0x71D67FFFEDA60000,
    't': 37,
    'c': 0xFFF7EEE000000000,
    'l': 43,
    'f': 6364136223846793005
}


class _MT19937:
    def __init__(self, version: int, consts: dict, seed: int):
        self.version = version
        self.w = consts['w']
        self.n = consts['n']
        self.m = consts['m']
        self.r = consts['r']
        self.a = consts['a']
        self.u = consts['u']
        self.d = consts['d']
        self.s = consts['s']
        self.b = consts['b']
        self.t = consts['t']
        self.c = consts['c']
        self.l = consts['l']
        self.f = consts['f']
        self.lower_mask = 0x7FFFFFFF #(1 << self.r) - 1 
        self.upper_mask = ~((1 << self.w) + self.lower_mask)

        self.MT = [i for i in range(self.n)]
        self.index = self.n + 1
        self._seed_mt(seed)

    def _seed_mt(self, seed: int):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & ((1 << self.w) - 1)
 
    def genrand_int(self) -> int:
        if self.index >= self.n:
            self._twist()
 
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
     
        self.index += 1

        return y & ((1 << self.w) - 1)

    def get_state(self) -> list[int]:
        return self.MT

    def set_state(self, state: list[int]):
        if (len(state) != self.n):
            raise ValueError(f"State needs to be of size {self.n}")
        self.index = self.n
        self.MT = state

    def _twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
    
        self.index = 0

def new(version: int, seed: int=5489) -> _MT19937:
    if version not in (32, 64):
        raise ValueError("Version must be either 32 or 64 bit")

    consts = CONSTANTS_32 if version == 32 else CONSTANTS_64
    return _MT19937(version, consts, seed)