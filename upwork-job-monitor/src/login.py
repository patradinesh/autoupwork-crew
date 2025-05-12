import logging
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoginManager:
    def __init__(self, username, password, security_answers=None):
        self.username = username
        self.password = password
        # Default security answers dictionary - can be overridden
        self.security_answers = security_answers or {
            "What is your first pet's name": "Pintu"
        }
        self.driver = None
        self.is_logged_in = False
        
    def initialize_driver(self):
        """Initialize and configure the Chrome webdriver with more human-like behavior"""
        try:
            chrome_options = Options()
            
            # Make the browser appear more like a regular browser to avoid detection
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Add random user agent to appear more like a regular user
            user_agents = [
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Disable automation flags to appear less like a bot
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Keep the browser window open after script completion
            chrome_options.add_experimental_option("detach", True)
            
            # Initialize the driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Set window size to a common resolution
            self.driver.set_window_size(1366, 768)
            
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: function() {
                        return [1, 2, 3, 4, 5];
                    }
                });
                """
            })
            
            logger.info("WebDriver initialized with anti-detection measures")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            return False

    def login_with_cloudflare_handling(self):
        """Log in to Upwork with better handling for Cloudflare verification"""
        if not self.initialize_driver():
            return False
            
        try:
            # Clear cookies and cache first
            self.driver.delete_all_cookies()
            
            # Navigate to Upwork login page with random delays
            self.driver.get("https://www.upwork.com")
            self.random_delay(1, 3)
            
            # Go to login page more naturally - click on the login button
            try:
                login_link = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='login']"))
                )
                login_link.click()
                logger.info("Clicked on login link")
            except Exception:
                # If we can't find the login link, go directly to login page
                self.driver.get("https://www.upwork.com/ab/account-security/login")
                logger.info("Navigated directly to login page")
            
            self.random_delay(2, 4)
            
            # Handle Cloudflare verification if present
            self.handle_cloudflare_verification()
            
            # Wait for username field and enter username with human-like typing
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login_username"))
            )
            self.human_like_typing(username_field, self.username)
            logger.info("Entered username")
            
            self.random_delay(1, 2)
            
            # Click continue button
            continue_button = self.driver.find_element(By.ID, "login_password_continue")
            continue_button.click()
            logger.info("Clicked continue button")
            
            self.random_delay(2, 4)
            
            # Handle Cloudflare verification again if it appears
            self.handle_cloudflare_verification()
            
            # Wait for password field and enter password with human-like typing
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login_password"))
            )
            self.human_like_typing(password_field, self.password)
            logger.info("Entered password")
            
            self.random_delay(1, 2)
            
            # Click login button
            login_button = self.driver.find_element(By.ID, "login_control_continue")
            login_button.click()
            logger.info("Clicked login button")
            
            self.random_delay(3, 5)
            
            # Handle Cloudflare verification again after login attempt
            self.handle_cloudflare_verification()
            
            # Check for security question
            try:
                security_form = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form[data-qa='security-question-form']"))
                )
                if security_form:
                    # Extract the security question text
                    question_element = security_form.find_element(By.CSS_SELECTOR, "div.up-card-section")
                    question_text = question_element.text.strip()
                    logger.info(f"Security question detected: {question_text}")
                    
                    print("\n" + "*" * 80)
                    print(f"* SECURITY QUESTION DETECTED: '{question_text}'")
                    print("* Please make note of this exact question text.")
                    print("* If you want to complete the security answer manually, do so now.")
                    print("* The script will wait for 60 seconds.")
                    print("*" * 80 + "\n")
                    
                    # Wait for manual intervention
                    time.sleep(60)
            except (TimeoutException, NoSuchElementException):
                logger.info("No security question detected")
            
            # Check if we're logged in
            try:
                # Try to find an element that indicates successful login
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "nav.navbar"))
                )
                logger.info("Login successful")
                self.is_logged_in = True
                return True
            except (TimeoutException, NoSuchElementException):
                logger.warning("Could not detect successful login")
                
                # The browser window will remain open for manual inspection
                print("\n" + "*" * 80)
                print("* Login process completed, but login status unclear.")
                print("* The browser window will remain open for manual inspection.")
                print("* You can continue manually if needed.")
                print("*" * 80 + "\n")
                
                return False
            
        except Exception as e:
            logger.error(f"Error during login process: {e}")
            if self.driver:
                self.driver.save_screenshot("login_error.png")
            return False
    
    def handle_cloudflare_verification(self):
        """Handle Cloudflare verification with better detection and waiting"""
        try:
            # Try different methods to detect Cloudflare
            cloudflare_detected = False
            
            # Method 1: Look for the iframe
            try:
                cloudflare_frame = self.driver.find_element(By.CSS_SELECTOR, 
                    "iframe[title='Widget containing a Cloudflare security challenge']")
                cloudflare_detected = True
                logger.info("Cloudflare verification detected via iframe")
            except NoSuchElementException:
                pass
                
            # Method 2: Look for the checkbox
            if not cloudflare_detected:
                try:
                    frames = self.driver.find_elements(By.TAG_NAME, "iframe")
                    for frame in frames:
                        try:
                            self.driver.switch_to.frame(frame)
                            checkbox = self.driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                            cloudflare_detected = True
                            logger.info("Cloudflare verification detected via checkbox")
                            break
                        except:
                            self.driver.switch_to.default_content()
                except:
                    self.driver.switch_to.default_content()
            
            # If Cloudflare is detected, wait for manual intervention
            if cloudflare_detected:
                print("\n" + "*" * 80)
                print("* CLOUDFLARE VERIFICATION DETECTED!")
                print("* Please complete the 'Verify you are human' check manually.")
                print("* The script will wait for 45 seconds while you do this.")
                print("* After checking the box, wait for the page to fully load.")
                print("*" * 80 + "\n")
                
                # Switch back to main content
                self.driver.switch_to.default_content()
                
                # Wait for manual verification
                time.sleep(45)
                
                # Make sure we're back on the main content
                self.driver.switch_to.default_content()
                logger.info("Waited for Cloudflare verification")
        except Exception as e:
            logger.warning(f"Error while handling Cloudflare: {e}")
            # Switch back to main content in case of error
            self.driver.switch_to.default_content()
    
    def human_like_typing(self, element, text):
        """Type text in a human-like manner with random delays between keystrokes"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.25))  # Random delay between keystrokes
    
    def random_delay(self, min_seconds, max_seconds):
        """Add a random delay to mimic human behavior"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def logout(self):
        """Log out from Upwork"""
        if not self.is_logged_in or not self.driver:
            return False
            
        try:
            # Click on the user menu to reveal the logout option
            user_menu = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.up-avatar"))
            )
            user_menu.click()
            logger.info("Clicked on user menu")
            
            # Click on the logout button
            logout_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log out')]"))
            )
            logout_link.click()
            logger.info("Clicked on logout button")
            
            # Wait for logout to complete
            time.sleep(3)
            
            self.is_logged_in = False
            logger.info("Successfully logged out from Upwork")
            return True
        except Exception as e:
            logger.error(f"Error during logout process: {e}")
            return False
            
    def close(self):
        """Close the browser and clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Browser closed")