from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# List of potential answers
airports = [
    "NARITA",
    "MUC",
    "MUNICHINTERNATIONALAIRPORT",
    "FRANZJOSEFSTRAUSS",
    "MUNICHAIRPORT",
    "MUNICH",
    "EDDM",
]

countries = [
    "japan",
    "germany",
]

schools = [
    "koreauniversity",
    "ku",
]

# URL of the challenge page
FORM_URL = "http://52.76.13.43:8128/"  # <-- Replace with the actual challenge URL

# Set up Edge WebDriver
driver = webdriver.Edge()

# Open the page
driver.get(FORM_URL)

# Loop through each answer (combination of airports, countries, and schools)
answers = []
for airport in airports:
    for country in countries:
        for school in schools:
            answers.append(f"{airport}{country}{school}")
for answer in answers:
    try:
        # Find input and fill answer
        input_field = driver.find_element(By.NAME, "answer")
        input_field.clear()
        input_field.send_keys(answer)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        # Wait for page to reload
        time.sleep(0.1)

        # Check for success (no 'Incorrect' message)
        page_source = driver.page_source.lower()
        if "wrong answer" not in page_source:
            print(f"[+] Correct answer found: {answer}")
            break
        else:
            print(f"[-] Tried: {answer} — incorrect")

    except Exception as e:
        print(f"[!] Error trying '{answer}': {e}")

# Close browser
driver.quit()
