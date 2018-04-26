from django.http import HttpResponse

from flango import render_template, request

from testproject import app


@app.route('/test')
def test():
    return request.GET['test']


@app.route('/kwarg/<val>')
def kwargs(val):
    return val


@app.route('/int/<int:val>')
def int_param(val):
    return type(val).__name__


def django_view(django_request):
    return HttpResponse(request.GET['v'])


@app.route('/template/<val>')
def template(val):
    return render_template('test.html', val=val)
