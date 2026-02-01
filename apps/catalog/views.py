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
from django.db import transaction

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
    books = Book.objects.filter(is_available=True).order_by('-available_stock')
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        
        book = get_object_or_404(Book, id=book_id)
        with transaction.atomic():
            if book.available_stock >= quantity:
                book.available_stock -= quantity
                book.save()
                
                # Create transaction record (SIMULATED payment)
                Transaction.objects.create(
                    user=request.user,
                    book=book,
                    transaction_type='buy',
                    status='completed',
                    quantity=quantity,
                    total_amount=book.price * quantity
                )
                messages.success(request, f'✅ Purchased {quantity}x {book.title}! Stock left: {book.available_stock}')
                return redirect('catalog:buy_books')
            else:
                messages.error(request, f'❌ Not enough stock! Only {book.available_stock} available.')
    
    context = {
        'page_obj': page_obj,
        'view_mode': 'table' if request.GET.get('view') == 'table' else 'cards',
    }
    return render(request, 'buy_books.html', context)


@login_required
def rent_books(request):
    books = Book.objects.filter(is_available=True).order_by('-available_stock')
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        rent_days = int(request.POST.get('rent_days', 7))  # ✅ FIX: Convert to int
        
        book = get_object_or_404(Book, id=book_id)
        with transaction.atomic():
            if book.available_stock >= 1:
                book.available_stock -= 1
                book.save()
                
                total_amount = book.price * rent_days  # ✅ Now works!
                Transaction.objects.create(
                    user=request.user,
                    book=book,
                    transaction_type='rent',
                    status='pending',
                    quantity=1,
                    rent_days=rent_days,
                    total_amount=total_amount
                )
                messages.success(request, f'Rented {book.title} for {rent_days} days!')
                return redirect('catalog:rent_books')
            else:
                messages.error(request, f'{book.title} is not available!')
    
    context = {
        'page_obj': page_obj,
        'view_mode': 'table' if request.GET.get('view') == 'table' else 'cards',
    }
    return render(request, 'rent_books.html', context)

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
