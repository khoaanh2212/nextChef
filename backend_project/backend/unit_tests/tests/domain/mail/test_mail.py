import unittest

from domain.mail.mail import Mail, InvalidMailException

class MailTest(unittest.TestCase):

    valid_email = "email@email.com"
    valid_subject = "subject"
    valid_message = "message"

    def test_new_should_throw_on_white_subject(self):
        with self.assertRaises(InvalidMailException):
            Mail.new("", self.valid_message, self.valid_email)

    def test_new_should_throw_on_white_message(self):
        with self.assertRaises(InvalidMailException):
            Mail.new(self.valid_subject, "", self.valid_email)

    def test_new_should_throw_on_invalid_to_email(self):
        with self.assertRaises(InvalidMailException):
            Mail.new(self.valid_subject, self.valid_message, "im not an email")

    def test_new_should_throw_on_invalid_from_email(self):
        with self.assertRaises(InvalidMailException):
            Mail.new(self.valid_subject, self.valid_message, self.valid_email, "im not an email")

