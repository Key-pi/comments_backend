from django.http import HttpRequest
from django.utils import translation


class LocaleMixin:
    def perform_authentication(self, request: HttpRequest):
        result = super(LocaleMixin, self).perform_authentication(request)
        if request.user.is_authenticated and not request.user.is_staff:
            translation.activate(request.user.language)
        return result
