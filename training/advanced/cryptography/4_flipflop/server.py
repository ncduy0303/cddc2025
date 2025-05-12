#!/usr/bin/env python3

from secret import FLAG, KEY
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import json

# Key will be used for AES
assert(len(KEY) == AES.block_size)

# Database
registered_users = {
	"admin": "313f5533de8a6421fa921741e7594d5f",
	"user1": "0fa84a52cafbb1cad05d7a6425f9ed1a",
}


def generate_token(iv, data):
	cipher = AES.new(KEY, AES.MODE_CBC, iv = bytes.fromhex(iv))
	data = pad(data, AES.block_size)
	token = cipher.encrypt(data)
	token = token.hex()
	return iv + token

def register(username, password):
	iv = password[:16].encode().hex()
	hash_password = hashlib.md5(password.encode()).digest().hex()
	data = json.dumps({"username": username, "password": hash_password, "isAdmin": 0}).encode()
	token = generate_token(iv, data)
	registered_users[username] = hash_password
	return token

def login(token):
	token = bytes.fromhex(token)
	iv = token[:16]
	token = token[16:]
	cipher = AES.new(KEY, AES.MODE_CBC, iv = iv)
	data = cipher.decrypt(token)
	data = unpad(data, 16)
	try:
		raw_data = json.loads(data)
		assert raw_data["password"] == registered_users[raw_data["username"]]
		assert raw_data["isAdmin"] in range(0, 2)
		return iv.hex(), raw_data
	except:
		print(f"Token error: {data.hex()}")
		return "Error", "Error"

def main_menu(iv, data):
	while True:
		if data["isAdmin"] == 0:
			print(f"Hello, {data['username']}! You are a regular user.")
			print("1. Logout")
			opt = input("$ ")

			if opt == "1":
				print(f"Thank you and see you again!")
				print(f"Your token for this session: {generate_token(iv, json.dumps(data).encode())}")
				break

			else:
				print("Invalid input!")

		elif data["isAdmin"] == 1:
			print(f"Hello, {data['username']}! You are an admin.")
			print("1. Logout")
			print("2. Get Flag")
			opt = input("$ ")

			if opt == "1":
				print(f"Thank you and see you again!")
				print(f"Your token for this session: {generate_token(iv, json.dumps(data).encode())}")
				break

			elif opt == "2":
				print(f"Here is your flag: {FLAG}")
				break			

			else:
				print("Invalid input!")

		else:
			print("Invalid session token!")


# Main code
while True:
	print(f"============== WELCOME ==============")
	print(f"1. Login")
	print(f"2. Register")
	print(f"3. Exit")
	opt = input("$ ")

	if opt == "1":
		token = input("Input your login token: ")
		try:
			iv, data = login(token)
			if data == "Error":
				continue
		except:
			print("Invalid session token!")
			continue
		main_menu(iv, data)

	elif opt == "2":
		username = input("Enter a username: ")
		if username in registered_users:
			print("That username is already taken. Try again.")
			continue
		password = input("Enter a password (min. 16 characters): ")
		if len(password) < 16:
			print("Your password length is too short. Try again. ")
			continue
		token = register(username, password)
		print(f"Registration successful!")
		print(f"Use this token to login: {token}")

	elif opt == "3":
		print("See you again!")
		exit()

	else:
		print("Invalid input!")