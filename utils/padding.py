def pad(plaintext: bytes, block_size: int) -> bytes:
    padding = block_size - (len(plaintext) % block_size)

    return plaintext + bytes([padding]) * padding

def unpad(padded: bytes, block_size: int) -> bytes:
    if len(padded) % block_size != 0:
        raise ValueError("Input data is not padded")
    if not _is_valid_padding(padded):
        raise ValueError("Not valid padding")

    return padded[:-padded[-1]]

def _is_valid_padding(padded: bytes) -> bool:
    pad = padded[-1]

    return padded[-pad:] == bytes([pad]) * pad
