import logging
import os
import sys
from login import LoginManager
import time
import traceback

# Configure logging with more detailed information
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("security_question_test.log"),
        logging.StreamHandler(sys.stdout)  # Explicitly log to stdout
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Print basic system info for debugging
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Script location: {os.path.abspath(__file__)}")
        
        # Upwork credentials
        username = "patra.dinesh@gmail.com"
        password = "NewP@ssw0rd"
        
        print("\n" + "*" * 80)
        print("* UPWORK AUTHENTICATION TEST WITH DEBUGGING")
        print("* Attempting to troubleshoot browser window not opening")
        print("*" * 80)
        
        # Initialize the login manager
        logger.info("Initializing LoginManager")
        login_manager = LoginManager(username, password)
        
        # Try to initialize the driver only
        logger.info("Explicitly trying to initialize the driver")
        driver_init_result = login_manager.initialize_driver()
        
        if not driver_init_result:
            logger.error("Failed to initialize WebDriver - browser window did not open")
            print("\nFailed to open browser window. Check the following:")
            print("1. Is Chrome installed on your system?")
            print("2. Is there enough memory available?")
            print("3. Check security_question_test.log for detailed error messages")
            return
        
        logger.info("WebDriver initialized successfully - browser should be open")
        print("\nBrowser window should now be open. If you can see it, type 'Y' below.")
        print("If you cannot see a browser window, type 'N'")
        
        user_response = input("Can you see the browser window? (Y/N): ").strip().upper()
        
        if user_response == 'Y':
            print("\nGood! Continuing with the login process...")
            # Proceed with login attempt
            login_manager.login_with_cloudflare_handling()
        else:
            print("\nBrowser window is not visible. Script will exit.")
            if login_manager.driver:
                login_manager.driver.quit()
            return
            
        print("\nScript completed. Browser window should remain open.")
        logger.info("Script completed successfully")
        
    except Exception as e:
        logger.error(f"Uncaught exception: {e}")
        logger.error(traceback.format_exc())  # Log the full traceback
        print(f"\nAn error occurred: {e}")
        print("Check security_question_test.log for details")

if __name__ == "__main__":
    main()