from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all, name='list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'(?P<pk>\d+)/$', views.list_detail, name='detail'),
    url(r'^create_list/$', views.create_list,
        name='create_list'),
    url(r'(?P<list_pk>\d+)/create_rest/$', views.create_rest,
        name='create_rest'),
]