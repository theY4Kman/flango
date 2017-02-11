from django.urls import reverse

from flango import request


def url_for(viewname, *args, **kwargs):
    url = reverse(viewname, args=args, kwargs=kwargs)
    if kwargs.pop('_external', False):
        url = request.build_absolute_uri(url)
    return url
