# Django imports
from django.urls import path

# App imports
from .views import user_registration, user_login, user_update

urlpatterns = [
    path("register/", user_registration, name="user_registration"),
    path("login/", user_login, name="user_login"),
    path("update/<pk>/", user_update, name="user_update"),
]
