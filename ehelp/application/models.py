from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
import datetime

"""
CITIES AND COUNTRIES
1. cities    = > name country longitude latitude
2. countries = > name iso1 iso2 phone currency
"""


class Country(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    currency = models.CharField(max_length=50, null=True, blank=True)
    lang = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Request_Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Request Categories'

    def __str__(self):
        return self.name


"""
USER MODEL AND USER MANAGER
1.before any migrations comment two lines
   'admin/' link from main url
   'django.contrib.admin', from Installed apps in main settings
"""


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """ Creates and saves a User with the given email and password. """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """ Creates and saves a staff user with the given email and password. """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")

    full_name = models.CharField(max_length=255)
    profile = models.ImageField(
        upload_to='images/profiles/',
        height_field='image_height', width_field='image_width',
        default='images/profiles/user-blank-image.png',
        help_text="Profile Picture", verbose_name="Profile Picture"
    )
    code = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone = models.CharField(max_length=255, unique=True, blank=True, null=True)
    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True)

    points = models.IntegerField(default=0, blank=True, null=True)
    requests = models.IntegerField(default=0, blank=True, null=True)
    responses = models.IntegerField(default=0, blank=True, null=True)
    hearts = models.IntegerField(default=0, blank=True, null=True)
    subscribers = models.IntegerField(default=0, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_admin = models.BooleanField(default=False)  # a superuser

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return "{0}".format(self.profile)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


"""
REQUEST, RESPONSE AND QUEUE MODELS AND MANAGERS
"""


class Request_Status(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Request Status'

    def __str__(self):
        return self.name


class Request(models.Model):
    desc = models.TextField(null=False, blank=False)
    request_category = models.ForeignKey(Request_Category, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255, null=False, blank=False)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, null=True, blank=True)
    supply = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)

    accepted = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Requests'

    def __str__(self):
        return str(self.id)


class Request_Images(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/requests/')

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.image.name + ' of ' + self.request


class Response(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    desc = models.TextField(null=True, blank=True)
    request_points = models.IntegerField(default=0, null=True, blank=True)
    shipment_points = models.IntegerField(default=0, null=True, blank=True)
    other_points = models.IntegerField(default=0, null=True, blank=True)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'Responses'

    def __str__(self):
        return str(self.id)


class Queue(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = 'Queues'

    def __str__(self):
        return str(self.id)

