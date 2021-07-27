from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
   path('', views.show_all_news, name = 'news'),
   path('<int:pk>', views.ArticleEuroDetail, name = 'article'),
   path('sync', views.sync_news, name = 'sync'),
]