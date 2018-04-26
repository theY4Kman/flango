from flango._request import request_stack


def global_request_middleware(get_response):
    """Save request object to thread local"""

    def middleware(request):
        request_stack.push(request)
        response = get_response(request)
        request_stack.pop()
        return response

    return middleware
