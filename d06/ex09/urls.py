from django.urls import path
from . import views

urlpatterns = [
	path('display/', views.display_view, name='display_view'),
]