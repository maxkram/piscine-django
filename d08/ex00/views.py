from django.views.generic import ListView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView
from .models import Article

class HomeView(RedirectView):
    url = '/articles/'

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'

class LoginView(AuthLoginView):
    template_name = 'articles/login.html'
    redirect_authenticated_user = True  