import functools

from django.conf.urls import url
from django.http.response import HttpResponse
from werkzeug.routing import Map, Rule

from flango.request import _push_request, _pop_request


class Flango(object):
    url_rule_class = Rule

    response_class = HttpResponse

    def __init__(self, import_name):
        self.import_name = import_name

        self.url_map = Map()
        self.view_functions = {}

    def route(self, rule, **options):
        """A decorator used to register a view function for a given URL rule.
        This does the same thing as :meth:`add_url_rule` but is intended for
        decorator usage::

            @app.route('/')
            def index():
                return 'Hello World'

        :param rule: the URL rule as string
        :param endpoint: the viewname for the registered URL rule. Flango itself
                         assumes the name of the view function as the endpoint.
        :param options: TODO
        """
        def decorator(f):
            endpoint = options.pop('endpoint', None)
            self.add_url_rule(rule, f, endpoint, **options)
            return f
        return decorator

    def add_url_rule(self, rule, view_func, endpoint=None, **options):
        """Register a URL rule

        :param rule: the URL rule as string
        :param view_func: the function to call when serving a request to the
                          provided endpoint
        :param endpoint: the viewname for the registered URL rule. Flango itself
                         assumes the name of the view function as the endpoint.
        :param options: TODO
        """
        if endpoint is None:
            endpoint = view_func.__name__

        options['endpoint'] = endpoint
        methods = options.pop('methods', None)

        # TODO: allow one django urlpattern to route to different rules

        rule = self.url_rule_class(rule, **options)

        self.url_map.add(rule)
        self.view_functions[endpoint] = self.build_view_wrapper(view_func, rule)

    def build_view_wrapper(self, view, rule):
        """Wrap a view function to eat Django's request argument. Handles
        conversion of route params. Also allows the view function to return a
        string (or Flask-like response tuples).
        """
        @functools.wraps(view)
        def wrapped_view(request, **kwargs):
            _push_request(request)

            for name, converter in rule._converters.iteritems():
                if name in kwargs:
                    kwargs[name] = converter.to_python(kwargs[name])

            try:
                rv = view(**kwargs)
            finally:
                _pop_request()

            return self.make_response(rv)

        return wrapped_view

    def make_response(self, rv):
        """Converts the return value from a view function to a real response
        object that is an instance of :attr:`response_class`.

        The following types are allowed for `rv`:

        .. tabularcolumns:: |p{3.5cm}|p{9.5cm}|

        ======================= ===========================================
        :attr:`response_class`  the object is returned unchanged
        :class:`str`            a response object is created with the
                                string as body
        :class:`unicode`        a response object is created with the
                                string encoded to utf-8 as body
        :class:`tuple`          A tuple in the form ``(response, status,
                                headers)`` or ``(response, headers)``
                                where `response` is any of the
                                types defined here, `status` is a string
                                or an integer and `headers` is a list or
                                a dictionary with header values.
        ======================= ===========================================

        :param rv: the return value from the view function
        """
        status_or_headers = headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None,) * (3 - len(rv))

        if rv is None:
            raise ValueError('View function did not return a response')

        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        if not isinstance(rv, self.response_class):
            if isinstance(rv, (str, unicode)):
                rv = self.response_class(rv, status=status_or_headers)
            else:
                raise ValueError('Content must be a string')

        if status_or_headers is not None:
            if isinstance(status_or_headers, (str, unicode)):
                # FIXME: I'm pretty sure Django's reason_phrase is *just* the
                #        'OK' in '200 OK', whereas Flask allows passing '200 OK'
                rv.reason_phrase = status_or_headers
            else:
                rv.status = status_or_headers

        if headers:
            # HttpResponse doesn't take a headers kwarg, so we must set each
            # header manually with rv[header] = value
            if isinstance(headers, dict):
                headers_iter = headers.iteritems()
            elif isinstance(headers, list):
                headers_iter = headers
            else:
                raise ValueError('headers must be dict, list, or None')

            for header, value in headers_iter:
                rv[header] = value

        return rv

    def iter_urlpatterns(self):
        for rule in self.url_map.iter_rules():
            pattern = rule._regex.pattern

            # First, we remove ^, to ease processing
            pattern = pattern[1:]

            # NOTE: _trace is filled with info about the parts of the URL rule,
            #       and is used to build URLs in the reverse

            # Werkzeug matches literal pipe at the beginning (r'\\|')
            # TODO: figure out why
            if rule._trace[0][1] == '|':
                pattern = pattern[2:]

            # Also, Django strips the first slash, so we remove it from the rule
            # (But only if not the index rule, because Werkzeug doesn't include
            #  that in the pattern)
            if rule._trace[1][1] != '/':
                pattern = pattern[2:]

            # Reinstate sir caret
            pattern = '^' + pattern

            yield url(pattern,
                      self.view_functions[rule.endpoint],
                      name=rule.endpoint)

    @property
    def urlpatterns(self):
        return list(self.iter_urlpatterns())
