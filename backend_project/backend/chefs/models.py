import datetime
import hashlib
import json
import binascii
import os
from random import choice
from string import ascii_lowercase, digits

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from django.contrib.sites.models import Site
from django.db.models.loading import get_model
from metrics.events import Events

from easy_thumbnails.templatetags.thumbnail import thumbnail_url

from utils import upload_to_random
from utils.common import get_ip, get_country_from_ip


class ChefsManager(BaseUserManager):
    def create_user(self, name, surname, email, password, type=0):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        errors = ''
        if not name:
            errors += 'Users must have name. '

        if not surname:
            errors += 'Users must have surname. '

        if not email:
            errors += 'Users must have an email address. '

        if not name or not email:
            raise ValueError(errors)

        if not surname:
            surname = ''

        type = 1
        user = self.model(
            email=ChefsManager.normalize_email(email),
            username=ChefsManager.normalize_email(email).split('@')[0],
            name=name,
            surname=surname,
            type=type,
            creation_date=now(),
            language='es',
            active=0,
            source='web',
            confirmation_email=0,
            cache_activity=0,
            cache_likes=0,
            cache_score=0,
            cache_activity_score=0,
            cache_recipes=0,
            cache_recipes_score=0,
            cache_photos_score=0,
            cache_photo_descriptions_score=0,
            cache_likes_score=0,
            noted=0,
            manual_score=0,
            final_score=0,
            email_newsletter=True,
            email_notifications=True

        )

        user.email_unsubscribe_hash = user.generate_random_email_hash(),

        if password is not None:
            user.set_password(password)

        user.save(using=self._db)

        model = get_model('emailing', 'EmailingList')
        model.objects.subscribe_chef(user)

        return user

    def create_superuser(self, email, password, name="Super", surname="User", type=0):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(name, surname, email, password, type=type)
        user.is_superuser = True
        user.is_confirmed = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def chefs_all(self):
        queryset = self.filter(cache_recipes__gte=1).order_by('-final_score')
        return queryset

    def chefs_pros(self):
        queryset = self.filter(type=1, cache_recipes__gte=1).order_by('-final_score')
        return queryset

    def chefs_foodies(self):
        queryset = self.filter(type=0, cache_recipes__gte=1).order_by('-final_score')
        return queryset

    def recommended(self, chef):
        query = self.filter(cache_recipes__gte=1)
        if not chef.is_anonymous():
            query = query.exclude(pk__in=chef.following.all())
        return query.order_by('-final_score')


