from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocialAPIViewSet

router = DefaultRouter()
router.register(r'social-api', SocialAPIViewSet, basename='social-api')

urlpatterns = [
    path('', include(router.urls)),
]
