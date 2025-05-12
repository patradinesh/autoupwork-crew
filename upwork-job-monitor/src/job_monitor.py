import time
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Job:
    def __init__(self, title, link, description, posted_time, budget=None):
        self.title = title
        self.link = link
        self.description = description
        self.posted_time = posted_time
        self.budget = budget
        self.found_at = datetime.now()
    
    def __str__(self):
        return f"Job: {self.title} (Posted: {self.posted_time})\nBudget: {self.budget}\nLink: {self.link}"

class JobMonitor:
    def __init__(self, login_manager, notification_service, search_keywords=None):
        self.login_manager = login_manager
        self.notification_service = notification_service
        self.search_keywords = search_keywords or ["DevOps", "Docker", "Kubernetes", "AWS", "CI/CD", "Jenkins", "Terraform"]
        self.last_job_ids = set()  # Keep track of job IDs we've already seen
        self.search_url = "https://www.upwork.com/nx/jobs/search/?q=DevOps&sort=recency"
    
    def start_monitoring(self, interval_seconds=300):
        """Start monitoring for new jobs at specified interval"""
        logger.info(f"Starting job monitoring with interval of {interval_seconds} seconds")
        
        while True:
            new_jobs = self.check_for_new_jobs()
            if new_jobs:
                logger.info(f"Found {len(new_jobs)} new DevOps jobs")
                for job in new_jobs:
                    if self.notification_service:
                        self.notification_service.send_notification(job)
            else:
                logger.info("No new jobs found")
                
            logger.info(f"Waiting {interval_seconds} seconds until next check...")
            time.sleep(interval_seconds)

    def check_for_new_jobs(self):
        """Check for new DevOps-related job postings"""
        if not self.login_manager or not self.login_manager.driver:
            logger.error("Login manager or driver not initialized")
            return []
            
        try:
            logger.info(f"Navigating to search URL: {self.search_url}")
            self.login_manager.driver.get(self.search_url)
            
            # Wait for the job results to load
            WebDriverWait(self.login_manager.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.job-tile"))
            )
            
            # Get all job listings on the page
            job_listings = self.login_manager.driver.find_elements(By.CSS_SELECTOR, "section.job-tile")
            logger.info(f"Found {len(job_listings)} job listings on the page")
            
            new_jobs = []
            current_job_ids = set()
            
            for job_listing in job_listings:
                try:
                    # Extract job ID to track if we've seen this job before
                    job_id = job_listing.get_attribute("data-job-id") or job_listing.get_attribute("id")
                    current_job_ids.add(job_id)
                    
                    # Skip if we've already seen this job
                    if job_id in self.last_job_ids:
                        continue
                    
                    # Extract job details
                    title_element = job_listing.find_element(By.CSS_SELECTOR, "h2 a")
                    title = title_element.text.strip()
                    link = title_element.get_attribute("href")
                    
                    # Check if job title contains any of our target keywords
                    if not any(keyword.lower() in title.lower() for keyword in self.search_keywords):
                        continue
                    
                    # Extract job description
                    try:
                        description = job_listing.find_element(By.CSS_SELECTOR, ".job-description-text").text.strip()
                    except NoSuchElementException:
                        description = "No description available"
                    
                    # Extract posted time
                    try:
                        posted_time = job_listing.find_element(By.CSS_SELECTOR, "span.job-created-at").text.strip()
                    except NoSuchElementException:
                        posted_time = "Unknown"
                    
                    # Extract budget if available
                    try:
                        budget = job_listing.find_element(By.CSS_SELECTOR, ".up-budget span").text.strip()
                    except NoSuchElementException:
                        budget = "Not specified"
                    
                    # Create a Job object and add to our list of new jobs
                    job = Job(title, link, description, posted_time, budget)
                    new_jobs.append(job)
                    logger.info(f"Found new job: {title}")
                
                except Exception as e:
                    logger.error(f"Error parsing job listing: {e}")
                    continue
            
            # Update our tracking set with the current job IDs
            self.last_job_ids = current_job_ids
            
            return new_jobs
            
        except TimeoutException:
            logger.error("Timeout while waiting for job listings to load")
            return []
        except Exception as e:
            logger.error(f"Error checking for new jobs: {e}")
            return []
    
    def search_by_keyword(self, keyword):
        """Perform a search for jobs with a specific keyword"""
        search_url = f"https://www.upwork.com/nx/jobs/search/?q={keyword}&sort=recency"
        self.search_url = search_url
        return self.check_for_new_jobs()