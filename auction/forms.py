from django import forms
from .models import Listing, Bid, Comment

# Form definition for the Create Listing Form
class ListingForm(forms.ModelForm):
    class Meta:
        # This form inherits from the Listing model
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

# Form definition for the Bid Amount
class BidForm(forms.ModelForm):
    class Meta:
        # This form inherits from the Bid model
        model = Bid
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder':'Bid Amount', 'class': 'form-control'})
        }
    
    # Cleaner function to ensure that the bid is valid
    def clean(self):
        super(BidForm, self).clean()
        item = self.instance.item
        amt = self.cleaned_data.get('amount')
        if item.price >= amt:
            self._errors['amount'] = self.error_class(['Your bid must be higher than the current price.'])
        return self.cleaned_data

# Form definition for the Comment section
class CommentForm(forms.ModelForm):
    class Meta:
        # This form inherits from the Comment model
        model = Comment
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Comment Title', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'placeholder':'Comment', 'class': 'form-control'})
        }