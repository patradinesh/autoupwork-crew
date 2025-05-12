from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import sys
import os

def browser_launch_test():
    print("\n" + "="*80)
    print("BROWSER LAUNCH TEST - TROUBLESHOOTING")
    print("="*80)
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Try Chrome first
    try_chrome()
    
    # If Chrome didn't work, try Firefox as a fallback
    try_firefox()
    
    print("\nTest complete. Check if any browser windows opened.")
    print("="*80)

def try_chrome():
    print("\n" + "-"*40)
    print("ATTEMPTING TO LAUNCH CHROME")
    print("-"*40)
    
    try:
        print("Setting up Chrome options...")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option("detach", True)  # Keep browser open
        
        # Uncomment the line below if you want to try headless mode
        # chrome_options.add_argument("--headless=new")
        
        print("Installing ChromeDriver...")
        service = ChromeService(ChromeDriverManager().install())
        
        print("Launching Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("SUCCESS: Chrome browser launched!")
        
        # Navigate to a simple URL to verify browser works
        driver.get("https://www.google.com")
        print(f"Navigated to Google. Page title: {driver.title}")
        
        print("Chrome test successful. Browser window should remain open.")
        print("If you can see a Chrome window, the Chrome test passed.")
        
        # We intentionally don't close the driver so the window stays open
        
    except Exception as e:
        print(f"ERROR: Failed to launch Chrome: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Chrome test failed. Trying Firefox next...")

def try_firefox():
    print("\n" + "-"*40)
    print("ATTEMPTING TO LAUNCH FIREFOX")
    print("-"*40)
    
    try:
        print("Setting up Firefox options...")
        firefox_options = FirefoxOptions()
        
        print("Installing GeckoDriver (Firefox driver)...")
        service = FirefoxService(GeckoDriverManager().install())
        
        print("Launching Firefox browser...")
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        print("SUCCESS: Firefox browser launched!")
        
        # Navigate to a simple URL to verify browser works
        driver.get("https://www.google.com")
        print(f"Navigated to Google. Page title: {driver.title}")
        
        print("Firefox test successful. Browser window will remain open.")
        print("If you can see a Firefox window, the Firefox test passed.")
        
        # We intentionally don't close the driver so the window stays open
        
    except Exception as e:
        print(f"ERROR: Failed to launch Firefox: {str(e)}")
        import traceback
        traceback.print_exc()
        print("Both Chrome and Firefox tests failed.")
        print("\nTROUBLESHOOTING SUGGESTIONS:")
        print("1. Verify that Chrome or Firefox is installed on your system")
        print("2. Try running the script with administrator/sudo privileges")
        print("3. Check if your antivirus or firewall is blocking WebDriver")
        print("4. Ensure you have enough system resources (memory, CPU)")
        print("5. Try installing the browser drivers manually")
        print("   - For Chrome: brew install chromedriver (on macOS)")
        print("   - For Firefox: brew install geckodriver (on macOS)")

if __name__ == "__main__":
    browser_launch_test()