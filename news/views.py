from rest_framework import generics
from news.models import News
from news.serializers import NewsSerializer, NewsDetailSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def health_check(request):
    return Response()


class NewsList(generics.ListAPIView):
    """
    API endpoint that allows news to be listed.
    """

    queryset = News.objects.published_news().order_by("-created_at")
    serializer_class = NewsSerializer


class NewsDetail(generics.RetrieveAPIView):
    """
    Retrieve a news instance.
    """


    queryset = News.objects.published_news()
    serializer_class = NewsDetailSerializer
