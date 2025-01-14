from django.urls import path
from . import views

urlpatterns = [
    path('complaints',views.complaintsViewer,name = 'complaints'),
]