from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id', 'user', 'email', 'home_page', 'text', 'created_at', 'parent_comment'
        extra_kwargs = {
            'parent_comment': {"read_only": True},
        }


class CreateCommentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = Comment
        fields = 'user', 'email', 'home_page', 'text', 'parent_comment'
        extra_kwargs = {
            'user': {"read_only": True},
        }

    def validate(self, data):
        user = self.context['request'].user
        email = data.get('email')
        if user.is_authenticated and not email:
            data['email'] = user.email
        elif not email:
            raise serializers.ValidationError({'email': _('This field is required for anonymous users.')})
        return data


class CommentDetailSerializer(CommentSerializer):
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj)
        serializer = CommentDetailSerializer(replies, many=True)
        return serializer.data

    class Meta(CommentSerializer.Meta):
        fields = (*CommentSerializer.Meta.fields, 'replies')


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'email', 'home_page', 'text',
        extra_kwargs = {
            'email': {'read_only': True},
            'parent_comment': {'read_only': True},
        }


class PartialUpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'email', 'home_page', 'text',
        extra_kwargs = {
            'email': {'read_only': True},
            'parent_comment': {'read_only': True},
        }
