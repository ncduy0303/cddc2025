from pwn import remote, context
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Util.number import long_to_bytes
import hashlib
import ast

# Set up connection
context.log_level = 'debug'  # Enable DEBUG mode
r = remote('52.76.13.43', 8081)

# === Step 1: Receive DH parameters ===
r.recvuntil(b"g = ")
g = int(r.recvline().decode().strip())
r.recvuntil(b"p = ")
p = int(r.recvline().decode().strip())
print(f"g: {g}, p: {p}")

# === Step 2: Intercept Alice's A ===
r.recvuntil(b"A = ")
A = int(r.recvline().decode().strip())

# === Step 3: Just send Alice's A back ===
r.sendlineafter(b"A = ", str(A).encode())

# === Step 4: Intercept Bob’s B ===
r.recvuntil(b"B = ")
B = int(r.recvline().decode().strip())

# === Step 5: Replace B with our own fake B ===
x = 2024  # our private key for talking to Alice
B_fake = pow(g, x, p)
r.sendlineafter(b"B = ", str(B_fake).encode())

# === Step 6: Receive Encrypted Flag ===
r.recvuntil(b"Alice: ")
data_str = r.recvline().decode().strip()
data = ast.literal_eval(data_str)

# === Step 7: Parse IV and ciphertext ===
iv = bytes.fromhex(data['iv'])
ct = bytes.fromhex(data['encrypted_flag'])

# === Step 8: Compute shared secret ===
shared_secret = pow(A, x, p)
key = hashlib.md5(long_to_bytes(shared_secret)).digest()
cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(ct), AES.block_size)

# === Step 9: Print the flag ===
print("Flag:", flag.decode())