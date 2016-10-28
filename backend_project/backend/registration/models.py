import datetime
import hashlib
import random
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.signals import user_logged_in

from utils.common import get_ip, get_country_from_ip
from chefs.models import Chefs

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

try:
    from django.utils.timezone import now as datetime_now
except ImportError:
    datetime_now = datetime.datetime.now

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """

    def activate_user(self, activation_key, site):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, return the ``User``
        after activating.
        
        If the key is not valid or has expired, return ``False``.
        
        If the key is valid but the ``User`` is already active,
        return ``False``.
        
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_confirmed = True
                user.save()
                profile.activation_key = self.model.ACTIVATED
                profile.save()
                if user.bii != True:
                    profile.send_welcome_email(site)
                return user
        return False

    def create_active_user(self, name, surname, email, password, language, type, site, send_email=True, bii=False):
        """
        Create a new, active ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        
        """
        new_user = Chefs.objects.create_user(name, surname, email, password, type)
        new_user.is_active = True
        new_user.is_confirmed = False
        new_user.language = language
        new_user.bii = bii
        if bii == True:
            new_user.membership = 'business'
        new_user.save()

        registration_profile = self.create_profile(new_user)
        if send_email:
            registration_profile.send_activation_email(site)

        return new_user

    def create_active_facebook_user(self, name, surname, email, fb_user_id, fb_access_token, language, type, site,
                                    send_email=True):

        new_user = Chefs.objects.create_user(name, surname, email, None, type)
        new_user.is_active = True
        new_user.is_confirmed = True
        new_user.language = language
        new_user.fb_user_id = fb_user_id
        new_user.fb_access_token = fb_access_token
        new_user.save()

        registration_profile = self.create_profile(new_user)
        RegistrationProfile.objects.activate_user(registration_profile.activation_key, site)

        return new_user

    def create_profile(self, user):
        """s
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.
        
        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = hashlib.sha1(salt + username).hexdigest()
        return self.create(user=user,
                           activation_key=activation_key)

    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.
        
        """
        for profile in self.all():
            try:
                if profile.activation_key_expired():
                    user = profile.user
                    if not user.is_active:
                        user.delete()
                        profile.delete()
            except User.DoesNotExist:
                profile.delete()


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.
    
    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.
    
    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.
    
    """
    ACTIVATED = u"ALREADY_ACTIVATED"

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or (self.user.creation_date + expiration_date <= datetime_now())

    activation_key_expired.boolean = True

    def send_activation_email(self, site):
        """
        Send an activation email to the user associated with this
        ``RegistrationProfile``.
        
        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'user': self.user,
                    'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site}

        if self.user.language == 'es':
            subject = render_to_string('registration/activation_email_subject_es.txt',
                                       ctx_dict)
        else:
            subject = render_to_string('registration/activation_email_subject.txt',
                                       ctx_dict)

        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        if self.user.language == 'es':
            message = render_to_string('registration/activation_email_es.html',
                                       ctx_dict)
        else:
            message = render_to_string('registration/activation_email.html',
                                       ctx_dict)

        self.user.html_email_user(subject, message, settings.DEFAULT_FROM_EMAIL)

    def send_welcome_email(self, site):
        """
        Send onboarding email after activation email is confirmed or when user registers via FB
        :param site:
        :return: None
        """
        ctx_dict = {'user': self.user,
                    'site': site}

        if self.user.language == 'es':
            subject = render_to_string('registration/welcome_email_subject_es.txt', ctx_dict)
        else:
            subject = render_to_string('registration/welcome_email_subject.txt', ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        if self.user.language == 'es':
            message = render_to_string('registration/welcome_email_es.html',
                                       ctx_dict)
        else:
            message = render_to_string('registration/welcome_email.html',
                                       ctx_dict)

        self.user.html_email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


def check_country(sender, user, request, **kwargs):
    # Try to determine user's country from his IP address
    if user.country is None:
        ip = get_ip(request)
        user.country = get_country_from_ip(ip)
        user.save()


user_logged_in.connect(check_country)