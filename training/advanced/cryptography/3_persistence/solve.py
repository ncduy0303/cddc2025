from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt(ciphertext):
	ciphertext = bytes.fromhex(ciphertext)
	iv = ciphertext[:AES.block_size]
	ciphertext = ciphertext[AES.block_size:]
	for i in range(256):
		key = bytes([i]) * AES.block_size
		cipher = AES.new(key, AES.MODE_CBC, iv)
		try:
			decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
			if decrypted.startswith("CDDC2025{"):
				return decrypted
		except Exception:
			continue

encrypted_flag = "2042d23ade667d1417a86c42cffb92b4be07835de9814b0a7fe41667120b23ed38518821e1d6f280b47187f4bca94ac18ab45689c302da2d24f1e46603a6904937a9d0a2ff306c509e74a3bd74547719"

flag = decrypt(encrypted_flag)
print(f"Flag: {flag}")