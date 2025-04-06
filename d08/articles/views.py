from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Article, UserFavouriteArticle
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegisterForm, PublishForm
from django.contrib.auth.forms import AuthenticationForm

class PublishView(LoginRequiredMixin, CreateView):
    form_class = PublishForm
    template_name = 'articles/publish.html'
    success_url = reverse_lazy('articles:publications')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class HomeView(RedirectView):
    url = '/articles/'

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    ordering = ['-created']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = AuthenticationForm()
        return context

class LoginView(AuthLoginView):
    template_name = 'articles/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('articles:articles')

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

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'articles/register.html'
    success_url = reverse_lazy('articles:login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('articles:home')  # Redirect authenticated users
        return super().dispatch(request, *args, **kwargs)
    
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
        # Check if the favorite already exists
        if UserFavouriteArticle.objects.filter(
            user=self.request.user,
            article=Article.objects.get(pk=self.kwargs['pk'])
        ).exists():
            # If it exists, redirect without creating a duplicate
            return self.get(self.request)
        # Otherwise, proceed with creation
        form.instance.user = self.request.user
        form.instance.article = Article.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
class LogoutView(AuthLogoutView):
    # template_name = 'articles/logout.html'
    # next_page = '/'
    next_page = reverse_lazy('articles:home')