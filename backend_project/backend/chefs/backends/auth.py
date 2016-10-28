
from django.contrib.auth.models import User, check_password
from chefs.models import Chefs

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """
    
    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = Chefs.objects.filter(email=username)[0]
            #user = Chefs.objects.get(email=username)
            if user.check_password(password):
                return user
        except:
            return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return Chefs.objects.get(pk=user_id)
        except Chefs.DoesNotExist:
            return None