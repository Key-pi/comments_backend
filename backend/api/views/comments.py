from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.mixins.locale import LocaleMixin
from api.mixins.mapping import SerializerMapper, QuerysetMapper, PermissionsMapper
from api.pagination.pagination import StandardResultsSetPagination
from api.serializers.comments import CommentSerializer, CreateCommentSerializer, CommentDetailSerializer, \
    UpdateCommentSerializer, PartialUpdateCommentSerializer
from apps.comments.models import Comment
from apps.comments.permissions import IsCommentOwnerOrReadOnly
from settings.swagger import SwaggerTags


@extend_schema_view(
    replies=extend_schema(
        description='replies comment', tags=[SwaggerTags.COMMENT],
        summary='Info comment'
    ),
    create=extend_schema(
        description='Create comment endpoint', tags=[SwaggerTags.COMMENT],
        summary='Create comment endpoint'
    ),
    list=extend_schema(
        description='List main comments', tags=[SwaggerTags.COMMENT],
        summary='List main comments'
    ),
    update=extend_schema(
        description='Update comment endpoint', tags=[SwaggerTags.COMMENT],
        summary='Update comment endpoint'
    ),
    partial_update=extend_schema(
        description='partial update comment endpoint', tags=[SwaggerTags.COMMENT],
        summary='partial update comment endpoint'
    ),
    destroy=extend_schema(
        description='Delete comment', tags=[SwaggerTags.COMMENT],
        summary='delete comment endpoint'
    ),
)
class CommentViewSet(LocaleMixin, SerializerMapper, PermissionsMapper, QuerysetMapper, viewsets.GenericViewSet):
    pagination_class = StandardResultsSetPagination

    serializers = {
        'create': CreateCommentSerializer,
        'list': CommentSerializer,
        'replies': CommentDetailSerializer,
        'update': UpdateCommentSerializer,
        'partial_update': PartialUpdateCommentSerializer,
        'default': Comment,
    }

    querysets = {
        'default': Comment.objects
    }

    permissions_per_actions = {
        'create': [AllowAny()],
        'update': [IsCommentOwnerOrReadOnly()],
        'partial_update': [IsCommentOwnerOrReadOnly()],
        'destroy': [IsCommentOwnerOrReadOnly()],
        'list': [AllowAny()],
        'default': [AllowAny()],
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.clear()
        return Response(serializer.data, status=201)

    @method_decorator(cache_page(300, key_prefix="comment-list"))
    def list(self, request):
        qs = self.get_queryset().filter(parent_comment=None)
        page = self.paginate_queryset(qs)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.clear()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()
        cache.clear()
        return Response(status=204)

    @action(detail=True, methods=['GET'])
    @method_decorator(cache_page(300, key_prefix="comment-replies"))
    def replies(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
