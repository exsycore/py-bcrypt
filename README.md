# bcrypt.py

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

## Ex Output
### Bcrypt
- Password is "mypassword"
- Wrong Password is "wrongpassword"
```bash
Hashed: 12$u+q2uy4U0yfe/9SPL+Pjzg==$u+q2uy4U0yfe/9SPL+Pjzm15cGFzc3dvcmQkmMGwXl7a4n9N ... so long
Verify: True
Verify (wrong): False
```
### FastBcrypt
- Password is "mypassword"
- Wrong Password is "wrongpass"
```bash
Hashed: 12$T32PMw1nUHWO+qF5GNOU3g==$V87QFoBtGUAEHckq7xe5sSaGCn2S3IlfvsF58plcvuE=
Verify: True
Verify (Wrong): False
```
# purebcrypt.py
## How to use in file purebcrypt.py
