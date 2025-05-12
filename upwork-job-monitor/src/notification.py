import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, email_sender=None, email_password=None, smtp_server=None, smtp_port=None):
        # Get email settings from environment variables or use provided values
        self.email_sender = email_sender or os.environ.get('EMAIL_SENDER')
        self.email_password = email_password or os.environ.get('EMAIL_PASSWORD')
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.environ.get('SMTP_PORT', 587))
        
    def send_email(self, recipient, subject, message, html_content=None, attachments=None):
        """
        Send an email with optional HTML content and attachments
        
        Args:
            recipient: Email address of the recipient
            subject: Subject of the email
            message: Plain text message
            html_content: Optional HTML content of the email
            attachments: Optional list of file paths to attach
        """
        if not self.email_sender or not self.email_password:
            logger.error("Email sender or password not configured")
            return False
            
        try:
            # Create a multipart message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_sender
            msg['To'] = recipient
            
            # Add plain text part
            text_part = MIMEText(message, 'plain')
            msg.attach(text_part)
            
            # Add HTML part if provided
            if html_content:
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)
                
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    try:
                        with open(file_path, 'rb') as file:
                            attachment = MIMEApplication(file.read())
                            attachment.add_header('Content-Disposition', 'attachment', 
                                                 filename=os.path.basename(file_path))
                            msg.attach(attachment)
                    except Exception as e:
                        logger.error(f"Error attaching file {file_path}: {e}")
            
            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_sender, self.email_password)
            
            # Send the email
            server.sendmail(self.email_sender, recipient, msg.as_string())
            server.quit()
            
            logger.info(f"Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_notification(self, job):
        """
        Send a notification for a new job
        
        Args:
            job: A Job object with details about the job posting
        """
        # Get notification email from environment
        recipient = os.environ.get('NOTIFICATION_EMAIL')
        if not recipient:
            logger.error("Notification email not configured")
            return False
            
        # Create email subject
        subject = f"New Upwork DevOps Job: {job.title}"
        
        # Create plain text message
        message = f"""
New DevOps job found on Upwork:

Title: {job.title}
Posted: {job.posted_time}
Budget: {job.budget}

Description:
{job.description[:500]}{'...' if len(job.description) > 500 else ''}

View job: {job.link}

This notification was sent by Upwork Job Monitor.
        """
        
        # Create HTML version of the message
        html_content = f"""
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #14a800; color: white; padding: 10px; text-align: center; }}
        .content {{ padding: 20px; background-color: #f9f9f9; }}
        .job-title {{ color: #14a800; font-size: 18px; font-weight: bold; }}
        .job-meta {{ color: #666; margin: 10px 0; }}
        .job-description {{ margin: 20px 0; }}
        .cta-button {{ display: inline-block; background-color: #14a800; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 4px; }}
        .footer {{ font-size: 12px; color: #999; margin-top: 30px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>New DevOps Job on Upwork</h2>
        </div>
        <div class="content">
            <div class="job-title">{job.title}</div>
            <div class="job-meta">
                <strong>Posted:</strong> {job.posted_time}<br>
                <strong>Budget:</strong> {job.budget}
            </div>
            <div class="job-description">
                <strong>Description:</strong><br>
                {job.description[:500]}{'...' if len(job.description) > 500 else ''}
            </div>
            <a href="{job.link}" class="cta-button">View Job</a>
        </div>
        <div class="footer">
            This notification was sent by Upwork Job Monitor.
        </div>
    </div>
</body>
</html>
        """
        
        return self.send_email(recipient, subject, message, html_content)
        
    def send_sms(self, phone_number, message):
        """
        Send an SMS notification (placeholder for future implementation)
        
        Args:
            phone_number: The recipient's phone number
            message: The SMS message text
        
        Note: This is a placeholder. To implement SMS functionality,
        you would need to integrate with an SMS service provider like Twilio.
        """
        # This is a placeholder for SMS sending logic
        logger.info(f"SMS would be sent to {phone_number}: {message}")
        return True