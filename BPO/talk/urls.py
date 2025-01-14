from django.urls import path
from . import views

urlpatterns = [
    path('talk', views.talker_file, name='talk'),

]