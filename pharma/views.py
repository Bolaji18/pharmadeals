from urllib import request
from urllib import request
import matplotlib.pyplot as plt
import io
import urllib, base64
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
from .models import buyerinfo
from .models import popular
from .models import cart
from .models import Pharma
from .forms import help_form
from django.views.decorators.csrf import csrf_exempt
from .models import searchProduct
from .forms import bid_form
from datetime import datetime
from .models import bid
# search for products 
from django.http import JsonResponse
from django.core.paginator import Paginator

# from django.db.models import Case, When, Value, IntegerField

# def product_list_api(request):
#     page = int(request.GET.get('page', 1))
#     per_page = 8
#     category_id = request.GET.get('category_id')  # or whatever parameter you use

#     # Annotate: 0 if product is in the selected category, 1 otherwise
#     products = Pharma.objects.filter(Approval=True).annotate(
#         category_priority=Case(
#             When(categor_id=category_id, then=Value(0)),
#             default=Value(1),
#             output_field=IntegerField(),
#         )
#     ).order_by('category_priority', 'id')  # category first, then by id

#     paginator = Paginator(products, per_page)
#     page_obj = paginator.get_page(page)
#     data = []
#     for item in page_obj:
#         data.append({
#             'id': item.id,
#             'name': item.name,
#             'price': item.price,
#             'image_url': item.image.url,
#             'shipping': item.shipping,
#         })
#     return JsonResponse({'items': data, 'has_next': page_obj.has_next()})


def product_list_api(request):
    page = int(request.GET.get('page', 1))
    per_page = 8  # or whatever your grid shows per "page"
    products = Pharma.objects.filter(Approval=True).order_by('id')
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page)
    data = []
    for item in page_obj:
        data.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'image_url': item.image.url,
            'shipping': item.shipping,
        })
    return JsonResponse({'items': data, 'has_next': page_obj.has_next()})


