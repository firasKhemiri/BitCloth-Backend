from typing import Sequence

from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from bit_cloth import settings


class User(AbstractUser):

    username = models.CharField(
        'username',
        max_length=100,
        unique=True,
        help_text=('Required. 30 characters or fewer. Letters, digits and '
                   '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(
                r'^[\w.@+-]+$',
                ('Enter a valid username. '
                 'This value may contain only letters, numbers '
                 'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': ("A user with that username already exists."),
        })
    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))

    facebook_id = models.CharField(max_length=200, unique=True,null=True,blank=True)

    email = models.EmailField(
        ('email address'),
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
        })


    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=6, blank=True)

    picture = models.CharField(max_length=255, blank=True)
    cover_picture = models.CharField(max_length=255, blank=True)

    phone = models.CharField(max_length=8, blank=True)

    is_social = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=True)

    # AbstractUser._meta.get_field('email')._unique = True

    date_joined = models.DateTimeField(('date joined'), default=timezone.now)

    following = models.ManyToManyField('self', related_name="who_follows", symmetrical=False, blank=True)
    followers = models.ManyToManyField('self', related_name="who_is_followed", symmetrical=False, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def to_dict(self):
        return {"firstName": self.first_name, "lastName": self.last_name,"followers":self.followers}

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def create_auth_token(sender, instance=None, created=False, **kwargs):
    #     Token.objects.get_or_create(user=instance)
    #     RefreshToken.generate_token()
    #     To

# class Creator(User):
#     class CreatorTypes(DjangoChoices):
#         AMATEUR = ChoiceItem(0)
#         PRO = ChoiceItem(1)
#
#     selling_address = models.CharField(max_length=50, blank=True, null=True)
#     type = models.CharField(choices=CreatorTypes.choices, max_length=8, blank=False, null=False, default=False)



