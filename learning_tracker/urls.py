"""
Project-level URL configuration.

Django checks these patterns in order for every request. The admin gets its
own URLs, /accounts/ goes to the accounts app (login, logout, sign up), and
everything else is handed to the topics app's urls.py.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("topics.urls")),
]
