from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavouriteArticle

class SiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.article = Article.objects.create(
            title='Test Article', author=self.user, synopsis='Test synopsis', content='Test content'
        )

    def test_favourites_view_authenticated_only(self):
        response = self.client.get(reverse('articles:favourites'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('articles:favourites'))
        self.assertEqual(response.status_code, 200)

    def test_publications_view_authenticated_only(self):
        response = self.client.get(reverse('articles:publications'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('articles:publications'))
        self.assertEqual(response.status_code, 200)

    def test_publish_view_authenticated_only(self):
        response = self.client.get(reverse('articles:publish'))
        self.assertEqual(response.status_code, 302)
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('articles:publish'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_unauthenticated_only(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('articles:register'))
        self.assertEqual(response.status_code, 302)  # Redirect for authenticated
        self.client.logout()
        response = self.client.get(reverse('articles:register'))
        self.assertEqual(response.status_code, 200)

    def test_no_duplicate_favourites(self):
        self.client.login(username='testuser', password='testpass')
        UserFavouriteArticle.objects.create(user=self.user, article=self.article)
        response = self.client.post(reverse('articles:add_to_favourite', kwargs={'pk': self.article.pk}))
        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)