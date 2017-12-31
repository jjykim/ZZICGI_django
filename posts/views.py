# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
import random
import golf.values as values
import requests
import geopy.distance

from golf.decorators import api
from django.contrib.auth import get_user_model
from .models import Filter, Store, Photo, SecretStoreKey, Survey
from golf.utils import SendJson, ImageUpload
from profiles.models import Profile
from django.db.models import Count


@api
def set_filter(request):
    query_dict = request.POST
    user_id = query_dict['user_id']
    filters = query_dict['filters']

    filter_list = filters.split(',')

    user = get_user_model().objects.get(username=user_id)
    profile = Profile.objects.get(user=user)

    profile.filters.clear()

    for filter_word in filter_list:
        add_filter = Filter.objects.get(name=filter_word)
        profile.filters.add(add_filter)

    return SendJson(result=True, message='filter success').json_response()


@api
def get_filter_list(request):
    filter_list_location = Filter.objects.filter(type=Filter.FILTER_CHOICES[0][0]).values('name', 'type')
    filter_list_tag = Filter.objects.filter(type=Filter.FILTER_CHOICES[1][0]).values('name', 'type')

    json_data = SendJson(True)
    json_data.add_object('filter_list_location', list(filter_list_location))
    json_data.add_object('filter_list_tag', list(filter_list_tag))
    return json_data.json_response()


@api
def set_gangseo_stores_open_api(request):
    ganseo_response = requests.get(values.gangseo_openapi)

    set_store_open_api(ganseo_response, 'GangseoModelRestaurantDesignate', "강서")


@api
def set_nowon_stores_open_api(request):
    nowon_response = requests.get(values.nowon_openapi)

    set_store_open_api(nowon_response, 'NwModelRestaurantDesignate', "노원")


def set_store_open_api(api_response, area, area_kr):
    api_data = api_response.json()[area]['row']

    for store_info in api_data:
        daum_api = requests.get(values.get_daum_geo_api(store_info['SITE_ADDR_RD']))

        if 'channel' in daum_api.json():
            lng = daum_api.json()['channel']['item'][0]['lng']
            lat = daum_api.json()['channel']['item'][0]['lat']

            store = Store()
            store.title = store_info['UPSO_NM']
            store.lat = lat
            store.lng = lng
            store.main = store_info['MAIN_EDF']
            store.location = store_info['SITE_ADDR_RD']
            store.save()

            if Filter.objects.filter(name=store_info['SNT_UPTAE_NM']).exist():
                tag_filter = Filter.objects.get(name=store_info['SNT_UPTAE_NM'])
            else:
                tag_filter = Filter(name=store_info['SNT_UPTAE_NM'], type=Filter.FILTER_CHOICES[1][0])
                tag_filter.save()

            store.filters.add(tag_filter)

            if Filter.objects.filter(name=area_kr).exist():
                location_filter = Filter.objects.get(name=area_kr)
            else:
                location_filter = Filter(name=area_kr)
                location_filter.save()

            store.filters.add(location_filter)
            return SendJson(True).json_response()
        else:
            return SendJson(False).json_response()


@api
def check_metadata(request):
    query_dict = request.POST
    user_id = query_dict['user_id']
    metadata = query_dict['meta_data']

    user = get_user_model().objects.get(username=user_id)
    profile = Profile.objects.get(user=user)

    if Photo.objects.get(meta_data=metadata, user=profile).exists():
        return SendJson(False, message='check fail : meta_data exist').json_response()
    else:
        return SendJson(True, message='check success').json_response()


