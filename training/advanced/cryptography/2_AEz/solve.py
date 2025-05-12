from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

key = b'SuperSecureKey12'

# AES block size is 16 bytes
def decrypt(ciphertext, key):
	ciphertext = bytes.fromhex(ciphertext)
	iv = ciphertext[:AES.block_size]
	ciphertext = ciphertext[AES.block_size:]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

encrypted_flag = "7b0c7480f7fcde2af93cf1191b10de6bae350af01eec1acd2c455ec61f33c939234d0402bab5fb212ec3232410bd2e824e0b643506937426028f893cecaaceb63537415a5be021e23be6678a45922842"

flag = decrypt(encrypted_flag, key)

print(f"Flag: {flag}")