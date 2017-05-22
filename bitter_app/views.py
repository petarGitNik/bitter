# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from bitter_app.forms import UserCreateForm
from bitter_app.forms import LogInForm

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
    user_create_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
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
            #authenticate(username=log_in_form.get_user().username, password=log_in_form.get_user().password)
            login(request, log_in_form.get_user())
            return redirect(reverse('bitter:index'))
        else:
            return index(request, log_in_form=log_in_form)
    else:
        return redirect(reverse('bitter:index'))
