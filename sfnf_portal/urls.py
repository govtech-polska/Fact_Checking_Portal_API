"""sfnf_portal URL Configuration """
from django.urls import path, include


urlpatterns = [
    path('', include('news.urls')),
]
