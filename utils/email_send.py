import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio

load_dotenv()

EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
GOOGLE_APPPASS = os.getenv("GOOGLE_APPPASS")
EMAIL_RECEPIENT = os.getenv("EMAIL_RECEPIENT")
EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")

class Send_order:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587
        self.username = EMAIL_LOGIN
        self.password = GOOGLE_APPPASS

    async def send_mail(self, message):
        msg = MIMEText(message)
        msg['Subject'] = 'TG Запрос доставки'
        msg['From'] = self.username
        msg['To'] = EMAIL_RECEPIENT

        smtp = SMTP(hostname=self.smtp_host, port=self.smtp_port, start_tls=True)

        try:
            await smtp.connect()
            await smtp.login(self.username, self.password)
            await smtp.send_message(msg)
        except Exception as e:
            print(f"[SMTP ERROR] {e}")
        finally:
            await smtp.quit()

# if __name__ == '__main__':
#     s = SendOrder()
#     asyncio.run(s.send_mail('HI'))
