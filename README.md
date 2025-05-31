# Py-bcrypt

## How to use
### Bcrypt
```py
hashed = bcryptHash("mypassword", cost=12)
print("Hashed:", hashed)
print("Verify:", bcryptVerify("mypassword", hashed))
print("Verify (wrong):", bcryptVerify("wrongpassword", hashed))
```
### FastBcrypt
```py
hashed = fbcryptHash("mypassword", cost=12)
print("Hashed:", hashed)
print("Verify:", fbcryptVerify("mypassword", hashed))
print("Verify (Wrong):", fbcryptVerify("wrongpass", hashed))
```
