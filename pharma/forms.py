from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pharma
from .models import cart
from .models import buyerinfo
from .models import help
from .models import bid



class UsernamePasswordResetForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    widgets = {
            'username' : forms.NumberInput(attrs={ 'class': 'form-control',  'placeholder':'Enter your Username'}),
     }


class bid_form(forms.ModelForm):
    class Meta:
        model = bid
        fields = [ 'bid_price', 'message', 'phone', 'email', 'address']
        widgets = {
            'bid_price' : forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Enter the price of your product'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
            'phone': forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        }
        help_texts = {
            'price': 'Price must be greater than 0',
            'message': 'Message must be at least 10 characters long',
            'phone': 'Phone number must be at least 10 digits long',
            'email': 'Email must be a valid email address',
            'address': 'Address must be at least 10 characters long',
        }

class help_form(forms.ModelForm):
    class Meta:
        model = help
        fields = ['subject', 'name', 'email', 'phone', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the subject'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your message'}),
        }

class buyerinfo_form(forms.ModelForm):
    class Meta:
        model = buyerinfo
        fields = ['name', 'email', 'phone', 'address', 'method']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
        }


class pharma_form(forms.ModelForm):
    class Meta:
        model = Pharma
        exclude = ['user', 'Approval']


        widgets = {

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the price of your product'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a description of your product'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the product'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How many items do you have in stock?'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the category of your product'}),
            'shipping': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the shipping cost of your product'}),
        }
        help_texts = {
            'shipping': 'Leave empty if no shipping cost',
            'stock': 'Stock must be greater than 0',
            'price': 'Price must be greater than 0',
            'description': 'Description must be at least 10 characters long',
            'name': 'Name must be at least 3 characters long',
            'category': 'Choose a category for your product',
        }
class cart_form(forms.ModelForm):
    class Meta:
        model = cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the quantity'}),
        }
        help_texts = {
            'quantity': 'Quantity must be greater than 0',
        }

class NewUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required. Add a valid email address.'
    )
    user_type = forms.ChoiceField(
        choices=[('Buyer', 'Buyer'), ('Seller', 'Seller')],
        required=True,
        initial='Buyer',
        label='User type',
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        initial=False,
        label='Agree to Terms',
        help_text='I agree to the terms and conditions to register. ',
    )

    class Meta:
        model = User
        fields = ["username", "email",'first_name', 'last_name', "password1", "user_type", "agree_to_terms"]

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']  # Save user_type field
        if commit:
            user.save()
        return user
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text=None
        self.fields['password2'].help_text=None
