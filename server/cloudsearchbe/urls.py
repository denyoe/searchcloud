from django.conf.urls import url
from . import views

app_name = 'cloudsearchbe'


urlpatterns = [

    #url(r'^cloudsearchbe$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
    url(r'^api/id', views.welcome, name='welcome'),
    url(r'^api/keywords', views.find_keywords, name='keywords'),
    url(r'^api/search_fetch', views.get_search_fetch, name='search_fetch'),
    # cannot call it search_fetch_by_types because Django will mingle with the previous one
    url(r'^api/res_by_types', views.get_res_by_types, name='res_by_types'),
    url(r'^api/engines', views.get_engines, name='engines'),
]
