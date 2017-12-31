# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^set/filter', views.set_filter),
    url(r'^get/filter/list', views.get_filter_list),
    url(r"^set/gangseo/stores/api", views.set_gangseo_stores_open_api),
    url(r"^set/nowon/stores/api", views.set_nowon_stores_open_api),
    url(r'^upload/post', views.upload_post),
    url(r'^main/feed/list', views.main_feed_list),
    url(r'^make/key', views.make_key),
    url(r'^get/key/list', views.key_list),
    url(r'^delete/photo', views.delete_photo),
    url(r'^get/my_profile', views.get_my_profile),
    url(r'^check/metadata', views.check_metadata),
    url(r'^get/store/detail', views.store_detail),
    url(r'^find/store/name', views.find_store_name),
    url(r'^get/store/location', views.get_store_location),
    url(r'^get/near/store', views.get_near_store),
    url(r'^get/donation/list', views.get_donation_list),
]