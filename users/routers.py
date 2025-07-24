# routers.py: URL routing for user registration endpoints
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RegisterView

# Create a router and register the RegisterView
router = DefaultRouter()
router.register(r'register', RegisterView, basename='register')

# Include the router URLs in the urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
