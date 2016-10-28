import urllib
import json
import smtplib

from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth import login
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from registration import signals
from registration.views import ActivationView as BaseActivationView
from registration.views import RegistrationView as BaseRegistrationView
from registration.forms import SignUpFacebookForm, LoginFacebookForm
from registration.models import RegistrationProfile

from chefs.models import Chefs
from recipe.models import Photos
from library.views import library
from explore.views import recommended

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from premailer import transform
from django.core.mail.message import EmailMultiAlternatives
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse





def connectFacebookCallback(request):
    pass


def registrationActivateComplete(request):
    return recommended(request, activation_complete=True)


def signupComplete(request):
    return HttpResponseRedirect(reverse('explore'))
    # return recommended(request, nux=True)


def signupCompleteFacebook(request):
    return recommended(request, nux=True)


def signupFacebookCallback(request):
    if request.method == 'POST':
        form = SignUpFacebookForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            picture = form.cleaned_data['picture']
            type = form.cleaned_data['type']
            fb_user_id = form.cleaned_data['user_id']
            fb_access_token = form.cleaned_data['token']
            language = request.LANGUAGE_CODE

            profile = json.load(
                urllib.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=fb_access_token))))
            callback_user_id = profile["id"]

            if fb_user_id != callback_user_id:
                return HttpResponseForbidden()

            chefs = Chefs.objects.filter(email=email)
            if chefs.count() != 0:
                chef = chefs[0]
                chef.fb_user_id = fb_user_id
                chef.fb_access_token = fb_access_token
                chef.save()
                chef.backend = 'chefs.backends.auth.EmailAuthBackend'
                login(request, chef)

            else:
                if Site._meta.installed:
                    site = Site.objects.get_current()
                else:
                    site = RequestSite(request)
                new_user = RegistrationProfile.objects.create_active_facebook_user(first_name, last_name, email,
                                                                                   fb_user_id, fb_access_token,
                                                                                   language, type, site)
                new_user.backend = 'chefs.backends.auth.EmailAuthBackend'
                login(request, new_user)
                chef = new_user

            try:
                chef.set_photo_from_facebook_url(picture)
            except Exception, e:
                pass

            return redirect(reverse('registration_complete_facebook'))

        else:
            return HttpResponseRedirect(reverse('registration_register'))
    else:
        return HttpResponseRedirect(reverse('registration_register'))


def loginFacebook(request):
    if request.method == "POST":
        form = LoginFacebookForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user_id = form.cleaned_data['user_id']
            token = form.cleaned_data['token']
            profile = json.load(
                urllib.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=token))))
            user_id_face = profile["id"]

            if user_id != user_id_face:
                return HttpResponseForbidden()

            chefs = Chefs.objects.filter(fb_user_id=user_id)

            if chefs.count() > 0:
                chef = chefs[0]

                if chef.is_active:
                    chef.backend = 'chefs.backends.auth.EmailAuthBackend'
                    login(request, chef)

                    try:
                        photos = Photos.objects.filter(chef=chef)[:1]
                        if photos.count() == 0:
                            picture = request.POST.get('picture')
                            chef.set_photo_from_facebook_url(picture)
                    except Exception, e:
                        pass

                    # TODO: Set chef language when logging
                    return redirect(reverse('library', kwargs={'slug': chef.slug, 'id': chef.id}))

                else:
                    return HttpResponseRedirect(reverse('login_not_allowed'))
            else:
                return signupFacebookCallback(request)
        else:
            return HttpResponseRedirect(reverse('auth_login'))
    else:
        return HttpResponseRedirect(reverse('auth_login'))


class RegistrationView(BaseRegistrationView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.
    
    """

    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        name, surname, email, password, type = cleaned_data['name'], cleaned_data['surname'], cleaned_data['email'], \
                                               cleaned_data['password1'], cleaned_data['type']
        bii = request.POST.get('bii')
        if bii == 'true':
            bii = bool(bii)
        language = request.LANGUAGE_CODE[0:2]
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        if bii == True:
            new_user = RegistrationProfile.objects.create_active_user(name, surname, email,
                                                                      password, language, type, site,bii=bii, send_email=False)
        else:
            new_user = RegistrationProfile.objects.create_active_user(name, surname, email,
                                                                      password, language, type, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        # send mail

        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login("apiumtechtest@gmail.com", "tobuildornottobuild00")

        # msg = "Your account is created."
        # server.sendmail("apiumtechtest@gmail.com", '%s' % cleaned_data['email'], msg)
        # server.quit()

        # end send mail
        new_user.backend = 'chefs.backends.auth.EmailAuthBackend'
        login(request, new_user)

        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.
        
        """
        return ('registration_complete', (), {})


class ActivationView(BaseActivationView):
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.
        
        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        activated_user = RegistrationProfile.objects.activate_user(activation_key, site)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('registration_activation_complete', (), {})

def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None):


    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


class CustomPasswordResetForm(PasswordResetForm):

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = render_to_string(email_template_name, c)
            inlined_mail = transform(email)
            mail = EmailMultiAlternatives(subject, '', settings.SERVER_EMAIL, [user.email], )
            mail.attach_alternative(inlined_mail, 'text/html')
            mail.send(fail_silently=True)