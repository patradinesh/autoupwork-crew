from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def apply_and_login_wework():
    driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
    driver.get("https://wework.wd1.myworkdayjobs.com/en-US/WeWork")
    driver.maximize_window()
    time.sleep(4)

    print("🔍 Opening the first job listing...")

    # Click the first job in the list
    first_job = driver.find_element(By.CSS_SELECTOR, 'a[href*="/WeWork/job/"]')
    job_url = first_job.get_attribute("href")
    print("📌 Navigating to job:", job_url)
    driver.get(job_url)
    time.sleep(5)

    try:
        # Scroll down to force button to render
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        print("🚀 Looking for Apply button...")

        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Apply') or contains(text(), 'Start application')]"))
        )

        apply_button.click()
        print("✅ Clicked Apply!")

    except Exception as e:
        print("⚠️ Apply button not found or clickable:", e)
        driver.quit()
        return

    # Optional: wait for login popup and try credentials later
    time.sleep(10)
    driver.quit()

apply_and_login_wework()
