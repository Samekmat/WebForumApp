from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from threads.models import Thread, Post


class SearchAPIView(APIView):
    def get(self, request):
        search_query = request.GET.get('text', '')

        if not search_query:
            return Response({"error": "Search query is empty"}, status=status.HTTP_400_BAD_REQUEST)

        threads = (Thread.objects.filter(title__icontains=search_query) |
                   Thread.objects.filter(opening_post__icontains=search_query))

        post_threads = Post.objects.filter(text__icontains=search_query).values_list('thread', flat=True)

        post_threads = Thread.objects.filter(id__in=post_threads)
        threads |= post_threads

        if not threads:
            return Response({"error": "No matches found"}, status=status.HTTP_404_NOT_FOUND)

        search_results = {}

        for thread in threads:
            thread_snippets = []

            if search_query.lower() in thread.title.lower():
                snippet_start = max(thread.title.lower().find(search_query.lower()) - 50, 0)
                snippet_end = min(thread.title.lower().find(search_query.lower()) + len(search_query) +
                                  50, len(thread.title))
                snippet = "..." + thread.title[snippet_start:snippet_end] + "..."
                thread_snippets.append(snippet)
            if search_query.lower() in thread.opening_post.lower():
                snippet_start = max(thread.opening_post.lower().find(search_query.lower()) - 50, 0)
                snippet_end = min(thread.opening_post.lower().find(search_query.lower()) +
                                  len(search_query) + 50, len(thread.opening_post))
                snippet = "..." + thread.opening_post[snippet_start:snippet_end] + "..."
                thread_snippets.append(snippet)
            search_results[thread.id] = thread_snippets

        return Response({"searchResults": search_results}, status=status.HTTP_200_OK)
