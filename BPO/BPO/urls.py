from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('home.urls')),
    path('',include('upload.urls')),
    path('',include('complaints.urls')),
    path('',include('talk.urls')),
    path('',include('chat.urls')),
    path('admin/', admin.site.urls),
]
