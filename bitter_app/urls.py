from django.conf.urls import url
from . import views

app_name = 'bitter'
urlpatterns = [
    # root: /
    url(r'^$', views.index , name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^signup/$', views.signup, name='signup'),
]