# 5개 지표 저장
@api
def upload_post(request):
    query_dict = request.POST
    user_id = query_dict.get('user_id')
    sns_type = query_dict.get('sns_type')
    store_id = query_dict.get('store_id')
    meta_data = query_dict.get('meta_data')
    secret_key_id = query_dict.get('secret_key_id')
    like = query_dict.get('like')
    review = query_dict.get('review')
    file_photo = request.FILES['upload_file']
    checks = query_dict['checks']

    user = get_user_model().objects.get(username=user_id)
    profile = Profile.objects.get(user=user)

    post = Photo(sns_type=sns_type)

    post.user = profile
    post.meta_data = meta_data

    add_store = Store.objects.get(id=store_id)
    post.store = add_store
    post.like = like
    post.review = review

    key = store_id + str(Store.objects.filter(id=store_id).count())

    post.image = ImageUpload().upload_image(key, file_photo)

    secret_store_key = SecretStoreKey.objects.get(id=secret_key_id)

    if secret_store_key.use:
        return SendJson(message='key already use').json_response()
    else:
        secret_store_key.use = 1
        secret_store_key.save()

        post.secret_key = secret_store_key
        post.save()

        check_list = checks.split(',')

        for check_good in check_list:
            if check_good is not '':
                add_check = Survey.objects.get(name=check_good)
                post.survey_check.add(add_check)

        json_data = SendJson(True, message='photo save success')
        json_data.add_object('url', post.image)
        return json_data.json_response()


@api
def main_feed_list(request):
    query_dict = request.POST
    user_id = query_dict['user_id']

    user = get_user_model().objects.get(username=user_id)
    user_profile = Profile.objects.get(user=user)

    filter_count = user_profile.filters.count()

    if filter_count == 1:
        photos = Photo.objects.filter(store__filters__in=user_profile.filters.get()).order_by('-created_at')
    elif filter_count == 2:
        user_filter = user_profile.filters.all()
        photos = Photo.objects.filter(store__filters=user_filter[0], store__filters=user_filter[1]).order_by(
            '-created_at')
    else:
        photos = Photo.objects.order_by('-created_at')

    photo_list = []
    for one_photo in photos:
        photo_list.append(one_photo.as_json())

    json_data = SendJson(True)
    json_data.add_object('photos', photo_list)
    return json_data.json_response()


@api
def make_key(request):
    query_dict = request.POST
    user_id = query_dict['user_id']
    store_id = query_dict['store_id']

    chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"',
                                                                                                         '').replace(
        '\\', '')

    secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(50)]) + user_id

    user = get_user_model().objects.get(username=user_id)
    user_profile = Profile.objects.get(user=user)
    choose_store = Store.objects.get(id=store_id)

    new_key = SecretStoreKey()
    new_key.user = user_profile
    new_key.store = choose_store
    new_key.value = secret_key
    new_key.use = 0
    new_key.save()

    return SendJson(True, message='make_key success').json_response()


@api
def key_list(request):
    query_dict = request.POST
    user_id = query_dict['user_id']

    user = get_user_model().objects.get(username=user_id)
    user_profile = Profile.objects.get(user=user)
    key_data = SecretStoreKey.objects.filter(user=user_profile, use=0).order_by('-created_at') \
        .values('id', 'created_at', 'store__title', 'store__id')

    if len(key_data) is 0:
        return SendJson(False, 'no valuable key').json_response()
    else:
        json_data = SendJson(True, 'key_exist')
        json_data.add_object(key_list, list(key_data))
        return json_data.json_response()


@api
def delete_photo(request):
    Photo.objects.all().delete()

    return SendJson(True).json_response()


@api
def get_my_profile(request):
    """
    :param request:
    :return: user 정보, 공유 사진 리스트, 갯수 json
    """
    query_dict = request.POST
    user_id = query_dict['user_id']

    user = get_user_model().objects.get(username=user_id)
    my_profile = Profile.objects.get(user=user)

    my_photos = Photo.objects.filter(user=my_profile).order_by('-created_at') \
        .values('id', 'review', 'created_at', 'image', 'store__title', 'store__id')
    share_count = my_photos.count()

    json_data = SendJson(True)
    json_data.add_object('user_id', user_id)
    json_data.add_object('nickname', my_profile.nickname)
    json_data.add_object('profile_url', my_profile.profile_image)
    json_data.add_object('share_count', share_count)
    json_data.add_object('photos', list(my_photos))

    return json_data.json_response()


