def rotate_left(byte, n):
    return ((byte << n) & 0xFF) | (byte >> (8 - n))

def sha256_block(data):
    h = [0x6a,0x09,0xe6,0x67,0xbb,0x67,0xae,0x85,0x3c,0x6e,0xf3,0x72,0xa5,0x4f,0xf5,0x3a,
         0x51,0x0e,0x52,0x7f,0x9b,0x05,0x68,0x8c,0x1f,0x83,0xd9,0xab,0x5b,0xe0,0xcd,0x19]

    for i, b in enumerate(data):
        idx = i % 32
        h[idx] = (h[idx] + b) & 0xFF
        h[idx] = rotate_left(h[idx], (i % 5) + 1)

    for _ in range(5):
        for i in range(32):
            h[i] = (h[i] ^ h[(i+13) % 32] ^ h[(i+27) % 32]) & 0xFF
            h[i] = rotate_left(h[i], 3)
    return bytes(h)

def pseudo_urandom(n):
    seed = 0x12345678
    out = bytearray()
    for _ in range(n):
        seed = (1103515245 * seed + 12345) & 0x7fffffff
        out.append(seed & 0xFF)
    return bytes(out)

_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def base64_encode(data):
    res = ""
    pad = (3 - len(data) % 3) % 3
    data += b"\x00" * pad
    for i in range(0, len(data), 3):
        n = (data[i] << 16) + (data[i+1] << 8) + data[i+2]
        res += _B64[(n >> 18) & 63] + _B64[(n >> 12) & 63] + _B64[(n >> 6) & 63] + _B64[n & 63]
    if pad:
        res = res[:-pad] + "=" * pad
    return res

def base64_decode(s):
    s = s.rstrip("=")
    table = {c: i for i, c in enumerate(_B64)}
    buf = 0
    bits = 0
    out = bytearray()
    for c in s:
        buf = (buf << 6) | table[c]
        bits += 6
        if bits >= 8:
            bits -= 8
            out.append((buf >> bits) & 0xFF)
    return bytes(out)

def slow_hash(password_bytes, salt_bytes, rounds):
    h = salt_bytes + password_bytes
    for _ in range(rounds):
        h = sha256_block(h)
    return h

def hash_password(password, cost=14, salt=None):
    if salt is None:
        salt = pseudo_urandom(16)
    rounds = 2 ** cost
    p = password.encode("utf-8")
    hashed = slow_hash(p, salt, rounds)
    return f"{cost}${base64_encode(salt)}${base64_encode(hashed)}"

def constant_time_compare(a, b):
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0

def verify_password(password, hashed):
    try:
        cost, salt_b64, hash_b64 = hashed.split("$")
        cost = int(cost)
        salt = base64_decode(salt_b64)
        expected_hash = slow_hash(password.encode("utf-8"), salt, 2 ** cost)
        return constant_time_compare(expected_hash, base64_decode(hash_b64))
    except Exception:
        return False

# --- TEST ---
def test():
    password_correct = "MySecurePassword123!"
    password_wrong = "NotTheRightPassword"

    hashed = hash_password(password_correct, cost=12)
    print("Hashed Password:", hashed)

    result_correct = verify_password(password_correct, hashed)
    print("Verify correct password:", result_correct)

    result_wrong = verify_password(password_wrong, hashed)
    print("Verify wrong password:", result_wrong)

if __name__ == "__main__":
    test()
