from django.urls import path

from .views import ImportUsersFromCSVAPIView

app_name = 'csv_import'

urlpatterns = [
    path('csv/', ImportUsersFromCSVAPIView.as_view(), name='import'),
]
