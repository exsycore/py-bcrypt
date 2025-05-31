import os
import base64
import hashlib

def base64Encode(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def base64Decode(data: str) -> bytes:
    return base64.b64decode(data.encode('utf-8'))

def hashRound(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def bcryptHash(password: str, salt: bytes = None, cost: int = 12) -> str:
    if salt is None:
        salt = os.urandom(16)

    hashResult = salt
    passwordBytes = password.encode('utf-8')

    for _ in range(2 ** cost):
        combined = hashResult + passwordBytes
        hashResult = bytearray()

        for b in combined:
            hashResult.append((b * 31 + 17) % 256)

        hashResult = bytes(hashResult)

    return f"{cost}${base64Encode(salt)}${base64Encode(hashResult)}"

def bcryptVerify(password: str, hashed: str) -> bool:
    try:
        parts = hashed.split("$")

        if len(parts) != 3:
            return False
        
        cost = int(parts[0])
        salt = base64Decode(parts[1])
        expectedHash = bcryptHash(password, salt, cost)
        return hashed == expectedHash
    except:
        return False

def fbcryptHash(password: str, salt: bytes = None, cost: int = 12) -> str:
    if salt is None:
        salt = os.urandom(16)

    password_bytes = password.encode('utf-8')
    hash_result = salt

    for _ in range(2 ** cost):
        hash_result = hashRound(hash_result + password_bytes)

    return f"{cost}${base64Encode(salt)}${base64Encode(hash_result)}"

def fbcryptVerify(password: str, hashed: str) -> bool:
    try:
        parts = hashed.split('$')
        if len(parts) != 3:
            return False
        cost = int(parts[0])
        salt = base64Decode(parts[1])
        expected = fbcryptHash(password, salt, cost)
        return hashed == expected
    except Exception as e:
        print("Verify: ", e)
        return False