class Chefs(AbstractBaseUser, PermissionsMixin):
    TYPE_FOODIE = 0
    TYPE_PRO = 1
    TYPE_BRAND = 2
    TYPE_CHOICES = (
        (TYPE_FOODIE, 'Foodie'),
        (TYPE_PRO, 'Pro'),
        (TYPE_BRAND, 'Brand'),
    )

    LANGUAGES_CHOICES = ('es', 'en', 'ca')
    ONBOARD_LANGUAGES_CHOICES = ('es', 'en', 'ca')

    MEMBERSHIP_DEFAULT = 'default'
    MEMBERSHIP_PRO = 'pro'
    MEMBERSHIP_BUSINESS = 'business'
    MEMBERSHIP_ENTERPRISE = 'enterprise'

    MEMBERSHIP = (
        (MEMBERSHIP_DEFAULT, 'Default'),
        (MEMBERSHIP_PRO, 'Pro'),
        (MEMBERSHIP_BUSINESS, 'Business'),
        (MEMBERSHIP_ENTERPRISE, 'Enterprise')
    )

    id = models.AutoField(primary_key=True)
    type = models.IntegerField(blank=True, null=True, default=TYPE_FOODIE, choices=TYPE_CHOICES)
    email = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=2)
    country = models.CharField(max_length=4, blank=True)
    location = models.CharField(max_length=200, blank=True)
    short_bio = models.CharField(max_length=255, blank=True)

    description = models.TextField(blank=True)
    role = models.CharField(max_length=127, blank=True)

    interests = models.CharField(max_length=200, blank=True)
    referents = models.CharField(max_length=200, blank=True)
    education = models.CharField(max_length=1000, blank=True)
    prev_restaurant = models.CharField(max_length=1024, blank=True)
    level = models.IntegerField(blank=True, null=True)

    active = models.BooleanField(default=True)
    private_recipes = models.BooleanField(default=False)
    offline = models.BooleanField(default=False)
    noted = models.BooleanField(default=False)

    cover = models.ImageField(upload_to=upload_to_random('chefs/'), blank=True, null=True)

    # Social
    fb_user_id = models.CharField(max_length=200, null=True, blank=True)
    fb_access_token = models.CharField(max_length=400, null=True, blank=True)
    fb_account = models.CharField(max_length=255, blank=True)
    tw_account = models.CharField(max_length=255, blank=True)
    personal_web_site = models.CharField(max_length=255, blank=True)
    web = models.CharField(max_length=255, blank=True)

    facebook_page = models.CharField(max_length=255, blank=True)
    twitter_page = models.CharField(max_length=255, blank=True)
    instagram_page = models.CharField(max_length=255, blank=True)
    pinterest_page = models.CharField(max_length=255, blank=True)
    google_plus_page = models.CharField(max_length=255, blank=True)
    linkedin_page = models.CharField(max_length=255, blank=True)

    email_notifications = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=True)
    email_unsubscribe_hash = models.CharField(max_length=50, blank=True)

    creation_date = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    edit_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    last_signin_date = models.DateTimeField(blank=True, null=True)

    following = models.ManyToManyField('self', through='ChefFollows', related_name='followers', symmetrical=False)

    cookbooth_page = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=50)
    confirmation_hash = models.CharField(max_length=50, blank=True)
    confirmation_email = models.BooleanField(default=False)

    manual_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    final_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    onboard_score = models.IntegerField(default=0)

    # These could (should?) be ManyToManyField fields instead
    languages = models.CharField(max_length=30, blank=True)
    onboard_languages = models.CharField(max_length=30, blank=True)

    # Cache
    cache_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_activity = models.IntegerField(default=0)
    cache_activity_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_recipes = models.IntegerField(default=0)
    cache_recipes_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_photos_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_photo_descriptions_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_likes_score = models.DecimalField(max_digits=7, decimal_places=4, default=0)
    cache_likes = models.IntegerField(default=0)
    membership = models.CharField(choices=MEMBERSHIP, max_length=255, default=MEMBERSHIP_DEFAULT)
    bii = models.BooleanField(default=False)
    # Required by AbstractBaseUser or contrib.admin
    USERNAME_FIELD = "email"
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    objects = ChefsManager()

    class Meta:
        app_label = 'chefs'
        db_table = 'chefs'
        verbose_name_plural = 'chefs'

    def is_chef(self):
        return self.type == self.TYPE_PRO

    def set_password(self, raw_password):
        self.password = hashlib.md5(raw_password).hexdigest()

    def check_password(self, raw_password):
        return self.password == hashlib.md5(raw_password).hexdigest()

    def api_set_password(self, raw_password):
        """
        Set user password as it comes from the apps
        """
        self.password = raw_password

    def api_check_password(self, raw_password):
        """
        Check user password as it comes from the apps
        """
        return self.password and self.password == raw_password

    def api_login(self, request):
        """
        Log in API user
        """
        # Try to determine user's country from his IP address
        if self.country is None:
            ip = get_ip(request)
            self.country = get_country_from_ip(ip)

        self.last_signin_date = now()
        self.last_login = self.last_signin_date
        self.save()

        self.auths_set.all().delete()
        auth = Auths.create(self, request)
        return auth.token

    def api_logout(self):
        """
        Log out API user
        """
        self.auths_set.all().delete()

    def has_usable_password(self):
        return True

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def html_email_user(self, subject, message, from_email=None):
        from premailer import transform
        from django.core.mail.message import EmailMultiAlternatives
        inlined_mail = transform(message)
        mail = EmailMultiAlternatives(subject, '', settings.SERVER_EMAIL, [self.email, ], )
        mail.attach_alternative(inlined_mail, 'text/html')
        mail.send(fail_silently=True)

    def get_full_name(self):
        # The user is identified by their email address
        full_name = ' '.join([self.name, self.surname])
        return full_name.strip() if full_name else ''

    def get_short_name(self):
        # The user is identified by their email address
        return self.name.strip()

    def __unicode__(self):
        return self.email

    def set_photo_from_facebook_url(self, image_url):

        import io
        import urllib
        from PIL import Image
        from django.core.files.storage import default_storage
        from recipe.models import Photos

        fd = urllib.urlopen(image_url + '?height=150')
        image_file = io.BytesIO(fd.read())
        im = Image.open(image_file)
        format = fd.headers.subtype
        path = self.slug + '-' + str(self.id) + '.' + format
        fh = default_storage.open(path, "w")
        im.save(fh, format)
        fh.close()
        photo = Photos.objects.create(
            creation_date=datetime.datetime.now(),
            edit_date=datetime.datetime.now(),
            chef=self,
            s3_url=settings.S3_URL + '/' + path
        )
        return photo

    @property
    def avatar(self):
        try:
            return self.avatar_photos.all()[:1][0].image
        except:
            return None

    @property
    def photo(self):
        try:
            return self.avatar_photos.all()[:1][0].s3_url.name
        except:
            return settings.STATIC_URL + 'img/cookbooth_avatar.jpg'

    @photo.setter
    def photo(self, image):
        try:
            photo = self.avatar_photos.all()[0]
            photo.photostyles_set.all().delete()
        except:
            photo = self.avatar_photos.create(chef=self)
        photo.s3_url = image
        photo.save()

    def cover_thumb(self, type):
        try:
            if self.cover:
                thumb = thumbnail_url(self.cover, type)
                return thumb
            else:
                best_recipe = self.best_recipe
                if best_recipe:
                    thumb = thumbnail_url(best_recipe.cover, type)
                    return thumb
                else:
                    return settings.STATIC_URL + 'img/chef_cover.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_cover.jpg'

    def avatar_thumb(self, type):
        try:
            if self.avatar:
                thumb = thumbnail_url(self.avatar, type)
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_avatar.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_avatar.jpg'

    @property
    def thumb_chefs_box(self):
        try:
            if self.cover:
                thumb = thumbnail_url(self.cover, 'chefs_box')
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_cover.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_cover.jpg'

    @property
    def thumb_chefs_nav_avatar(self):
        try:
            if self.avatar:
                thumb = thumbnail_url(self.avatar, 'base_nav_avatar')
                return thumb
            else:
                return settings.STATIC_URL + 'img/chef_avatar.jpg'
        except Exception, e:
            return settings.STATIC_URL + 'img/chef_avatar.jpg'

    @property
    def best_recipe(self):
        try:
            return self.recipes.all().filter(private=0, draft=0).order_by('-final_score')[:1][0]
        except:
            return None

    @property
    def top_rated_recipe(self):
        try:
            return self.recipes.all().order_by('-final_score')[:1][0]
        except:
            return ''

    @property
    def slug(self):
        return slugify(self.name + ' ' + self.surname)

    @property
    def full_name(self):
        return self.name + ' ' + self.surname

    @property
    def type_class(self):
        if self.type == self.TYPE_FOODIE or self.type is None:
            return 'foodie'
        elif self.type == self.TYPE_PRO:
            return 'pro'
        else:
            return 'brand'

    @property
    def url(self):
        return reverse('library', kwargs={'slug': self.slug, 'id': self.id})

    @property
    def site_url(self):
        site = Site.objects.get_current()
        return reverse('library', kwargs={'slug': self.slug, 'id': self.id})

    @property
    def public_url(self):
        site = Site.objects.get_current()
        return 'http//' + site.domain + reverse('library', kwargs={'slug': self.slug, 'id': self.id})

    @property
    def nb_followings(self):
        return self.following.count()

    @property
    def nb_followers(self):
        return self.followers.count()

    @property
    def nb_books(self):
        return self.books.count() + self.books_added.count()

    @property
    def nb_recipes(self):
        from recipe.models import ChefsHasRecipes

        own_recipes = self.recipes.filter(private=False, draft=False).count()
        copied_recipes = ChefsHasRecipes.objects.filter(chef=self,
                                                        recipe__draft=False,
                                                        recipe__private=False).count()
        return own_recipes + copied_recipes

    @property
    def nb_likes(self):
        likes = self.recipes.filter(private=False, draft=False).aggregate(Sum('nb_likes'))
        number = likes.get('nb_likes__sum', 0)
        return number if number else 0

    def generate_random_email_hash(self, length=40, chars=ascii_lowercase + digits, split=40, delimiter='-'):
        hash_token = ''.join([choice(chars) for i in xrange(length)])
        if split:
            hash_token = delimiter.join([hash_token[start:start + split] for start in range(0, len(hash_token), split)])
        chefs = Chefs.objects.filter(email_unsubscribe_hash=hash_token)
        if chefs.exists():
            return self.generate_random_email_hash(length=length, chars=chars, split=split, delimiter=delimiter)
        else:
            return hash_token

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        self.surname = self.surname.strip()
        super(Chefs, self).save(*args, **kwargs)

    def follows_to(self, chef):
        """
        Does self follows chef?
        """
        return ChefFollows.objects.filter(following=chef, follower=self).exists()

    def follow(self, chef):
        """
        Follow chef
        """
        try:
            follow = ChefFollows.objects.get(following=chef, follower=self)
            follow.save()  # Update edit_date
        except ChefFollows.DoesNotExist:
            ChefFollows.objects.create(following=chef, follower=self)

        Events.track(self.email, Events.EVENT_FOLLOW)

    def unfollow(self, chef):
        """
        Unfollow chef
        """
        ChefFollows.objects.filter(following=chef, follower=self).delete()

    def report_recipe(self, recipe):
        """
        Report recipe
        """
        pass

    @property
    def loves_list(self):
        loves = []
        for love in self.likes.all():
            loves.append(love.recipe_id)
        return loves

    @property
    def json_loves_list(self):
        loves = []
        for love in self.likes.all():
            loves.append(love.recipe_id)
        return json.dumps(loves)

    @property
    def follows_list(self):
        follows = []
        for follow in self.follows.all().order_by('following'):
            follows.append(follow.following_id)
        return follows

    @property
    def json_follows_list(self):
        follows = []
        for follow in self.follows.all().order_by('following'):
            follows.append(follow.following_id)
        return json.dumps(follows)

    @property
    def most_popular_recipe_cover_image(self):
        from recipe.models import Photos
        try:
            photos = Photos.objects \
                .filter(is_cover=True) \
                .filter(recipe__chef=self, recipe__draft=False, recipe__private=False) \
                .order_by('-recipe__nb_likes')
            return photos[0]
        except:
            return None


