from django import forms
from .models import Book

class BuyBookForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, 
        max_value=10,  # Max 10 per purchase
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'min': '1', 
            'max': '10'
        })
    )

class RentBookForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    rent_days = forms.ChoiceField(
        choices=[(7, '1 Week'), (14, '2 Weeks'), (30, '1 Month')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class DonateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }
