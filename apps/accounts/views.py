from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.catalog.models import Transaction 
from django.db.models import Count, Q
from django.core.paginator import Paginator

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def profile(request):
    # ALL transactions for user with pagination
    transactions = Transaction.objects.filter(
        user=request.user
    ).select_related('book__author').order_by('-created_at')
    
    paginator = Paginator(transactions, 10)  # 10 per page
    page_number = request.GET.get('page')
    transactions_page = paginator.get_page(page_number)
    
    context = {
        'transactions': transactions_page,  # Paginated
        'user': request.user,
        'total_transactions': transactions.count(),
        'total_spent': sum(t.total_amount for t in transactions[:10])  # Recent spending
    }
    return render(request, 'profile.html', context)