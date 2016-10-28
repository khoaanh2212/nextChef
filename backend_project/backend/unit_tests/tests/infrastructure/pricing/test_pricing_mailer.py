import unittest
import mock

from infrastructure.pricing.mailer import PricingMailer

class PricingMailerTest(unittest.TestCase):

    def setUp(self):
        self.mailerStub = mock.MagicMock(name='send_email')
        self.sut = PricingMailer.new(mailer=self.mailerStub)

    valid_email = "email@email.com"
    valid_message = "message"

    def exercise_contact_about_enterprise(self, email=None):
        email = email or self.valid_email
        self.sut.contact_about_enterprise(self.valid_message, email)

    def test_contact_about_enterprise_should_send_email(self):
        self.exercise_contact_about_enterprise()
        self.assertEqual(self.mailerStub.send_email.called, True)

    def test_contact_about_enterprise_should_call_send_email_two_time(self):
        self.exercise_contact_about_enterprise()
        self.assertEqual(self.mailerStub.send_email.call_count, 2)

    def test_contact_about_enterprise_should_contact_admin(self):
        admin_email = "hello@nextchef.co"
        self.exercise_contact_about_enterprise(admin_email)
        self.assertEqual(self.mailerStub.send_email.mock_calls[1][1][0].to_email, admin_email)

    def test_contact_about_enterprise_should_notify_client(self):
        client_email = "client@email.com"
        self.exercise_contact_about_enterprise(client_email)
        self.assertEqual(self.mailerStub.send_email.mock_calls[0][1][0].to_email, client_email)
