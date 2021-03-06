from django.conf.urls import url
from . import views

app_name = 'bitter'
urlpatterns = [
    # https://docs.python.org/2.7/howto/regex.html
    url(r'^$', views.index , name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^bitts/$', views.bitts, name='bitts'),
    url(r'^submit/$', views.bitt_submit, name='submit'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<username>\w{0,30})/$', views.users, name='user'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^unfollow/$', views.unfollow,  name='unfollow'),
]
