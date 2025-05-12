from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import remote, context, xor
import hashlib
import json

context.log_level = 'debug'  # Enable DEBUG mode

r = remote('52.76.13.43', 8080)

def menu_choice(choice: int):
    r.recvuntil(b'$ ')
    r.sendline(str(choice).encode())

def register(username: str, password: str):
    menu_choice(2)
    r.recvuntil(b'Enter a username: ')
    r.sendline(username.encode())
    r.recvuntil(b'Enter a password (min. 16 characters): ')
    r.sendline(password.encode())
    r.recvuntil(b'Use this token to login: ')
    token = r.recvline().strip().decode()
    return token

def login(token: str):
    menu_choice(1)
    r.recvuntil(b'Input your login token: ')
    r.sendline(token.encode())

def decrypt(iv: bytes, ciphertext: bytes):
    login_token = iv.hex() + ciphertext.hex()
    login(login_token)
    r.recvuntil(b'Token error: ')
    raw_data = r.recvline().strip().decode()
    raw_data = bytes.fromhex(raw_data)
    return raw_data

# https://www.bigous.me/2023/11/17/CBC-bit-flipping-en.html
def bit_flipping(original_plaintext: bytes, modified_plaintext: bytes, ciphertext: bytes, changeiv=False, iv=None):
    diff_positions = []
    print(f"Length of original plaintext: {len(original_plaintext)}, Length of modified plaintext: {len(modified_plaintext)}")
    for position, byte_ in enumerate(original_plaintext):
        x = xor(original_plaintext[position], modified_plaintext[position]) # xor each byte
        if x != b'\x00': # if the result is not null, then it is different
            diff_positions.append(position)
    
    ciphertext = list(ciphertext)
    diff_positions.reverse()
    diff_positions = [position for position in diff_positions if position >= 16]
    
    for position in diff_positions:
        ciphertext[position - 16] = original_plaintext[position] ^ ciphertext[position - 16] ^ modified_plaintext[position] 
    
    ciphertext = bytes(ciphertext) # this ciphertext is wrong

    # recursively call the function until the modified plaintext is equal to the plaintext

    mod_final_plaintext = decrypt(iv, ciphertext) # the attacker needs to be able to decrypt the ciphertext
    new_ciphertext = ciphertext ## need to change the ciphertext again
    
    if mod_final_plaintext[16:] != modified_plaintext[16:]:
        new_ciphertext = bit_flipping(mod_final_plaintext, modified_plaintext, new_ciphertext, changeiv=False, iv=iv)
        mod_final_plaintext = decrypt(iv, new_ciphertext)

    if changeiv == True:
        # the firts 16 bytes of our modified plaintext are wrong, so we need to change the iv, lets get exactly the first 16 bytes wrongs positions of the plaintext
        # like diff again      
        wrong_positions = []
        for position, byte_ in enumerate(mod_final_plaintext[:16]):
            x = xor(mod_final_plaintext[position], modified_plaintext[position])
            if x != b'\x00':
                wrong_positions.append(position)

        # iv to change   
        new_iv = list(iv)
        for wrong_position in wrong_positions:
            new_iv[wrong_position] = mod_final_plaintext[wrong_position] ^ iv[wrong_position] ^ modified_plaintext[wrong_position]
        new_iv = bytes(new_iv)

        # return a tuple contaning the new ciphertext and the new iv
        return new_ciphertext, new_iv

    return new_ciphertext

# Register a user
username = "hacker"
password = "A"*16
token = register(username, password)

# Get the iv and original ciphertext
token_bytes = bytes.fromhex(token)
iv = token_bytes[:16]
ct = token_bytes[16:]

# Get the original and modified plaintext
data = {
    "username": username,
    "password": hashlib.md5(password.encode()).hexdigest(),
    "isAdmin": 0
}
org_pt = json.dumps(data).encode()
data["isAdmin"] = 1
mod_pt = json.dumps(data).encode()

# Do the bit flipping attack
new_ct, new_iv = bit_flipping(org_pt, mod_pt, ct, changeiv=True, iv=iv)
login_token = new_iv.hex() + new_ct.hex()

# Get the flag
login(login_token)
menu_choice(2)
r.recvuntil(b'Here is your flag: ')
flag = r.recvline().strip().decode()
print(f"Flag: {flag}")