from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    auth,
    comments
)

router = routers.SimpleRouter()

router.register('auth', auth.AuthViewSet, basename='auth')
router.register('comment', comments.CommentViewSet, basename='comment')

urlpatterns = router.urls
