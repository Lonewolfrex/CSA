from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
from .models import Book, Transaction, Genre, Author
from .forms import BuyBookForm, RentBookForm
from django.conf import settings
import os

@login_required
def home(request):
    """Home page - redirect to dashboard"""
    return render(request, 'home.html')
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).select_related('book__author').order_by('-created_at')[:10]
    
    stats = transactions.aggregate(
        total_buys=Count('id', filter=Q(transaction_type='buy')),
        total_rents=Count('id', filter=Q(transaction_type='rent')),
        total_returns=Count('id', filter=Q(transaction_type='return')),
        total_donations=Count('id', filter=Q(transaction_type='donate'))
    )
    
    context = {
        'transactions': transactions,
        **stats
    }
    return render(request, 'dashboard.html', context)

@login_required
def profile(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    context = {
        'transactions': transactions,
        'user': request.user
    }
    return render(request, 'profile.html', context)

@login_required
def buy_books(request):
    books = Book.objects.filter(is_available=True, stock_count__gt=0).select_related('author').prefetch_related('genre')
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        book = get_object_or_404(Book, id=book_id, is_available=True, stock_count__gte=quantity)
        
        Transaction.objects.create(
            user=request.user,
            book=book,
            transaction_type='buy',
            status='completed',
            quantity=quantity,
            amount=book.price * Decimal(quantity)
        )
        
        book.stock_count -= quantity
        book.save()
        
        messages.success(request, f'Successfully purchased {quantity} copy/copies of "{book.title}"!')
        return redirect('catalog:buy_books')
    
    return render(request, 'buy_books.html', {'books': books})

@login_required
def rent_books(request):
    books = Book.objects.filter(is_available=True, stock_count__gt=0).select_related('author').prefetch_related('genre')
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rent_days = int(request.POST.get('rent_days'))
        book = get_object_or_404(Book, id=book_id, is_available=True, stock_count__gt=0)
        
        Transaction.objects.create(
            user=request.user,
            book=book,
            transaction_type='rent',
            status='completed',
            quantity=1,
            amount=book.price * Decimal(rent_days),
            rent_days=rent_days
        )
        
        book.stock_count -= 1
        book.save()
        
        messages.success(request, f'Successfully rented "{book.title}" for {rent_days} days!')
        return redirect('catalog:rent_books')
    
    return render(request, 'rent_books.html', {'books': books})

@login_required
def return_books(request):
    transactions = Transaction.objects.filter(
        user=request.user, 
        transaction_type='rent',
        status='completed'
    ).select_related('book').order_by('-created_at')
    return render(request, 'return_books.html', {'transactions': transactions})

@login_required
def donate_books(request):
    if request.method == 'POST':
        # Handle donation form
        title = request.POST.get('title')
        author_name = request.POST.get('author')
        messages.success(request, f'Thank you for donating "{title}"!')
        return redirect('catalog:donate_books')
    
    return render(request, 'donate_books.html')
