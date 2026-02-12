import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from ..config import Config

class EmailSender:
    def __init__(self):
        self.api_key = Config.SENDGRID_API_KEY
        self.from_email = Config.SENDGRID_FROM_EMAIL
        self.sg = sendgrid.SendGridAPIClient(api_key=self.api_key) if self.api_key else None

    def send(self, to_email, subject, content):
        """
        Send an email using SendGrid.
        """
        if Config.ANTIGRAVITY_FLIGHT:
            print(f"🚀 [FLIGHT MODE] Sending email to {to_email}")
            print(f"Subject: {subject}")
            print(f"Content: {content[:100]}...")
            return True

        if not self.sg:
            print("SendGrid API Key missing. Cannot send.")
            return False

        # Add signature
        content += "\n\nPS: import antigravity"

        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            html_content=content
        )

        try:
            response = self.sg.send(message)
            return response.status_code in (200, 201, 202)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
