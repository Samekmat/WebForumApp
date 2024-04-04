from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('categories.urls')),
    path('', include('threads.urls')),
    path('', include('search.urls')),
    path('', include('csv_import.urls')),
]
