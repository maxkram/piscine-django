from django.urls import path
from . import views

urlpatterns = [
    path('init', views.my_view, name='my_view'),
]