class Restaurant(models.Model):
    RESTAURANT_TYPE_ARTISAN = 1
    RESTAURANT_TYPE_BAR = 2
    RESTAURANT_TYPE_CHEF = 3
    RESTAURANT_TYPE_CHEF_CONSULTANT = 4
    RESTAURANT_TYPE_CHEF_PERSONAL = 5
    RESTAURANT_TYPE_FOOD_DRINKS_BRAND = 6
    RESTAURANT_TYPE_FOOD_PRODUCER = 7
    RESTAURANT_TYPE_FOOD_STYLIST = 8
    RESTAURANT_TYPE_HOTEL = 9
    RESTAURANT_TYPE_R_D = 10
    RESTAURANT_TYPE_PUB = 11
    RESTAURANT_TYPE_RESTAURANT = 12
    RESTAURANT_TYPE_SCHOOL_UNIVERSITY = 13
    RESTAURANT_TYPE_SUPPLIER = 14
    RESTAURANT_TYPE_TAKE_AWAY = 15
    RESTAURANT_TYPE_UNIVERSITY = 16

    RESTAURANT_TYPES = (
        (RESTAURANT_TYPE_ARTISAN, 'Artisan'),
        (RESTAURANT_TYPE_BAR, 'Bar, Cocktail Bar'),
        (RESTAURANT_TYPE_CHEF, 'Chef'),
        (RESTAURANT_TYPE_CHEF_CONSULTANT, 'Chef, consultant'),
        (RESTAURANT_TYPE_CHEF_PERSONAL, 'Chef, personal'),
        (RESTAURANT_TYPE_FOOD_DRINKS_BRAND, 'Food or Drink Brand'),
        (RESTAURANT_TYPE_FOOD_PRODUCER, 'Food producer'),
        (RESTAURANT_TYPE_FOOD_STYLIST, 'Food Stylist'),
        (RESTAURANT_TYPE_HOTEL, 'Hotel'),
        (RESTAURANT_TYPE_R_D, 'R & D'),
        (RESTAURANT_TYPE_PUB, 'Pub'),
        (RESTAURANT_TYPE_RESTAURANT, 'Restaurant'),
        (RESTAURANT_TYPE_SCHOOL_UNIVERSITY, 'School or University'),
        (RESTAURANT_TYPE_SUPPLIER, 'Supplier'),
        (RESTAURANT_TYPE_TAKE_AWAY, 'Take Away'),
        (RESTAURANT_TYPE_UNIVERSITY, 'University'),
    )

    chef = models.OneToOneField(Chefs, related_name="restaurant")
    type = models.IntegerField(choices=RESTAURANT_TYPES, default=RESTAURANT_TYPE_ARTISAN, blank=False, null=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    web = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)

    image = models.ImageField(upload_to=upload_to_random('restaurants/'), blank=True, null=True)
    logo = models.ImageField(upload_to=upload_to_random('restaurants/'), blank=True, null=True)

    class Meta:
        db_table = 'restaurants'

    @property
    def thumb_account_button(self):
        try:
            if self.image:
                thumb = thumbnail_url(self.image, 'account_button')
                return thumb
            else:
                return settings.STATIC_URL + 'img/restaurant_cover.png'
        except Exception, e:
            return settings.STATIC_URL + 'img/restaurant_cover.png'


