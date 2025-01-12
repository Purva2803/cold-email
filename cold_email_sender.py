import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import time
from email.utils import formataddr, formatdate
import uuid

class ColdEmailSender:
    def __init__(self):
        self.SCOPES = [
            'https://mail.google.com/',  # Full access to Gmail
            'https://www.googleapis.com/auth/gmail.settings.basic',
            'https://www.googleapis.com/auth/gmail.settings.sharing'
        ]
        self.creds = None

    def authenticate(self):
        """Handles Gmail API authentication"""
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        return build('gmail', 'v1', credentials=self.creds)

    def create_message_with_attachment(self, sender, to, subject, message_text, resume_path):
        """Creates an email message with attachment and proper headers"""
        message = MIMEMultipart('mixed')
        
        # Proper email headers for authentication
        message['Message-ID'] = f"<{uuid.uuid4()}@gmail.com>"
        message['Date'] = formatdate(localtime=True)
        message['To'] = to
        message['From'] = formataddr(("Your Name", sender))  # Replace with your name
        message['Subject'] = subject
        message['MIME-Version'] = '1.0'
        
        # Create the body
        body = MIMEMultipart('alternative')
        
        # Plain text version
        text_part = MIMEText(message_text, 'plain', 'utf-8')
        body.attach(text_part)
        
        # HTML version
        html_content = message_text.replace('\n', '<br>')
        html_part = MIMEText(f"<html><body>{html_content}</body></html>", 'html', 'utf-8')
        body.attach(html_part)
        
        message.attach(body)

        # Add resume attachment
        if resume_path and os.path.exists(resume_path):
            with open(resume_path, 'rb') as f:
                attachment = MIMEApplication(f.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', 'attachment', 
                                   filename=os.path.basename(resume_path))
                message.attach(attachment)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_email(self, service, sender, to, subject, message_text, resume_path):
        """Sends an email"""
        try:
            message = self.create_message_with_attachment(
                sender, to, subject, message_text, resume_path)
            sent_message = service.users().messages().send(
                userId='me', body=message).execute()
            print(f'Message Id: {sent_message["id"]} sent to {to}')
            return True
        except Exception as e:
            print(f'An error occurred while sending email to {to}: {str(e)}')
            return False

    def send_bulk_emails(self, email_list, subject, message_text, resume_path, 
                        sender=None, delay=5):
        """Sends cold emails to a list of recipients"""
        service = self.authenticate()
        
        try:
            # Get the user's email address
            profile = service.users().getProfile(userId='me').execute()
            sender = profile['emailAddress']
        except HttpError as error:
            print(f'Error getting user profile: {error}')
            return {'total_sent': 0, 'total_failed': len(email_list)}

        success_count = 0
        failed_count = 0

        for email in email_list:
            if self.send_email(service, sender, email, subject, message_text, resume_path):
                success_count += 1
            else:
                failed_count += 1
            
            if len(email_list) > 1:
                time.sleep(delay)

        return {
            'total_sent': success_count,
            'total_failed': failed_count
        }

def main():
    sender = ColdEmailSender()
    
    # Example usage
    email_list = [
        'your.email@example.com'  # Replace with your email for testing
    ]

    subject = "Your Email Subject"
    message_text = """Dear Hiring Manager,

Your email content here.

Best regards,
Your Name"""
    
    resume_path = 'your_resume.pdf'  # Replace with your resume filename
    
    print(f"Total number of emails: {len(email_list)}")
    
    results = sender.send_bulk_emails(
        email_list=email_list,
        subject=subject,
        message_text=message_text,
        resume_path=resume_path,
        delay=5
    )
    
    print(f"\nEmail Campaign Results:")
    print(f"Successfully sent: {results['total_sent']}")
    print(f"Failed to send: {results['total_failed']}")

if __name__ == '__main__':
    main()