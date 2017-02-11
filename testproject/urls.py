from django.conf.urls import url, include

from testproject import app, views


urlpatterns = [
    url('^django', views.django_view),
    url('', include(app.urlpatterns)),
]
