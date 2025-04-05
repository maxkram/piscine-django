from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, UserFavouriteArticle

class HomeView(RedirectView):
    url = '/articles/'

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'

class LoginView(AuthLoginView):
    template_name = 'articles/login.html'
    redirect_authenticated_user = True

class PublicationListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/publication_list.html'
    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'

class LogoutView(AuthLogoutView):
    next_page = '/'

class FavouriteListView(LoginRequiredMixin, ListView):
    model = UserFavouriteArticle
    template_name = 'articles/favourite_list.html'
    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(user=self.request.user)