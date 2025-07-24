from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RegisterView

router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')

urlpatterns = [
    path('', include(router.urls)),
]
