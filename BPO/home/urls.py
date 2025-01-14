from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_render,name='home'),
    path('home',views.home_render,name='home')
]