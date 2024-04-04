from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from WebForumApp import settings
from categories.models import Category
from categories.serializers import CategorySerializer


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        if 'category' in request.query_params:
            return self.delete(request)

        user_id = request.COOKIES.get('User-Id')

        user = User.objects.get(id=user_id)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data

        for item in response_data:
            for key, value in item.items():
                if key == 'author':
                    item[key] = user.username

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        admin_api_key = request.headers.get('Token')
        session_cookie = request.COOKIES.get('Set-Cookie')

        if not admin_api_key or not session_cookie:
            raise AuthenticationFailed("Unauthorized. Missing admin API key or session cookie.")

        if admin_api_key != settings.ADMIN_API_KEY:
            raise AuthenticationFailed("Invalid admin API key.")

        categories_data = request.data.get('categories', [])
        categories_data = [{"name": category_name} for category_name in categories_data]
        serializer = self.get_serializer(data=categories_data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        admin_api_key = request.headers.get('Token')
        if admin_api_key != settings.ADMIN_API_KEY:
            return Response({"error": "Admin API key is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        category = request.query_params.get('category')
        if not category:
            return Response({"error": "Category is missing"}, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.get(name=category)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
