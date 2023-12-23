from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE  # noqa
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE  # noqa


def avatars_photo_file_path(instance, filename):
    return f'avatars/photo_type/{instance.username}&{filename}'


class User(AbstractUser):
    email = models.EmailField(_('Email'), blank=True, null=True, unique=True)
    language = models.CharField(_('Language'), max_length=10, choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)
    avatar = models.ImageField(_('Avatar image'), upload_to=avatars_photo_file_path, blank=True, null=True,
                               help_text=_('Avatar'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def remove_user_info(self):
        self.email = ''
        self.first_name = ''
        self.save()
