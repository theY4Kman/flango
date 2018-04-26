import pytest

from flango import Flango, url_for


@pytest.mark.parametrize('pattern,uri', [
    ('/', '/'),
    ('/test', '/test'),
    ('/param/<val>', '/param/42')
])
def test_urlpatterns(pattern, uri):
    app = Flango('test')

    @app.route(pattern)
    def route(*kwargs):
        pass

    urlpatterns = list(app.urlpatterns)
    assert len(urlpatterns) == 1
    assert urlpatterns[0].resolve(uri.lstrip('/'))


def test_global_request(client):
    response = client.get('/test?test=unique')
    assert response.content == b'unique'


def test_view_params(client):
    response = client.get('/kwarg/uneek')
    assert response.content == b'uneek'


def test_param_converters(client):
    response = client.get('/int/42')
    assert response.content == b'int'


def test_request_fails_outside_flango_view_without_middleware(client):
    with pytest.raises(AssertionError):
        client.get('/django?v=test')


def test_request_outside_flango_view_with_middleware(client, settings):
    settings.MIDDLEWARE += ('flango.global_request_middleware',)
    response = client.get('/django?v=test')
    assert response.content == b'test'


def test_render_template(client):
    response = client.get('/template/unique')
    assert response.content.strip() == b'unique'


def test_url_for(client):
    assert url_for('template', val='unique') == '/template/unique'
