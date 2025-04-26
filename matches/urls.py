from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='match_list'),
    path('filter/', views.filter_matches, name='filter_matches'),
]
