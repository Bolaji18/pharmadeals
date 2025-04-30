from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pharma


class pharma_form(forms.ModelForm):
    class Meta:
        model = Pharma
        exclude = ['user']


        widgets = {

            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the price of your product'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a description of your product'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the name of the product'}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How many items do you have in stock?'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the category of your product'}),
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
        help_text='I agree to the terms and conditions to register.',
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
