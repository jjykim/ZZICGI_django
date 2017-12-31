# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Filter, Store, Photo, SecretStoreKey, Survey


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'secret_key', 'store')
    list_display_links = ('id', 'user')


class KeyAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'use', 'user', 'domination_date', 'domination')
    list_display_links = ('id', 'store')

admin.site.register(Filter)
admin.site.register(Store, StoreAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(SecretStoreKey, KeyAdmin)
admin.site.register(Survey)