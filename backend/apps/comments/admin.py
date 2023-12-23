from django.contrib import admin
from apps.comments.models import Comment

@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'home_page', 'text', 'created_at', 'parent_comment')
    fields = ('user', 'email', 'home_page', 'text', 'parent_comment')
    list_display_links = ('parent_comment',)
