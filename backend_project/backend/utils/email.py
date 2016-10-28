from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, get_urlconf, set_urlconf
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext as _

from registration.models import RegistrationProfile
from emailing.models import EmailingList


def subscribe_sendy(chef):
    """
    Subscribe chef to sendy mailing lists
    """
    try:
        EmailingList.objects.subscribe_chef(chef)
        return True
    except:
        return False


def send_activation_email(chef):
    """
    Send activation email to new user
    """
    cur_language = translation.get_language()
    translation.activate(chef.language)

    cur_urlconf = get_urlconf()
    set_urlconf('backend.urls')

    site = Site.objects.get_current()
    registration_profile = RegistrationProfile.objects.create_profile(chef)
    registration_profile.send_activation_email(site)

    set_urlconf(cur_urlconf)
    translation.activate(cur_language)


def send_welcome_email(chef):
    """
    Send welcome email to new user registered via FB
    """
    cur_language = translation.get_language()
    translation.activate(chef.language)

    cur_urlconf = get_urlconf()
    set_urlconf('backend.urls')

    site = Site.objects.get_current()
    registration_profile = RegistrationProfile.objects.create_profile(chef)
    RegistrationProfile.objects.activate_user(registration_profile.activation_key, site)

    set_urlconf(cur_urlconf)
    translation.activate(cur_language)


def send_reset_password_email(chef):
    """
    Send reset password email with link to user
    """
    cur_language = translation.get_language()
    translation.activate(chef.language)

    subject = _('Reset password')
    subject = ' '.join(subject.splitlines())

    site = Site.objects.get_current()
    link = reverse('auth_password_reset', 'backend.urls')
    ctx = {'site': site, 'link': link}
    message = render_to_string('emails/reset_password.txt', ctx)
    chef.email_user(subject, message, 'info@nextchef.co')

    translation.activate(cur_language)


def send_report_recipe_email(report):
    """
    Send reset password email with link to user
    """
    subject = 'Receta marcada como inapropiada'
    ctx = {'report': report}
    message = render_to_string('emails/report_recipe.txt', ctx)
    send_mail(subject, message, 'no-reply@nextchef.co', ['info@nextchef.co'])
