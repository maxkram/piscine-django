from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('publications/', views.PublicationListView.as_view(), name='publications'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('favourites/', views.FavouriteListView.as_view(), name='favourites'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('publish/', views.PublishView.as_view(), name='publish'),
    path('article/<int:pk>/add-to-favourite/', views.AddToFavouriteView.as_view(), name='add_to_favourite'),
]