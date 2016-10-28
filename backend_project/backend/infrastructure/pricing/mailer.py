from infrastructure.mailer_adapter import MailerAdapter
from domain.mail.mail import Mail


class PricingMailer:

    @staticmethod
    def new(mailer=MailerAdapter.new(), mail=Mail):
        return PricingMailer(mailer, mail)

    def __init__(self, mailer, mail):
        self.mail = mail
        self.mailer = mailer

    def contact_about_enterprise(self, message, to_email):
        client = self.mail.new("Confirm email was delivered", "Your email was delivered", to_email)
        admin = self.mail.new("Contact about enterprise", message, "hello@nextchef.co")

        self.send_email(client)
        self.send_email(admin)

    def send_email(self, mail):
        self.mailer.send_email(mail)