# function to place a bid and send email
def bids_app(request, id):
    if request.method == 'POST':
     if request.user.is_authenticated:
        form = bid_form(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            name.user = request.user
            email = request.user.email
            name.name = Pharma.objects.get(id=id)
            email2 = Pharma.objects.get(id=id).user.email
            username = Pharma.objects.get(id=id).user.username
            bid_price = request.POST.get('bid_price')
            name.bid_time = datetime.now()
            name.status = "pending"
            subject = f"PharmaDeals Bid Request by {name.user}"
            name.save()
            send_email(request, messages='', subjects=subject, emails=email2, html='email/bid.html', context={'username':username, 'bid_amount': bid_price, 'product_name': name.name.name, 'bidder_username':name.user, 'bid_time': name.bid_time})
            send_email(request, messages='', subjects=subject, emails=email, html='email/bidplaced.html', context={'username':name.user, 'bid_amount': bid_price, 'product_name': name.name.name, 'bid_time': name.bid_time})
            return render(request, 'pharma/register.html', context={ 'none': 'none',  'success': "Your bid has been sent successfully"})
     else:
        option = Pharma.objects.filter(id=id).first()
        form = cart_form() 
        format = bid_form() 
        message ="pls login to place a bid"
        return render(request, 'pharma/item.html', context={"item": option, "form": form, 'display': 'block', 'message': message, 'format':format})
    else:
        
      return HttpResponse("Bid not placed")

@csrf_exempt
def submit_search(request):
    if request.method == "POST":
        user = request.user
        search = request.POST.get('search')
        result = Pharma.objects.filter(name__icontains=search, Approval=True)
        if user.is_authenticated:
            search_product = searchProduct.objects.create(search=search, user=request.user)
            return render(request, 'pharma/product.html', {'popular_items': result})
        else:
            return render(request, 'pharma/product.html', {'popular_items': result})



def help(request):
    if request.method == 'POST':
        form = help_form(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
            name.user = request.user
            email = request.POST.get('email')
            username = request.POST.get('name')
            subject = "PharmaDeals Help Request"
            subject2 = f"PharmaDeals Help Request by {name}"
            message = send_email(request, messages='', subjects=subject, emails=email, html='email/help.html', context={'name': name})
            owner = send_email(request, messages='', subjects=subject2, emails='daropaleb@gmail.com', html='email/help.html', context={'name': name})
            name.save()
            messages= f"Your message has been sent successfully"
            
            return render(request, 'pharma/register.html', context={'message': messages, 'none': 'none', 'text':messages, 'success': "Your message has been sent successfully"})
    else:
        form = help_form()
    return render(request, 'pharma/register.html', context={'form': form, 'none': 'none', 'text': 'How can we help you?'})

# purchase function to get all the items bought by the user
# and display them in a table
def purchase(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            name = request.user
            items = boughtitem.objects.filter(buyer_info__user=name)
            bid_items = bid.objects.filter(user=name)
            cart_data = []
            for item in items:
                product= Pharma.objects.filter(name=item.product_name).first()
                if product:
                    cart_data.append({
                        'name': product.name,
                        'quantity': item.quantity,
                        'price': item.total_earned,
                        'image_url': product.image.url,
                        'total': item.total_earned * item.quantity,
                        'status': item.status,
                        'date': item.created_at,
                        'order_id': item.order_id,
                        
                    })
               
            return render(request, 'tables/purchase_table.html', {'cart_items': cart_data, 'Bid_items': bid_items})
        else:
            return redirect('login')
    else:
        return JsonResponse({"error": "invalid request"}, status=400)


def pharma_delete(request, id):
    
        if request.user.is_authenticated:
            pharma_item = get_object_or_404(Pharma, id=id)
            if pharma_item.user != request.user:
                return HttpResponse("You are not authorized to delete this item.")
            else:
                
                 messages= f"{pharma_item.name} has been deleted successfully"
                 pharma_item.delete()
                 return render(request, 'pharma/profile.html', context={'message': messages, 'display': 'block'})
        else:
            return redirect('login')
   


def product(request, categor):
    options = Categories.objects.filter(category=categor).first()
    option = Pharma.objects.filter(categor=options, Approval=True)[:10]
    return render(request, 'pharma/product.html', context={"popular_items": option})

def category(request):
    option = Categories.objects.all()
    return render(request, 'pharma/category.html', context={'categories':option})

def buynow(request, name , id):
     
        if request.user.is_authenticated:
            cart.objects.create(user=request.user, name=Pharma.objects.get(name=name, id=id), quantity=1)
            
            return redirect('see_cart')
        else:
              option = Pharma.objects.filter(name=name, id=id).first()
              form = cart_form() 
              messages= f"pls login to add item to cart"
              return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages, 'display': 'block'})


def item(request,name, id):
    option = Pharma.objects.filter(name=name, id=id).first()
    popular_item, created = popular.objects.get_or_create(name=option, defaults={'views': 1})
    if not created:
        popular_item.views += 1
        popular_item.save()
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
                format = bid_form() 
                return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages, 'display': 'block', 'format':format})
        else:
              format = bid_form()
              messages= f"pls login to add item to cart"
              return render(request, 'pharma/item.html', context={"item": option, "form": form, 'message': messages, 'display': 'block', 'format':format})
    else:
        form = cart_form() 
    format = bid_form() 
    message ="you can add item to cart"
    return render(request, 'pharma/item.html', context={"item": option, "form": form, 'display': 'none', 'message': message, 'format':format})

def profile(request):
  if request.user.is_authenticated:
    return render(request, 'pharma/profile.html', context={'display': 'none'})
  else:
    return redirect('login')

