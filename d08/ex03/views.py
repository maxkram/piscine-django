from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, UserFavouriteArticle
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, PublishForm

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
    
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'articles/register.html'
    success_url = reverse_lazy('articles:login')

class PublishView(LoginRequiredMixin, CreateView):
    form_class = PublishForm
    template_name = 'articles/publish.html'
    success_url = reverse_lazy('articles:publications')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddToFavouriteView(LoginRequiredMixin, CreateView):
    model = UserFavouriteArticle
    fields = []
    template_name = 'articles/add_to_favourite.html'
    def get_success_url(self):
        return reverse_lazy('articles:detail', kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)