@api
def store_detail(request):
    query_dict = request.POST
    store_id = query_dict['store_id']

    store = Store.objects.get(id=store_id)
    photos = Photo.objects.filter(store=store).order_by('-created_at')

    share_count = photos.count()

    photo_list = []
    for photo in photos:
        photo_list.append(photo.as_json())

    donation_count = SecretStoreKey.objects.filter(store=store, donation=SecretStoreKey.IS_DONATION[1][0]).count()

    json_data = SendJson(True)
    json_data.add_object('store_id', store.id)
    json_data.add_object('store_name', store.title)
    json_data.add_object('store_location', store.location)
    json_data.add_object('share_count', share_count)
    json_data.add_object('photos', photo_list)
    json_data.add_object('donation_count', donation_count)

    if Photo.objects.filter(store=store).exist():
        good_count = Photo.objects.filter(like=Photo.LIKE_CHOICES[0][0], store=store).count()
        json_data.add_object('good_count', good_count)

        categories = Photo.objects.filter(store=store).values('survey_check__name').annotate(
            count=Count('survey_check__name'))
        json_data.add_object('categories', categories)

    return json_data.json_response()


@api
def find_store_name(request):
    query_dict = request.POST
    store_keyword = query_dict['store_keyword']

    stores = Store.objects.filter(title__contains=store_keyword).values('id', 'title', 'location')

    if stores:
        json_data = SendJson(True, 'store list exist')
        json_data.add_object('store_list', list(stores))
        return json_data.json_response()
    else:
        return SendJson(message='no valuable store').json_response()


@api
def get_store_location(request):
    query_dict = request.POST
    store_id = query_dict['store_id']

    store = Store.objects.get(id=store_id)
    share_count = Photo.objects.filter(store=store).count()
    donation_count = SecretStoreKey.objects.filter(store=store, donation=SecretStoreKey.IS_DONATION[1][0]).count()

    json_data = SendJson(True)
    json_data.add_object('lat', store.lat)
    json_data.add_object('lng', store.lng)
    json_data.add_object('name', store.title)
    json_data.add_object('id', store.id)
    json_data.add_object('location', store.location)

    if share_count > 0 and (donation_count / share_count * 100) > 90:
        json_data.add_object('good_donator', True)
    else:
        json_data.add_object('good_donator', False)

    return json_data.json_response()


@api
def get_near_store(request):
    query_dict = request.POST
    position_lng = query_dict['position_lng']
    position_lat = query_dict['position_lat']

    square_standard = get_square_standard(position_lat, position_lng)
    stores = Store.objects.filter(lat__gt=square_standard[2], lat__lt=square_standard[3],
                                  lng__gt=square_standard[1], lng__lt=square_standard[0])

    near_stores = []
    for one_store in stores:
        share_count = Photo.objects.filter(store=one_store).count()
        donation_count = SecretStoreKey.objects.filter(store=one_store, donation=SecretStoreKey.IS_DONATION[1][0]).count()

        send_info = {'lng': one_store.lng, 'lat': one_store.lat, 'id': one_store.id, 'name': one_store.title,
                     'location': one_store.location}

        if share_count is not 0 and (donation_count / share_count * 100) > 90:
            send_info['good_donator'] = True
        else:
            send_info['good_donator'] = False
        near_stores.append(send_info)

    json_data = SendJson(True)
    json_data.add_object('near_stores', near_stores)
    return json_data.json_response()


def get_square_standard(latitude, longitude, kilometers=0.5):
    # 사용자 현재 위치 기준으로 0.5km point 구하기
    start = geopy.Point(latitude, longitude)

    d = geopy.distance.VincentyDistance(kilometers=kilometers)

    north = d.destination(point=start, bearing=0).latitude
    east = d.destination(point=start, bearing=90).longitude
    south = d.destination(point=start, bearing=180).latitude
    west = d.destination(point=start, bearing=270).longitude

    return east, west, south, north


@api
def get_donation_list(request):
    query_dict = request.POST
    user_id = query_dict['user_id']

    user = get_user_model().objects.get(username=user_id)
    my_profile = Profile.objects.get(user=user)

    keys = SecretStoreKey.objects.filter(user=my_profile).filter(donation=SecretStoreKey.IS_DONATION[1][0])\
        .annotate(count_donation=Count('store'))

    donation_list = []
    for key in keys:
        send_info = {'donation_date': key.donation_date, 'store_name': key.store.name, 'count': key.count_donation}
        donation_list.append(send_info)

    json_data = SendJson(True)
    json_data.add_object('donation_list', donation_list)
    return json_data.json_response()
