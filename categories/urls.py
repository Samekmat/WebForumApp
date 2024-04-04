from django.urls import path
from .views import CategoryListCreateAPIView

app_name = 'categories'

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category_list_create'),
]
