from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver = webdriver.Chrome(service=Service('./chromedriver.exe'))
driver.get("https://www.google.com")
print(driver.title)
driver.quit()