# Create your views here.
def index(request):
    cate = Categories.objects.all()[:4]
    #cate = Categories.objects.all().order_by('id')[:4]
    popular_items = popular.objects.filter(name__Approval=True).order_by('-views')[:8]

    return render(request, 'pharma/home.html', context = {
    "categories": cate,
    "popular_items": popular_items,
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
            popular.objects.create(name=product, views=0)
            # Send email to the user after successful product upload
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
def get_user(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            name = request.user
            sales = boughtitem.objects.filter(users=name).count()
            user = User.objects.filter(username=name).first()
            views = sum(item.views for item in popular.objects.filter(name__user=name))
            labels = [p.name.name for p in popular.objects.all() if p.name.user == request.user]
            values = [int(p.views) for p in popular.objects.all() if p.name.user == request.user]
      
                # Create the bar chart
            fig, ax = plt.subplots()
            ax.plot(labels, values, marker='o')
            ax.set_title('Views per Product')
            ax.set_xlabel('Product Name')
            # Save it to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            # Encode to base64
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            tab = saleschart(request)
            return render(request, 'tables/user_table.html', {'user': user, 'sales': sales, 'views': views, 'data': uri, 'tab':tab})
        else:
            return redirect('login')
    else:
        return JsonResponse({"error": "invalid request"}, status=400)
#chart to show sales
def saleschart(request):
            name = request.user
            labels = [p.product_name for p in boughtitem.objects.filter(users=name)]
            values = [int(p.total_earned) for p in boughtitem.objects.filter(users=name)]
            # Create the bar chart
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_title('Total Sales Per Product')
            ax.set_xlabel('Product Name')
            # Save it to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            # Encode to base64
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            return uri

def get_sales(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            name = request.user
            sales = boughtitem.objects.filter(users=name).count()
            sale = boughtitem.objects.filter(users=name).order_by('-id')
            views = sum(item.views for item in popular.objects.filter(name__user=name))
            bids = bid.objects.filter(name__user=name).order_by('-bid_time') # to get the first bid
            bid_count= bid.objects.filter(name__user=name).count()
            total_earned = sum([item.total_earned for item in sale])
            labels = [p.product_name for p in boughtitem.objects.filter(users=name)]
            values = [int(p.total_earned) for p in boughtitem.objects.filter(users=name)]
            # Create the bar chart
            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_title('Total Sales Per Product')
            ax.set_xlabel('Product Name')
            # Save it to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            # Encode to base64
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            return render(request, 'tables/sales_table.html', {'total': sales, 'sales': sale, 'views':views, 'bids':bids, 'bid_count': bid_count, 'total_earned': total_earned, 'data': uri})
        else:
            return redirect('login')
    else:
        return JsonResponse({"error": "invalid request"}, status=400)

def get_table(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            name = request.user
            pharma = popular.objects.filter(name__user=name)
            return render(request, 'tables/table.html', {'categories': pharma})
        else:
            return redirect('login')
    else:
        return JsonResponse({"error": "invalid request"}, status=400)

def get_pharma(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            name = request.user
            pharma = cart.objects.filter(user=name).count()
            return render(request, 'pharma/cart.html', {'pharma': pharma})
        else:
            return render(request, 'pharma/cart.html', {'pharma': 0})
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
                
                if method == "2" or method == "1":
                    message = send_email(request, messages="", subjects="order is being processed", emails=email, html='email/process.html',  context={'name': name2} )
                    text = "Your order is being processed, please wait for a confirmation email. Thank you for your order."
                    
                    cart_items = cart.objects.filter(user=name.user)
                    for item in cart_items:   
                        email = item.name.user.email
                        users = item.name.user.username
                        name2 = item.name.user.first_name
                        product_name = item.name.name
                        quantity = item.quantity
                        total_earned = item.name.price * item.quantity
                        order_id = item.id
                        status = "pending"
                        
                        buyer_info = buyerinfo.objects.filter(user=name.user).order_by('-id').first()
                        bought_item = boughtitem.objects.create(email=email, name=name2, users=users, product_name=product_name, quantity=quantity, total_earned=total_earned, order_id=order_id, buyer_info=buyer_info, status=status)
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


