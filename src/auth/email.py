import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")

def send_email(to, subject, body):
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = MAIL_USERNAME
    msg['To'] = to
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [to], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f'Email error: {e}')
        return False

def send_verification(email, username, code):
    body = f'''
    <h2>Welcome to DocGen, {username}!</h2>
    <p>Your verification code: <strong>{code}</strong></p>
    <p>Enter this code to verify your account.</p>
    '''
    return send_email(email, 'DocGen - Verify your account', body)

def send_reset_password(email, username, token):
    body = f'''
    <h2>Password Reset - DocGen</h2>
    <p>Hello {username},</p>
    <p>Use this token to reset your password: <strong>{token}</strong></p>
    '''
    return send_email(email, 'DocGen - Reset Password', body)
