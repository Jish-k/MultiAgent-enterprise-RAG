import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

# Load from environment variables
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

def send_otp_email(email: str, otp: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"\n{'='*40}")
        print(f"[Warning] SMTP_USER or SMTP_PASSWORD not set in .env. Falling back to mock email.")
        print(f"MOCK EMAIL: To {email}, OTP {otp}")
        print(f"{'='*40}\n")
        return True

    msg = MIMEMultipart()
    msg['From'] = f"Agentic RAG <{SMTP_USER}>"
    msg['To'] = email
    msg['Subject'] = "Your Agentic RAG Login Code"
    
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Agentic RAG Login</h2>
        <p>Your one-time password (OTP) is:</p>
        <h1 style="color: #0056b3; letter-spacing: 2px;">{otp}</h1>
        <p>This code will expire in 5 minutes. Do not share this code with anyone.</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[Success] Sent real OTP email to {email}")
        return True
    except Exception as e:
        print(f"[Error] Failed to send email to {email}: {e}")
        return False
