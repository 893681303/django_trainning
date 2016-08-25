from django.conf.urls import include, url
from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.posts_list, name='list'),
    url(r'^create/$' , views.posts_create, name='create'),
    url(r'^(?P<slug>[\w-]+)/$', views.posts_detail, name='detail'),
    url(r'^(?P<id>\d+)/edit/$', views.posts_update, name='update'),
    url(r'^(?P<id>\d+)/delete/$', views.posts_delete, name='delete'),

]