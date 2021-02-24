from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder':'Product Title',
                'class': 'form-control'
                }),
            'desc': forms.Textarea(attrs={
                'placeholder':'Product Description',
                'class': 'form-control'
                }),
            'price': forms.NumberInput(attrs={
                'placeholder':'Starting Bid',
                'class': 'form-control'
                }),
            'image': forms.TextInput(attrs={
                'placeholder':'Image URL',
                'class': 'form-control'
                }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        fields = ['title','desc','price','image','category']