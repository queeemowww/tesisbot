import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
import poplib
load_dotenv()

EMAIL_LOGIN = os.getenv('EMAIL_LOGIN')
GOOGLE_APPPASS = os.getenv("GOOGLE_APPPASS")
EMAIL_RECEPIENT = os.getenv("EMAIL_RECEPIENT")


class Send_order():
    def __init__(self):
        self.smtp = smtplib.SMTP('smtp.gmail.com', port=587)
        self.smtp.connect("smtp.gmail.com", 587)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(EMAIL_LOGIN, GOOGLE_APPPASS)
        # smtp.quit()
    
    async def send_mail(self, message):
        msg = MIMEText(message)
        msg['Subject'] = 'TG Запрос доставки'
        msg['From'] = EMAIL_LOGIN
        msg['To'] = EMAIL_RECEPIENT
        self.smtp.sendmail(EMAIL_LOGIN, EMAIL_RECEPIENT, msg.as_string())
# if __name__ == '__main__':
#     email = Send_order()
#     email.send_mail('blyadi')