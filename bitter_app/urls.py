from django.conf.urls import url
from . import views

app_name = 'bitter'
urlpatterns = [
    # root: /
    url(r'^$', views.index , name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^bitts/$', views.bitts, name='bitts'),
]
