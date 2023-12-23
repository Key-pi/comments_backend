from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.http import HttpRequest
from django.urls import path
from django.utils import translation
from django.utils.translation import gettext_lazy as _




class CommentsAdminSite(AdminSite):
    site_header = _('Comments API')
    index_title = _("Control panel")
    site_url = ''

    def get_app_list(self, request: HttpRequest):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request)

        apps_names_order = 'user', 'comments'

        app_list = []
        for app_name in apps_names_order:
            app = app_dict.get(app_name)
            if app:
                app_list.append(app)
        return app_list

    def each_context(self, request):
        context = super().each_context(request)
        if request.user.is_authenticated:
            translation.activate(request.user.language)
        return context

class CommentsAdminSiteAdminConfig(AdminConfig):
    default_site = 'admin.CommentsAdminSite'


admin_site = CommentsAdminSite()
