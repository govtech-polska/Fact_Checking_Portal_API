import uuid
from django.test import TestCase
from news.models import News


class NewsModelTestCase(TestCase):
    def setUp(self):
        News.objects.create(title="Fake news", image="https://image.jpg")

    def test_news_id_is_uuid(self):
        news = News.objects.get(title="Fake news")
        self.assertEqual(type(news.id), uuid.UUID)

    def test_news_available_fields(self):
        title = "Fake news"
        image = "https://image.jpg"

        news = News.objects.create(title=title, image=image)

        self.assertEqual(news.title, title)
        self.assertEqual(news.image, image)
        assert news.created
