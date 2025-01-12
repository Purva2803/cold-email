# Cold Email Script

A Python script for sending professional cold emails using Gmail API.

## Setup

1. Create Google Cloud Project:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download credentials.json

2. Clone the repository:
   ```bash
   git clone https://github.com/Purva2803/cold-email-script.git
   cd cold-email-script
   ```

3. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

5. Setup credentials:
   - Place credentials.json in the project directory
   - Place your resume PDF in the project directory
   - Run the script first time to authenticate:
     ```bash
     python cold_email_sender.py
     ```

## Features
- Sends personalized cold emails with proper authentication
- Supports PDF attachments
- Bulk email sending with configurable delays
- Uses Gmail API for reliable delivery

## Usage
1. Update the email list in cold_email_sender.py
2. Customize the email message
3. Run the script:
   ```bash
   python cold_email_sender.py
   ```

## Note
Make sure to keep your credentials.json and token.pickle secure and never commit them to Git.