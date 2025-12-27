import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

MAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email: str, otp: str):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Email OTP Verification"
    message["From"] = f"TestGuru <{MAIL}>"
    message["To"] = to_email

    # HTML content matching your image
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #eee;">
        <div style="text-align: center; margin-bottom: 20px;">
          <h2 style="color: #0033ff;">Sign In to Your TestGuru Account</h2>
        </div>
        
        <p>Hi <strong>{to_email}</strong>,</p>
        
        <p>We noticed a request to sign in to your <strong>TestGuru</strong> account. To keep your access secure, please use the One-Time Password (OTP) below:</p>
        
        <div style="margin: 30px 0; text-align: center;">
          <div style="display: inline-block; padding: 15px 30px; border: 2px dashed #0033ff; border-radius: 10px; font-size: 32px; font-weight: bold; color: #0033ff; letter-spacing: 2px;">
            {otp}
          </div>
        </div>
        
        <p style="text-align: center;">This OTP will expire in <strong>5 minutes</strong>.</p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        
        <p style="font-size: 14px; color: #666;">
          With your subscription, you get <strong>all-access</strong> to every exam area, unlimited tests, detailed performance reports, and competitive leaderboards—so you can focus on preparing without limits.
        </p>
        
        <p style="font-size: 14px; color: #666;">
          If you didn't request this sign-in, you can safely ignore this email—your account remains secure.
        </p>
        
        <p style="font-size: 14px; color: #666;">
          Cheers,<br>
          TestGuru Team
        </p>
        
        <footer style="text-align: center; font-size: 12px; color: #999; margin-top: 30px;">
          © 2025 TestGuru. All rights reserved.
        </footer>
      </body>
    </html>
    """

    # Attach HTML to the message
    message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MAIL, PASSWORD)
            server.send_message(message)
        print(f"OTP email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")