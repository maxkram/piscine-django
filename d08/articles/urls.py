from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('login/', views.LoginView.as_view(), name='login'),
]