from django.urls import path
from . import views

urlpatterns =[
    path('', views.home_page, name='home_page'),
    path('home', views.home_page, name='home_page'),
    path('search',views.search,name='search'),
    path('overview',views.overview,name='overview')
] 