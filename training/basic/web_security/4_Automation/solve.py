import requests

base_url = "http://52.76.13.43:8138/page/"

letters = []

for i in range(1, 103):
    url = f"{base_url}{i}"
    resp = requests.get(url)
    if resp.status_code == 200:
        # Assuming the letter is the whole response or in the body
        letter = resp.text.strip()
        print(f"Page {i}: {letter}")
        if len(letter) == 1:
            letters.append(letter)
    else:
        print(f"Failed to fetch page {i}")

flag = ''.join(letters)
print("Flag:", flag)