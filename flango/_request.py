from werkzeug.local import LocalProxy, LocalStack


request_stack = LocalStack()


def _get_request():
    request = request_stack.top
    if not request:
        raise AssertionError(
            "No request registered. If you are trying to use Flango's request "
            "from outside a Flango view, add 'flango.global_request_middleware' "
            "to the top of settings.MIDDLEWARE.")

    return request


request = LocalProxy(_get_request, 'request')
