"""
Catalog App URLs - CSA Library
"""
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/buy/', views.buy_books, name='buy_books'),
    path('books/rent/', views.rent_books, name='rent_books'),
    path('books/return/', views.return_books, name='return_books'),
    path('books/donate/', views.donate_books, name='donate_books'),
]
