# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Bitts(models.Model):
    user = models.ForeignKey(User)
    bitt_text = models.CharField(max_length=140)
    date_created = models.DateTimeField(auto_now=True, blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=250, blank=True)
    avatar = models.FileField(
        upload_to='avatars/%Y/%m/%d',
        default='avatars/avatar_default.jpeg'
    )

# Two following definitions make sure that pforile is created and updated
# simultaneously with the user model
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
