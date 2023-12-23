from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _

from celery_conf import celery_app


@celery_app.task()
def send_email_notification(comment_id):
    from apps.comments.models import Comment
    comment = Comment.objects.get(id=comment_id)
    user_name = comment.user.username if comment.user else _('Anonymous user')
    subject = _('Response to comment')
    message = _(f'You have received a reply to a comment: {comment.parent_comment.text}\n\n'
                f'From user: {comment.email}\nText: {comment.text}')
    send_mail(
        subject,
        message,
        None,
        [comment.parent_comment.email],
        fail_silently=False,
    )
