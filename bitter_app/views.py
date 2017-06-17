# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from bitter_app.forms import UserCreateForm
from bitter_app.forms import LogInForm
from bitter_app.forms import EditProfileForm
from bitter_app.forms import BittForm
from bitter_app.models import Bitts

def index(request, user_create_form=None, log_in_form=None):
    """
    If user is logged in displays users homepage, if user is not logged in
    displays home page with sign up and registration form.
    """
    if request.user.is_authenticated():
        own_bitts = Bitts.objects.filter(user_id=request.user.id).order_by('-date_created')
        friends_bitts = Bitts.objects.filter(user__profile__in=request.user.profile.follows.all()).order_by('-date_created')
        bitts = own_bitts | friends_bitts
        return render(request, 'bitter_app/home.html', {
            'bitts' : bitts,
            'bitt_form' : BittForm(),
            'return_to' : reverse('bitter:index')
        })
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
    """
    Deal with the signup form. If the user is successfully signed up, display
    the home page. If the user form is not valid, load the index page with form
    displaying errors.
    """
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

        return index(request, user_create_form=user_create_form)
    return redirect(reverse('bitter:index'))

def log_out(request):
    """
    Log out the user from the site.
    """
    logout(request)
    return redirect(reverse('bitter:index'))

def log_in(request):
    """
    Deal with the log in form. If the user is successfully logged in, display
    the home page. If the user form is not valid, load the index page with form
    displaying errors.
    """
    if request.method == 'POST':
        log_in_form = LogInForm(data=request.POST)

        if log_in_form.is_valid():
            login(request, log_in_form.get_user())
            return redirect(reverse('bitter:index'))

        return index(request, log_in_form=log_in_form)
    return redirect(reverse('bitter:index'))

# right click on profile page, view source, leads to
# view-source:http://127.0.0.1:8000/accounts/login/?next=/profile/
# i.e. 404, why?
@login_required
@transaction.atomic
def profile(request, user_form=None, profile_form=None):
    """
    Display a page where user can edit their profile.
    """
    if request.method == 'POST':
        user_form = UserCreateForm(data=request.POST, instance=request.user)
        # Make a function to check a file size, settings.py: CONTENT_TYPES, MAX_UPLOAD_SIZE
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.clean_password())
            user.save()
            profile_form.save()

            # should user be re-authenticated before this?
            login(request, user)
            return redirect(reverse('bitter:index'))
        else:
            # This should throw error or warning messages
            return redirect(reverse('bitter:profile'))
    else:
        user_form = UserCreateForm(instance = request.user)
        profile_form = EditProfileForm(instance = request.user.profile)
        return render(request, 'bitter_app/profile.html', {
            'user_form' : user_form,
            'profile_form' : profile_form,
        })

@login_required
def bitts(request):
    return render(request, 'bitter_app/bitts.html', {
        'bitts' : Bitts.objects.filter(user_id=request.user.id),
        'user' : request.user,
        'bitt_form' : BittForm(),
        'return_to' : reverse('bitter:bitts'),
    })

@login_required
def bitt_submit(request):
    """
    Submit a 'bitt'. After a status is posted successfully redired a user to the
    page from which they posted a 'bitt'. If there is no information about the
    page the user is currently on, redirect them to home page.
    """
    if request.method == 'POST':
        bitt_form = BittForm(data=request.POST)
        return_to = request.POST.get('return_to', reverse('bitter:index'))

        if bitt_form.is_valid():
            bitt = bitt_form.save(commit=False)
            bitt.user = request.user
            bitt.save()
            return redirect(return_to)

        raise ValidationError("Invalid data for a bitt form.")
    return redirect(reverse('bitter:index'))

@login_required
def users(request, username='', native_user=False, bitt_form=None, return_to='', follow={}):
    """
    If a user is a session user (native_user) do not display follow button, but
    display a bitt form. The bug here is, the session user has two same pages
    i.e. /bitts/ is same as /users/[username]/. In any cass, restrict user view
    to show only users different from a session user. Is this function doing
    too much? Probably :(
    """
    # Display an individual user
    if username:
        # If user is clicking on himself
        if username == request.user.username:
            native_user = True
            bitt_form = BittForm()
            return_to = reverse('bitter:user', args=[username])
        else:
            # Do I follow already this user, or not?
            # If I follow, present me the unfollow option et vice versa
            if request.user.profile.follows.filter(user__username=username):
                follow = {
                    'follow_link' : reverse('bitter:unfollow'),
                    'follow_option' : 'Unfollow',
                }
            else:
                follow = {
                    'follow_link' : reverse('bitter:follow'),
                    'follow_option' : 'Follow',
                }

        # get object or 404 user - should be before conditional statement
        user = User.objects.get(username=username)
        bitts = Bitts.objects.filter(user_id=user.id)

        return render(request, 'bitter_app/user_username.html', {
            'native_user' : native_user,
            'bitt_form' : bitt_form,
            'return_to' : return_to,
            'bitts' : bitts,
            'user' : user,
            'follow' : follow,
        })
    else:
        # Display a list of users
        return render(request, 'bitter_app/users.html', {
            'users' : User.objects.all().annotate(bitt_count=Count('bitts')),
        })

@login_required
def follow(request):
    """
    Follow another user.
    """
    if request.method == 'POST':
        user_follow_id = request.POST['user_follow_id']
        user_to_follow = User.objects.get(id=user_follow_id)
        request.user.profile.follows.add(user_to_follow.profile)
        return redirect(reverse('bitter:user', args=[user_to_follow.username]))
    return redirect(reverse('bitter:users'))

@login_required
def unfollow(request):
    """
    Unfollow a user.
    """
    if request.method == 'POST':
        user_follow_id = request.POST['user_follow_id']
        user_to_unfollow = User.objects.get(id=user_follow_id)
        request.user.profile.follows.remove(user_to_unfollow.profile)
        return redirect(reverse('bitter:user', args=[user_to_unfollow.username]))
    return redirect(reverse('bitter:users'))
