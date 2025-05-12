from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import sys
import os
import traceback

def headless_chrome_test():
    print("\n" + "="*80)
    print("HEADLESS CHROME TEST")
    print("="*80)
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        print("Setting up Chrome options for headless mode...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless=new")  # Run in headless mode
        
        # Try with explicit chromedriver path if available
        chromedriver_path = "/usr/local/bin/chromedriver"  # Common location on macOS with Homebrew
        if os.path.exists(chromedriver_path):
            print(f"Found ChromeDriver at {chromedriver_path}")
            service = Service(executable_path=chromedriver_path)
        else:
            print("Using webdriver-manager to find ChromeDriver")
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
        
        print("Launching headless Chrome browser...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("SUCCESS: Headless Chrome browser launched!")
        
        # Navigate to a URL to verify browser works
        driver.get("https://www.google.com")
        print(f"Navigated to Google. Page title: {driver.title}")
        
        # Take a screenshot to verify the browser is working
        screenshot_path = os.path.join(os.getcwd(), "chrome_test_screenshot.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Get the page source to verify content
        page_source = driver.page_source
        print(f"Page source length: {len(page_source)} characters")
        
        print("Headless Chrome test successful!")
        driver.quit()
        print("Browser closed.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to launch headless Chrome: {str(e)}")
        traceback.print_exc()
        print("\nTROUBLESHOOTING SUGGESTIONS:")
        print("1. Verify that Chrome is installed on your system")
        print("2. Try installing ChromeDriver manually: brew install chromedriver")
        print("3. Check if the ChromeDriver version matches your Chrome version")
        print("4. Look for security/permission issues in System Preferences")
        
        return False

if __name__ == "__main__":
    headless_chrome_test()