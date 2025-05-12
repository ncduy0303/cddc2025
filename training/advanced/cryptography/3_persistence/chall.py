import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

flag = b'CDDC2025{REDACTED}'
key = os.urandom(1)*AES.block_size

def encrypt(msg, key):
	iv = os.urandom(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	ciphertext = cipher.encrypt(pad(msg, AES.block_size))
	return (iv + ciphertext).hex()

print("Encrypted flag:", encrypt(flag, key))

# Encrypted flag: 2042d23ade667d1417a86c42cffb92b4be07835de9814b0a7fe41667120b23ed38518821e1d6f280b47187f4bca94ac18ab45689c302da2d24f1e46603a6904937a9d0a2ff306c509e74a3bd74547719