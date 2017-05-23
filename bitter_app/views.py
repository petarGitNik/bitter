# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from bitter_app.forms import UserCreateForm
from bitter_app.forms import LogInForm
from bitter_app.forms import EditProfileForm

def index(request, user_create_form=None, log_in_form=None):
    """
    If user is logged in displays users homepage, if user is not logged in
    displays home page with sign up and registration form.
    """
    if request.user.is_authenticated():
        return render(request, 'bitter_app/home.html')
    else:
        user_create_form = user_create_form or UserCreateForm()
        log_in_form = log_in_form or LogInForm()
        return render(request, 'bitter_app/index.html', {
            'log_in_form' : log_in_form,
            'user_create_form' : user_create_form,
        })

# The navbar logic does not work!
def about(request, show_full_nav=False):
    """
    If user is logged in show the full navigation bar.
    """
    if request.user.is_authenticated():
        show_full_nav = True
    return render(request, 'bitter_app/about.html', {
        'show_full_nav' : show_full_nav
    })

def signup(request):
    if request.method == 'POST':
        user_create_form = UserCreateForm(data=request.POST)
        if user_create_form.is_valid():
            username = user_create_form.cleaned_data['username']
            password = user_create_form.clean_password()

            user_auth = user_create_form.save()
            user_auth.set_password(password)
            user_auth.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                raise PermissionDenied("No backend authenticated the credentials")

            return redirect(reverse('bitter:index'))
        else:
            # Add error messages when sign up fails
            return index(request, user_create_form=user_create_form)
    else:
        return redirect(reverse('bitter:index'))

def log_out(request):
    logout(request)
    return redirect(reverse('bitter:index'))

def log_in(request):
    if request.method == 'POST':
        log_in_form = LogInForm(data=request.POST)
        if log_in_form.is_valid():
            login(request, log_in_form.get_user())
            return redirect(reverse('bitter:index'))
        else:
            # Add error messages when log in fails
            return index(request, log_in_form=log_in_form)
    else:
        return redirect(reverse('bitter:index'))

# right click on profile page, view source, leads to
# view-source:http://127.0.0.1:8000/accounts/login/?next=/profile/
# i.e. 404
@login_required
@transaction.atomic
def profile(request, user_form=None, profile_form=None):
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST, instance=request.user)
        profile_form = EditProfileForm(data=request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.clean_password())
            user.save()
            profile_form.save()
            # Should this redirect back to home/index/root or profile?
            # user not authenticated after profile edit? yes, it is not
            # and it is not logged in
            # user should be re-authenticated and logged in again
            # maybe a separate function to deal with it, or extra case in log_in?
            login(request, user)
            return redirect(reverse('bitter:index'))
        else:
            # This should throw error or warning message e.g.
            # passwords should match, and so on
            return redirect(reverse('bitter:profile'))
    else:
        user_form = UserCreateForm(instance = request.user)
        profile_form = EditProfileForm(instance = request.user.profile)
        return render(request, 'bitter_app/profile.html', {
            'user_form' : user_form,
            'profile_form' : profile_form,
        })
