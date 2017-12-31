# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField('nickname', max_length=100, blank=True)
    device_id = models.CharField('deviceID', max_length=300, blank=True)
    profile_image = models.URLField(default='/url')
    filters = models.ManyToManyField('posts.Filter')

    def __unicode__(self):
        return self.nickname