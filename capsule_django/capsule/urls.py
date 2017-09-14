from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'keygen/(?P<id>.+)/(?P<scheme>.+)/$', views.keygen),
    url(r'bootstrap/(?P<key_id>.+)/$', views.bootstrap),
    url(r'decrypt/(?P<key_id>.+)/$', views.decrypt)
]
