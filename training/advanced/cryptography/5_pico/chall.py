from Crypto.Util.number import *

flag = b"CDDC2025{REDACTED}"
m = bytes_to_long(flag)

p = getPrime(512)
q = getPrime(512)
e = 3
n = p*q
phi = (p-1)*(q-1)
d = pow(e,-1,phi)

c = pow(m,e,n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
# print(f"d = {d}")