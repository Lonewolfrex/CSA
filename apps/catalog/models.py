from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Genre(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#007bff")
    
    class Meta:
        verbose_name_plural = "Genres"
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField(Genre)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    stock_count = models.PositiveIntegerField(default=10)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'pk': self.pk})

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Purchase'),
        ('rent', 'Rental'),
        ('return', 'Return'),
        ('donate', 'Donation'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    quantity = models.PositiveIntegerField(default=1)
    rent_days = models.PositiveIntegerField(default=7, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.get_transaction_type_display()})"
