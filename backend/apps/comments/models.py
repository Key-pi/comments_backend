from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, AFTER_CREATE
from celery_conf import QueuesConfig

from apps.comments.tasks import send_email_notification

User = get_user_model()


class Comment(LifecycleModelMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(('Email'), null=False, blank=True)
    home_page = models.URLField(_('Home Page'), blank=True, null=True)  # Воообще не понял зачем и почему это поле
    text = models.TextField(_('Comment text'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.created_at}"

    @hook(AFTER_CREATE)
    def send_email_notification(self):
        if self.parent_comment is not None:
            send_email_notification.apply_async(args=[self.id], countdown=10, queue=QueuesConfig.HIGH_PRIORITY_QUEUE)
