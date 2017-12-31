# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Profile
from django.contrib.auth import get_user_model, authenticate
from golf.utils import SendJson
from golf.decorators import api


@api
def create_user(request):
    query_dict = request.POST
    user_id = query_dict['user_id']
    nickname = query_dict['nickname']
    device_id = query_dict['device_id']
    profile_image = query_dict['profile_image']

    auth_user = authenticate(username=user_id, password=user_id + nickname)

    json_data = SendJson(True)

    if auth_user is not None:
        if auth_user.is_active:
            json_data.add_object('message', 'exist active user')
        else:
            json_data.add_object('message', 'exist not active user')

    else:
        new_user = get_user_model().objects.create_user(
            username=user_id,
            password=user_id + nickname,
        )

        new_profile = Profile(
            user=new_user,
            nickname=nickname,
            device_id=device_id,
            profile_image=profile_image,
        )

        new_profile.save()

        json_data.add_object('message', 'login success')

    json_data.add_object('user_id', user_id)
    json_data.add_object('nickname', nickname)
    json_data.add_object('device_id', device_id)
    json_data.add_object('profile_image', profile_image)

    return json_data.json_response()
