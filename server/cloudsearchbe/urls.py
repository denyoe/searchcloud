from django.conf.urls import url
from . import views

app_name = 'cloudsearchbe'


urlpatterns = [

    #url(r'^cloudsearchbe$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^find_keywords', views.find_keywords, name='find_keywords'),
    url(r'^search_fetch', views.find_keywords, name='search_fetch'),
    url(r'^get_engines', views.find_keywords, name='get_engines'),
]