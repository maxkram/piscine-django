from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('upvote/<int:tip_id>/', views.upvote_tip, name='upvote_tip'),
    path('downvote/<int:tip_id>/', views.downvote_tip, name='downvote_tip'),
    path('delete/<int:tip_id>/', views.delete_tip, name='delete_tip'),
]