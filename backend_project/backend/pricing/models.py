"""import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Enterprise(object):

    @staticmethod
    def send_email(subject, message, recipient):

        from_email = "no-reply@nextchef.co"
        to_email = recipient

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = recipient
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("email@example.com", "password")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

    def send_email_to_admin(self, subject, message):
        recipient = 'info@nextchef.io'
        return self.send_email(subject, message, recipient)

    def confirm_email_delivered(self, recipient):
        subject = 'Confirm email was delivered'
        message = 'Your email was delivered'
        return self.send_email(subject, message, recipient)
"""