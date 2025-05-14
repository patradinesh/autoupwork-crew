import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import dotenv_values

# ✅ STEP 1: LOAD CREDENTIALS FROM .env FILE
print("🚦 Script started...")

config = dotenv_values("upwork-job-monitor/.env")  # adjust path to where your .env file is
email = config.get("UPWORK_USERNAME")
password = config.get("UPWORK_PASSWORD")

print("📧 Loaded email:", email)
print("🔐 Loaded password:", '*' * len(password) if password else "❌ MISSING")

# ✅ STEP 2: AUTOMATE UPWORK LOGIN
def login_upwork():
    print("🌐 Launching ChromeDriver...")
    driver = uc.Chrome()
    print("✅ Chrome launched.")

    driver.get("https://www.upwork.com/ab/account-security/login")
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    try:
        print("📝 Waiting for email field...")
        email_input = wait.until(EC.presence_of_element_located((By.ID, "login_username")))
        email_input.send_keys(email)
        print("📧 Email entered.")

        print("➡️ Clicking Continue...")
        continue_button = wait.until(EC.element_to_be_clickable((By.ID, "login_password_continue")))
        continue_button.click()

        print("⏳ Waiting for password screen...")
        time.sleep(2)

        print("🔑 Waiting for password input...")
        password_input = wait.until(EC.visibility_of_element_located((By.ID, "login_password")))
        password_input.send_keys(password)
        print("🔒 Password entered.")

        print("✅ Clicking Log In...")
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login_control_continue")))
        login_button.click()

        print("🎉 Login attempted. Solve CAPTCHA manually if it appears.")
        time.sleep(15)

    except Exception as e:
        print("❌ Error during login:", str(e))

    finally:
        print("🛑 Closing browser...")
        driver.quit()

# ✅ RUN THE FUNCTION
login_upwork()
