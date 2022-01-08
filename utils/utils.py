
def xor(*args, **kwargs):
    strs = [s for s in args]

    length = kwargs.pop('length', 'max')
    if isinstance(length, int):
        length = length
    elif length == 'max':
        length = max(len(s) for s in strs)
    elif length == 'min':
        length = min(len(s) for s in strs)
    else:
        raise ValueError("Invalid value for length parameter")

    def xor_indices(index):
        b = 0
        for s in strs:
            b ^= s[index % len(s)]
        return b

    return bytes([xor_indices(i) for i in range(length)])
