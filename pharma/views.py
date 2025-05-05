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
from .models import cart
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from .forms import buyerinfo_form
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import bought
from .models import boughtitem


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
                messages= f"{quantity} items added to cart successfully "
                return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages, 'display': 'block'})
        else:
              messages= f"pls login to add item to cart"
              return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages, 'display': 'block'})
    else:
        form = cart_form()  
    message ="you can add item to cart"
    return render(request, 'pharma/item.html', context={"item": option, "form": form, 'display': 'none', 'message': message,})

def profile(request):
    return render(request, 'pharma/profile.html', context={})

# Create your views here.
def index(request):
    cate = Categories.objects.all()[:4]
    #cate = Categories.objects.all().order_by('id')[:4]

    return render(request, 'pharma/home.html', context = {
    "categories": cate,
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
           name = request.POST.get("first_name")
           message = send_email(request, messages='', subjects="Welcome to PharmaDeals", emails=email, html='email/welcome.html',  context={'name': name} )
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
            name = request.user.first_name
            message = send_email(request, messages='', subjects="Product upload", emails=email, html='email/upload.html', context={'name': name})
            success= "Your product has been uploaded"
            return render(request, 'pharma/register.html', {'success': success, 'none':'none'})
    else:
        form = pharma_form()
    return render(request, 'pharma/register.html', {'form': form, 'text':text})



def send_email(request, messages, subjects, emails, html, context=None):
    email = emails
    subject = subjects
    message = messages
    from_email = 'admin@pharmadeals.ng'
    
    # Render the HTML template with context
    html_message = render_to_string(html, context or {})
    
    send_mail(subject, message, from_email, [email], html_message=html_message)
    
    # Log the email for debugging
    with open('email.txt', 'a') as f:
        f.write(f'Email sent to {email} with subject "{subject}"\n')
    
    return f'Email sent to {email}'

def get_pharma(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            name = request.user
            pharma = cart.objects.filter(user=name).count()
            return render(request, 'pharma/cart.html', {'pharma': pharma})
           
    else:
        return JsonResponse({"error": "invalid request"}, status=400)

def see_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = buyerinfo_form(request.POST)
            if form.is_valid():
                name = form.save(commit=False)
                name.user = request.user
                method = request.POST.get('method')
                email = request.POST.get('email')
                name2 = request.POST.get('name')
                name.save()
                cart_items = cart.objects.filter(user=name.user)
                
                if method == "2":
                    message = send_email(request, messages="", subjects="order is being processed", emails=email, html='email/process.html',  context={'name': name2} )
                    text = "Your order is being processed, please wait for a confirmation email. Thank you for your order."
                    
                    cart_items = cart.objects.filter(user=name.user)
                    for item in cart_items:   
                        email = item.name.user.email
                        users = item.name.user.username
                        name = item.name.user.first_name
                        product_name = item.name.name
                        quantity = item.quantity
                        total_earned = item.name.price * item.quantity
                        order_id = item.id
                        bought_item = boughtitem.objects.create(email=email, name=name, users=users, product_name=product_name, quantity=quantity, total_earned=total_earned, order_id=order_id)
                        bought_item.save()

                        message = send_email(request, messages="", subjects="Item bought on Pharmadeals", emails=email, html='email/bought.html',  context={'username': name, 'product_name':product_name,'quantity':quantity, 'total_earned':total_earned,'order_id':order_id } )
                    return render(request, 'pharma/register.html', {'text': text})
                    
                
                return redirect('index')
            else:
               return render(request, 'pharma/cart_total.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form, 'item': item})
        
        name = request.user
        cart_items = cart.objects.filter(user=name)
        total_price = 0
        item = []
        for item in cart_items:
            option = get_object_or_404(Pharma, id=item.name.id)
            total_price += option.price * item.quantity
        form = buyerinfo_form()
        return render(request, 'pharma/cart_total.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form, 'item': item})
    else:
        return redirect('login')
    
def remove_from_cart(request, id):
    if request.method == 'POST':
     if request.user.is_authenticated:
        cart_item = get_object_or_404(cart, id=id)
        cart_item.delete()
        return redirect('see_cart')
    else:
        return redirect('login')


