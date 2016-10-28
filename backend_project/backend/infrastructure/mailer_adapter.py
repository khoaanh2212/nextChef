import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class MailerAdapter:
    @staticmethod
    def new(
            _smtplib=smtplib,
            mime_multipart=MIMEMultipart,
            mime_text=MIMEText,
            mandrill=EmailMultiAlternatives,
            logger=logging.getLogger('mailer')):
        return MailerAdapter(_smtplib, mime_multipart, mime_text, mandrill, logger)

    def __init__(self, _smtplib, mime_multipart, mime_text, mandrill, logger):
        self.smtplib = _smtplib
        self.MIMEMultipart = mime_multipart
        self.MIMEText = mime_text
        self.mandrill = mandrill
        self.logger = logger


    def send_email(self, mail, is_html=False):
        from_email = mail.from_email
        to_email = mail.to_email

        msg = self.MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = mail.subject

        body = mail.message

        if is_html:
            msg.attach(self.MIMEText(body, 'html'))
        else:
            msg.attach(self.MIMEText(body, 'plain'))

        server = self.smtplib.SMTP(settings.EMAIL_HOST, 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)  # Need change to real email
        text = msg.as_string()

        self.logger.info('email sent: From "%s", To "%s", Subject "%s"' % (from_email, to_email, mail.subject))
        self.logger.debug(text)
        server.sendmail(from_email, to_email, text)

    def send_mandrill_email(self, mail, template_name=''):

        msg = self.mandrill(
            subject=mail.subject,
            body=mail.message,
            from_email=mail.from_email,
            to=[mail.to_email]
        )
        msg.attach_alternative("<p>This is the HTML email body</p>", "text/html")

        msg.send()

        self.logger.info('mandrill email sent: To "%s", Subject "%s"' % (mail.to_email, mail.subject))
        self.logger.debug(mail.message)
