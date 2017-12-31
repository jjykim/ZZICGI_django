from arclib.django.decorators import api as arc_api, exception_json


def api(func):
    @arc_api
    @exception_json
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance
