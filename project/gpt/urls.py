from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^results/(?P<result_set_id>[0-9]+)/$', views.results, name='results'),
]

