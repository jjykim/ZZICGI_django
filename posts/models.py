# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os


class Filter(models.Model):
    FILTER_CHOICES = (
        (0, 'location',),
        (1, 'tag',),
    )
    
    type = models.IntegerField(default=0, choices=FILTER_CHOICES)
    name = models.CharField('name', max_length=100)

    def __unicode__(self):
        return self.name


class Store(models.Model):

    title = models.CharField('title', max_length=500)
    lat = models.CharField('lat', max_length=500, default='none')
    lng = models.CharField('lng', max_length=500, default='none')
    main = models.CharField('main', max_length=500, default='none')
    location = models.CharField('location', max_length=1000, default='none')
    filters = models.ManyToManyField(Filter)

    def __unicode__(self):
        return self.title


class SecretStoreKey(models.Model):
    IS_USED = (
        (0, 'not',),
        (1, 'use',),
    )

    IS_DONATION = (
        (0, 'no',),
        (1, 'yes',),
    )

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    use = models.IntegerField(default=0, choices=IS_USED)
    value = models.CharField('special_key', max_length=1000, default='value_none')
    store = models.ForeignKey(Store)
    user = models.ForeignKey('profiles.Profile', default='-99')
    donation = models.IntegerField(default=0, choices=IS_DONATION)
    donation_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.id)

    
class Photo(models.Model):
    SNS_CHOICES = (
        (0, 'facebook',),
        (1, 'kakaotalk',),
    )

    LIKE_CHOICES = (
        (0, 'good',),
        (1, 'bad',),
    )

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    image = models.URLField(default='/url') 
    sns_type = models.IntegerField(default=0, choices=SNS_CHOICES)
    user = models.ForeignKey('profiles.Profile', default='-99')
    store = models.ForeignKey(Store)
    meta_data = models.CharField('meta_data', max_length=1000, default='none') #date_time
    secret_key = models.ForeignKey(SecretStoreKey, null=True, default=-99)
    review = models.TextField('review', default='none')
    like = models.IntegerField(default=0, choices=LIKE_CHOICES)
    survey_check = models.ManyToManyField('Survey')

    def __unicode__(self):
        return unicode(self.id)

    def as_json(self):
        return dict(
            photo_id=self.id, 
            photo_user_id=self.user.user.username,
            photo_user_nickname=self.user.nickname,
            photo_user_image=self.user.profile_image,
            photo_review=self.review, 
            photo_date=self.created_at.isoformat(),
            photo_url=self.image,
            photo_store_name=self.store.title,
            photo_store_id=self.store.id,
            )


class Survey(models.Model):
    FILTER_CHOICES = (
        (0, 'food',),
        (1, 'hotel',),
    )
    
    type = models.IntegerField(default=0, choices=FILTER_CHOICES)
    name = models.CharField('name', max_length=100)

    def __unicode__(self):
        return self.name
      


