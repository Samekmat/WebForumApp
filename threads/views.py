from rest_framework import generics, status, viewsets
from rest_framework.response import Response


from WebForumApp import settings
from .models import Thread
from .serializers import ThreadListSerializer, ThreadCreateSerializer, PostSerializer


class ThreadViewSet(viewsets.ViewSet):
    queryset = Thread.objects.all()

    def list(self, request):
        if 'id' in request.query_params:
            return self.destroy(request)

        if not request.COOKIES.get('Set-Cookie'):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        categories = request.GET.getlist('categories')
        newest_first = request.GET.get('newest_first', False)
        page = request.GET.get('page', 0)
        page_size = request.GET.get('page_size', 10)

        if not categories:
            return Response({"error": "Missing required parameter: categories"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not Thread.objects.filter(category__in=categories).exists():
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        threads = Thread.objects.filter(category__in=categories)

        if newest_first:
            threads = threads.order_by('-created_at')

        start_index = int(page) * int(page_size)
        end_index = start_index + int(page_size)
        threads = threads[start_index:end_index]

        serializer = ThreadListSerializer(threads, many=True)

        return Response({"threads": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        user_id = request.COOKIES.get('User-Id')
        if user_id:
            request.data['author'] = user_id
            serializer = ThreadCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User-Id cookie is missing."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        admin_api_key = request.headers.get('Token')
        if admin_api_key != settings.ADMIN_API_KEY:
            return Response({"error": "Admin API key is missing"}, status=status.HTTP_401_UNAUTHORIZED)

        thread_id = request.query_params.get('id')
        if not thread_id:
            return Response({"error": "Thread ID is missing"}, status=status.HTTP_400_BAD_REQUEST)

        thread = Thread.objects.get(id=thread_id)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadPostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        thread_id = request.GET.get('thread_id')
        try:
            thread = Thread.objects.get(pk=thread_id)
        except Thread.DoesNotExist:
            return Response({"error": "Thread does not exist."}, status=status.HTTP_404_NOT_FOUND)

        posts = thread.posts.all()
        post_serializer = self.get_serializer(posts, many=True)
        response_data = {
            "id": thread.id,
            "category": thread.category,
            "title": thread.title,
            "text": thread.opening_post,
            "author": thread.author.username,
            "createdAt": thread.created_at,
            "posts": post_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        thread_id = request.data.get('thread_id')
        posts_data = request.data.get('posts', [])

        try:
            thread = Thread.objects.get(pk=thread_id)
        except Thread.DoesNotExist:
            return Response({"error": "Thread does not exist."}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.COOKIES.get('User-Id')
        if not user_id:
            return Response({"error": "User-Id cookie is missing."}, status=status.HTTP_400_BAD_REQUEST)

        created_posts = []
        for post_data in posts_data:
            post_data['author'] = user_id
            post_data['thread'] = thread.pk
            serializer = PostSerializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(author_id=user_id, thread_id=thread_id)
            created_posts.append(serializer.data)

        return Response(created_posts, status=status.HTTP_201_CREATED)
