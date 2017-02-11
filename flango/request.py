from werkzeug.local import Local, LocalProxy, LocalManager

_local = Local()
_local_manager = LocalManager([_local])


def _push_request(request):
    """Add request to the request stack"""
    if not hasattr(_local, 'request_stack'):
        _local.request_stack = []
    _local.request_stack.append(request)


def _pop_request():
    """Pop request from request stack. Be sure to do this at end of request ;)"""
    try:
        _local.request_stack.pop()
    except (AttributeError, IndexError):
        raise AssertionError('No requests on request stack.')


def _get_request():
    try:
        return _local.request_stack[-1]
    except (AttributeError, IndexError):
        raise AssertionError("'No request registered. If you are trying to use "
                             "Flango\'s request from outside a Flango view, "
                             "you must install the global_request_middleware'")


request = LocalProxy(_get_request, 'request')
