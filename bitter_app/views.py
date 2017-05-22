# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from bitter_app.forms import UserCreateForm
from bitter_app.forms import LogInForm

def index(request, user_create_form=None, log_in_form=None):
    """
    If user is logged in displays users homepage, if user is not logged in
    displays home page with sign up and registration form.
    """
    user_create_form = user_create_form or UserCreateForm()
    log_in_form = log_in_form or LogInForm()
    return render(request, 'bitter_app/index.html', {
        'log_in_form' : log_in_form,
        'user_create_form' : user_create_form,
    })

def about(request, show_full_nav=False):
    if request.user.is_authenticated():
        show_full_nav = True
    return render(request, 'bitter_app/about.html', {
        'show_full_nav' : show_full_nav
    })
