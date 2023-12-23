from typing import Type

from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.serializers import Serializer


class SerializerMapper:
    serializers = {
        'default': Serializer,
    }

    def get_serializer_class(self) -> Type[Serializer]:
        return self.serializers.get(self.action, self.serializers['default'])

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class PermissionsMapper:
    permissions_per_actions = {
        'default': [permissions.AllowAny()],
    }

    def get_permissions(self) -> list:
        return self.permissions_per_actions.get(self.action, self.permissions_per_actions['default'])


class QuerysetMapper:
    default_queryset = None
    querysets = {
        'default': default_queryset
    }

    def get_queryset(self):
        queryset = self.querysets.get(self.action, self.querysets['default'])
        if isinstance(queryset, QuerySet):
            # Ensure queryset is re-evaluated on each request.
            queryset = queryset.all()
        return queryset
