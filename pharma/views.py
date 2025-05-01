from urllib import request
from urllib import request

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .forms import pharma_form
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import Categories
from .models import Pharma
from .models import Approval
from .forms import cart_form

def product(request, categor):
    options = Categories.objects.filter(category=categor).first()
    option = Pharma.objects.filter(categor=options, Approval=True)
    return render(request, 'pharma/product.html', context={"popular_items": option})

def category(request):
    option = Categories.objects.all()
    return render(request, 'pharma/category.html', context={'categories':option})

def item(request,name, id):
    option = Pharma.objects.filter(name=name, id=id).first()
    form = cart_form()
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_item = cart_form(request.POST)
            if cart_item.is_valid():
                name = cart_item.save(commit=False)
                quantity = request.POST.get('quantity')
                if quantity == '':
                    messages.error(request, 'Please enter a quantity.')
                    return redirect('item', name=name, id=id)
                name.quantity = quantity
                name.user = request.user
                name.name = option
                name.save()
                messages= f"{quantity} added to cart successfully "
                return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages})
        else:
            messages.error(request, 'You need to be logged in to add items to your cart.')
            return redirect('login')
    else:
        form = cart_form()  
    return render(request, 'pharma/item.html', context={"item": option, "form": form})

def profile(request):
    return render(request, 'pharma/profile.html', context={})

# Create your views here.
def index(request):
    return render(request, 'pharma/test.html', context = {
    "categories": [
        {"image": "images/10802284-removebg-preview.png", "title": "Vitamins and Supplements"},
        {"image": "images/e01a6ff2-3a78-4a34-8d64-82cf884ff9a7-removebg-preview.png", "title": "Antimalaria"},
        {"image": "images/2010.i121.044_isometric_gastroenterology_set-01-03-removebg-preview.png", "title": "Antibiotics"},
        {"image": "images/3644225-removebg-preview.png", "title": "Painkillers"},
    ],
    "popular_items": [
        {"image": "images/2024-08-08-66b4fdf35f7ae.WEBP", "title": "N/factor Vitamin C 1000mg"},
        {"image": "images/2024-08-08-66b51bee6ba9e.WEBP", "title": "N/factor Vitamin C 1000mg"},
        {"image": "images/2024-08-08-66b51c324e992.WEBP", "title": "N/factor Vitamin C 1000mg"},
        {"image": "images/2024-08-08-66b5010de8c82.WEBP", "title": "N/factor Vitamin C 1000mg"},
    ]
}
)


def login(request):
    form = NewUserForm()
    return render(request, 'pharma/login.html',  context={"form":form})



def register(request):
    if request.method == "POST":

       form = NewUserForm(request.POST)
       if form.is_valid():

           # seller = request.POST.get('user_type')
           # if seller == 'Seller':
           #     user = form.save()
           #     name = request.POST.get('username')
           #     group = get_object_or_404(Group, name='sellers')
           #     name.groups.add(group)
           #     return redirect('login')

           email = request.POST.get("email")
           message = send_email(request, messages='', subjects="Welcome to PharmaDeals", emails=email, html='email/welcome.html')
           user = form.save()
           return redirect('login')
       else:
            # Form is not valid, errors will be passed to the template
            return render(request, 'pharma/register.html', {'form': form})


    form= NewUserForm()
    text= "Register"
    return render(request=request, template_name="pharma/register.html", context={"form":form, 'text':text})

@login_required
def pharma_upload(request):
    text= "Upload your product"
    if request.method == 'POST':
        form = pharma_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            email = request.user.email
            message = send_email(request, messages="", subjects="product added successfully", emails=email, html='email/upload.html')
            success= "Your product has been uploaded"
            return render(request, 'pharma/register.html', {'success': success, 'none':'none'})
    else:
        form = pharma_form()
    return render(request, 'pharma/register.html', {'form': form, 'text':text})


def send_email(request, messages,subjects, emails, html ):
    email = emails
    subject = subjects
    message = messages
    from_email = 'admin@pharmadeals.ng'
    html_message = render(request, html, {}).content.decode('utf-8')
    send_mail(subject, message, from_email, [email], html_message=html_message)
    f = open('email.txt', 'a')
    f.write(f'email sent to {email} \n')
    f.close()
    return f'email sent to {email}'

