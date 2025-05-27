from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from autoslug import AutoSlugField

from apps.common.models import BaseModelWithUID
from django.contrib.postgres.fields import ArrayField
from .choices import CountryChoices
from .managers import CustomUserManager

from .utils import default_countries, default_sources, default_keywords


class User(AbstractUser, BaseModelWithUID, PermissionsMixin):
    email = models.EmailField(unique=True)
    slug = AutoSlugField(populate_from="email", unique=True)
    countries = ArrayField(
        models.CharField(max_length=2, choices=CountryChoices.choices),
        default=default_countries,
        help_text="Preferred countries (ISO country codes)",
    )
    sources = ArrayField(
        models.CharField(max_length=100),
        default=default_sources,
        help_text="Preferred news sources",
    )
    keywords = ArrayField(
        models.CharField(max_length=100),
        default=default_keywords,
        help_text="Search keywords for personalizing news",
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"UID: {self.uid}, Email: {self.email}"

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_joined = timezone.now()
        self.username = self.email
        super().save(*args, **kwargs)
