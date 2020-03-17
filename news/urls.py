from django.urls import path

from . import views

urlpatterns = [
    path('', views.health_check),
    path('news', views.NewsList.as_view()),
    path('news/<uuid:pk>', views.NewsDetail.as_view()),
]
