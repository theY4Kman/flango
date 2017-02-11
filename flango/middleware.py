from flango.request import _push_request, _pop_request


def global_request_middleware(get_response):
    """Save request object to thread local"""

    def middleware(request):
        _push_request(request)
        response = get_response(request)
        _pop_request()
        return response

    return middleware
