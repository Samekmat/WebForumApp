import csv
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from WebForumApp import settings


class ImportUsersFromCSVAPIView(APIView):
    def post(self, request):

        admin_api_key = request.headers.get('Token')
        if admin_api_key != settings.ADMIN_API_KEY:
            return Response({"error": "Admin API key is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            next(csv_reader)

            users_to_create = []
            for row in csv_reader:
                if len(row) != 3:
                    return Response({'error': 'Invalid CSV format'}, status=status.HTTP_400_BAD_REQUEST)
                username, password, email = row
                user = User(username=username, email=email)
                user.set_password(password)
                users_to_create.append(user)

            User.objects.bulk_create(users_to_create)

            return Response({'message': 'Users imported successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
