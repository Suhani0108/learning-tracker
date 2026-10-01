from django.urls import include, path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    # Django's built-in login, logout and password views. They give us URL
    # names like "login" and "logout", and look for templates in
    # templates/registration/ (e.g. registration/login.html).
    path("", include("django.contrib.auth.urls")),
]
