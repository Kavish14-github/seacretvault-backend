from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, EnvironmentViewSet, SecretViewSet
from rest_framework.authtoken import views


router = DefaultRouter()
router.register(r'secrets', SecretViewSet, basename='secret')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'environments', EnvironmentViewSet, basename='environment')


urlpatterns = [
    path('', include(router.urls)),
    path("auth/token/", views.obtain_auth_token),
]
