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
    stock_count = models.PositiveIntegerField(default=10)  # TOTAL stock
    available_stock = models.PositiveIntegerField(default=10)  # AVAILABLE stock
    is_available = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Auto-update availability
        self.is_available = self.available_stock > 0
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'pk': self.pk})    
    def __str__(self):
        return f"{self.title} ({self.available_stock} available)"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('rent', 'Rent'),
        ('return', 'Return'),
    ]
    
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, cancelled
    quantity = models.PositiveIntegerField(default=1)
    rent_days = models.PositiveIntegerField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.transaction_type})"
