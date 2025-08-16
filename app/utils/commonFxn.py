#class for common functions
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException
from collections.abc import Iterable
import bcrypt
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
class CommonFxn:
    def sendEmail(self,email_dict:dict):
        msg = MIMEText(email_dict.get('body', ''))
        msg['Subject'] = email_dict.get('subject', '')
        msg['From'] = email_dict.get('from', settings.SMTP_USER)
        msg['To'] = email_dict.get('to')
    
        if not msg['To']:
            raise ValueError("Recipient email ('to') is required.")

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    
    
    # Function to hash a password
    def hash_password(self,password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    #### Function to check if a password matches the hash
    def check_password(self, stored_hash: str, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))