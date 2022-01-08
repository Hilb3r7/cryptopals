from utils.utils import xor

def get_frequency_vectors():
    ENG_FREQS = {
        b'a': .0655, b'b': .0127, b'c': .0227, b'd': .0335,
        b'e': .1021, b'f': .0197, b'g': .0164, b'h': .0486,
        b'i': .0573, b'j': .0011, b'k': .0057, b'l': .0336,
        b'm': .0202, b'n': .0570, b'o': .0620, b'p': .0150,
        b'q': .0009, b'r': .0497, b's': .0533, b't': .0751,
        b'u': .0230, b'v': .0079, b'w': .0169, b'x': .0015,
        b'y': .0147, b'z': .0007, b' ': .1832
    }

    freq_vectors = [[0]*256 for _ in range(256)]

    for k,v in ENG_FREQS.items():
        for row in range(256):
            freq_vectors[row][ord(k)^row] = v

    return freq_vectors

def get_occurance_vector(a: bytes) -> list:
    size = len(a)
    W = [0] * 256
    for b in a:
        W[b] += (1 / size)

    return W

def dot_product(a: list, b: list) -> int:
    return sum([i*j for i,j in zip(a,b)])

def get_vector_scores(ct: bytes) -> list:
    freq_vectors = get_frequency_vectors()
    W = get_occurance_vector(ct)

    return [dot_product(W, v) for v in freq_vectors]

def get_single_byte_xor(ct: bytes) -> bytes:
    scores = get_vector_scores(ct)
    key = scores.index(max(scores))

    return bytes([key])

def main():
    ct = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    ct = bytes.fromhex(ct)

    key = get_single_byte_xor(ct)
    pt = xor(ct, key)
    print(f"Key: {key}, pt: {pt}")

if __name__ == '__main__':
    main()