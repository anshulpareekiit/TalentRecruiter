#class for common functions
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException
from collections.abc import Iterable

import smtplib
from email.mime.text import MIMEText
from app.core.config import settings
class CommonFxn:
    """#check if object is iterable but not string
    def is_iterable(self,obj):
        return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))
    
    #convert response to json and return
    def responseToJSON(self,model,result):
        if not self.is_iterable(result):
            print('iera')
            resp = model.model_validate(result).model_dump() 
        else:
            print('im iterable but no iterable')
            resp = [model.model_validate(res).model_dump() for res in result]
        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
        """
    def sendEmail(email_dict:dict):
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