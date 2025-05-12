import time
import os
import logging
import argparse
from login import LoginManager
from job_monitor import JobMonitor
from notification import NotificationService
from utils.config import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("upwork_monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Upwork DevOps Job Monitor')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--interval', type=int, help='Check interval in seconds')
    parser.add_argument('--keywords', type=str, help='Comma-separated search keywords')
    return parser.parse_args()

def main():
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load configuration settings
        config_path = args.config or os.path.join(project_root, 'config', 'settings.json')
        config = load_config(config_path)
        
        # Override config with command line arguments if provided
        if args.interval:
            config['check_interval'] = args.interval
            
        # Set up search keywords if provided
        search_keywords = None
        if args.keywords:
            search_keywords = [kw.strip() for kw in args.keywords.split(',')]
            
        # Validate required configs
        if not config.get('upwork_username') or not config.get('upwork_password'):
            logger.error("Upwork credentials not found. Please set UPWORK_USERNAME and UPWORK_PASSWORD environment variables.")
            return
            
        if not config.get('notification_email'):
            logger.warning("Notification email not configured. Set NOTIFICATION_EMAIL environment variable for email alerts.")

        # Initialize the notification service
        notification_service = NotificationService(
            email_sender=config.get('email_sender'),
            email_password=config.get('email_password'),
            smtp_server=config.get('smtp_server'),
            smtp_port=config.get('smtp_port')
        )
        
        # Initialize the login manager
        login_manager = LoginManager(config['upwork_username'], config['upwork_password'])
        
        # Log in to Upwork
        logger.info("Attempting to log in to Upwork...")
        if login_manager.login():
            logger.info("Logged in to Upwork successfully.")
            
            # Initialize the job monitor with login_manager and notification_service
            job_monitor = JobMonitor(login_manager, notification_service, search_keywords)
            
            # Start monitoring with specified interval
            interval = int(config.get('check_interval', 300))
            logger.info(f"Starting job monitoring with {interval} seconds interval")
            
            try:
                job_monitor.start_monitoring(interval)
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user.")
            finally:
                # Clean up resources
                logger.info("Cleaning up resources...")
                login_manager.close()
        else:
            logger.error("Upwork login failed. Please check your credentials.")
    
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main()