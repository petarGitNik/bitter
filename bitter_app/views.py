# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from bitter_app.forms import UserCreateForm
from bitter_app.forms import LogInForm

def index(request, user_create_form=None, log_in_form=None):
    """
    If user is logged in displays users homepage, if user is not logged in
    displays home page with sign up and registration form.
    """
    if request.user.is_authenticated():
        pass
    else:
        user_create_form = user_create_form or UserCreateForm()
        log_in_form = log_in_form or LogInForm()
        return render(request, 'bitter_app/index.html', {
            'log_in_form' : log_in_form,
            'user_create_form' : user_create_form,
        })

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
