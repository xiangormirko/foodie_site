from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list_all, name='list'),
    url(r'edit_list/(?P<list_pk>\d+)/$', views.list_edit,
        name='edit_list'),
    url(r'profile/$', views.profile_page,
        name='profile'),
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.user_login, name='login'),
    url(r'chat/$', views.chat_room, name='chat'),
    url(r'logout/$', views.user_logout, name='logout'),
    url(r'(?P<list_pk>\d+)/edit_rest/(?P<rest_pk>\d+)/$', views.rest_edit, name='edit_rest'),
    url(r'(?P<pk>\d+)/$', views.list_detail, name='detail'),
    url(r'create_list/$', views.create_list,
        name='create_list'),
    url(r'(?P<list_pk>\d+)/create_rest/$', views.create_rest,
        name='create_rest'),
    url(r'search/$', views.search,
        name='search'),
    url(r'recommend/$', views.recommend,
        name='recommend'),
]