class ChefFollows(models.Model):
    follower = models.ForeignKey(Chefs, blank=True, null=True, related_name="follows")
    following = models.ForeignKey(Chefs, blank=True, null=True, related_name="followed")

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chef_follows'


class AuthsManager(models.Manager):
    def valid_token(self, token):
        return self.get(token=token, expires__gte=now())


class Auths(models.Model):
    chef = models.ForeignKey(Chefs, blank=True, null=True)
    token = models.CharField(max_length=255)
    expires = models.DateTimeField()
    last_use = models.DateTimeField(blank=True, null=True)
    last_ip_used = models.CharField(max_length=255, blank=True)

    objects = AuthsManager()

    class Meta:
        db_table = 'auths'

    @classmethod
    def create(cls, user, request):
        auth = cls(
            chef=user,
            token=binascii.hexlify(os.urandom(20)).decode(),
            expires=now() + datetime.timedelta(days=30)
        )
        auth.update_use(request)
        auth.save()
        return auth

    def update_use(self, request):
        self.last_use = now()
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        self.last_ip_used = ip


# class Plan(models.Model):
#     PLAN_CHOICES = (
#         ("pro", "Pro"),
#         ("business", "Business")
#     )
#
#     INTERVAL_CHOICES = (
#         ("monthly", "Monthly"),
#         ("annually", "Annually")
#     )
#
#     type = models.CharField(choices=PLAN_CHOICES, default='pro', max_length=255)
#     interval = models.CharField(choices=INTERVAL_CHOICES, default='monthly', max_length=255)
#     amount_per_month = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#     amount_per_year = models.DecimalField(default=0, max_digits=7, decimal_places=2)
#
#     class Meta:
#         db_table = 'plan'
#
#
# class StripePayment(models.Model):
#     plan_id = models.CharField(max_length=255)
#     customer_id = models.CharField(max_length=255)
#     last4 = models.IntegerField()
#     exp_month = models.IntegerField()
#     exp_year = models.IntegerField()
#
#     class Meta:
#         db_table = 'stripe_payment'
#
#
# class Subscription(models.Model):
#     STATUSES = (
#         ('started', 'Started'),
#         ('canceled', 'Canceled'),
#         ('holding', 'Holding')
#     )
#
#     chef = models.ForeignKey(Chefs, related_name="+")
#     plan = models.ForeignKey(Plan, related_name="+")
#     started_at = models.DateTimeField(default=datetime.datetime.now())
#     period_start = models.DateTimeField(default=datetime.datetime.now())
#     period_end = models.DateTimeField(blank=True, null=True, default=None)
#     ended_at = models.DateTimeField(blank=True, null=True, default=None)
#     canceled_at = models.DateTimeField(blank=True, null=True, default=None)
#     status = models.CharField(choices=STATUSES, default='started', max_length=255)
#     is_canceled_at_period_end = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'subscription'
#
#
# class SubscriptionPayment(models.Model):
#     subscription_id = models.IntegerField()
#     subscription_method = models.CharField(default="stripe", max_length=255)
#     stripe_payment_id = models.IntegerField()
#     is_active = models.BooleanField()
#
#     class Meta:
#         db_table = 'subscription_payment'
