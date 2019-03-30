from django.conf.urls import url
from . import views

app_name = 'cloudsearchbe'


urlpatterns = [

    #url(r'^cloudsearchbe$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^api/keywords', views.find_keywords, name='keywords'),
    url(r'^api/search_fetch', views.get_search_fetch, name='search_fetch'),
    url(r'^api/engines', views.get_engines, name='engines'),
]