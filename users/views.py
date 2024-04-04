from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            for field in serializer.errors:
                if serializer.errors[field][0] == "A user with that username already exists." \
                        or serializer.errors[field][0] == "A user with that email already exists.":
                    return Response(serializer.errors[field], status=status.HTTP_418_IM_A_TEAPOT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                'username': user.username,
                'email': user.email,
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='Set-Cookie', value=str(access_token), httponly=True, secure=True)
            response.set_cookie(key='User-Id', value=user.id)

            return response

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

