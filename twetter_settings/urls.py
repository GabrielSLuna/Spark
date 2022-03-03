from django.contrib import admin
from django.urls import path
from app_twetter import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('send_to_producer', views.send_to_producer, name='send_producer'),
    path('graph_tweet', views.graph_tweet, name='graph_tweet'),
    path('shp_layer', views.get_layer),
    path('get_word_frequency', views.get_words_frequency),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)