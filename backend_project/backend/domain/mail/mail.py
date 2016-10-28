
class InvalidMailException(Exception):
    pass

class Mail:
    @staticmethod
    def new(subject, message, to_email, from_email="no-reply@nextchef.co"):
        return Mail(subject, message, to_email, from_email)

    def __init__(self, subject, message, to_email, from_email):

        if not subject or not message:
            raise InvalidMailException("subject: %s, message: %s" % (subject, message))

        if not validateEmail(to_email) or not validateEmail(from_email):
            raise InvalidMailException("to_email: %s, from_email %s" % (to_email, from_email))

        self.subject = subject
        self.message = message
        self.to_email = to_email
        self.from_email = from_email


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
