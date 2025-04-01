from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_tip/', views.create_tip, name='create_tip'),
    path('vote/<int:tip_id>/<str:vote_type>/', views.vote, name='vote'),
    path('delete_tip/<int:tip_id>/', views.delete_tip, name='delete_tip'),
]