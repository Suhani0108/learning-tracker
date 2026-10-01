from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def signup(request):
    """Create an account, log the new user in, and send them to their topics."""
    # Logged-in users don't need to sign up again
    if request.user.is_authenticated:
        return redirect("topics:list")

    if request.method == "POST":
        # UserCreationForm is built into Django: username + password twice,
        # with password strength checks from settings.AUTH_PASSWORD_VALIDATORS
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in straight away
            messages.success(request, f"Welcome, {user.username}! Add your first topic.")
            return redirect("topics:list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
