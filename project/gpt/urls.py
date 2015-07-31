from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/', views.search, name='search'),
    #url(r'^results/(?P<result_set_id>[0-9]+)/$', views.results, name='results'),
    url(r'^results/(?P<pk>[0-9]+)/$', views.ResultView.as_view(), name='result'),
]

