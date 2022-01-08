import chall03
from utils.utils import xor

def parse_input(filename):
    with open(filename) as f:
        cts = f.read().split('\n')

    return [bytes.fromhex(ct) for ct in cts]

def find_xored_ct(cts: list) -> bytes:
    best_ofs = []
    for ct in cts:
        scores = chall03.get_vector_scores(ct)
        max_score = max(scores)
        key = scores.index(max_score)
        best_ofs.append((max_score, key, ct))

    best_ofs.sort(key=lambda x:x[0], reverse=True)

    return best_ofs[0]

def main():
    cts = parse_input('./resources/chall04.txt')

    winner = find_xored_ct(cts)
    print(winner)
    key = bytes([winner[1]])
    pt = winner[2]

    print(f"pt: {xor(pt, key)}")

if __name__ == '__main__':
    main()