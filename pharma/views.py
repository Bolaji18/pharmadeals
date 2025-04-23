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



create_message= """
  Hi,

Welcome to Pharmadeals.ng – we're thrilled to have you on board!

You've just joined Nigeria’s leading online marketplace for pharmaceutical products, where quality meets affordability. Whether you’re a pharmacy owner, a healthcare professional, or just someone looking for trusted medical supplies, you’re in the right place.

Here’s what you can expect: ✅ Access to top-quality pharmaceutical products
✅ Verified and trusted suppliers
✅ Competitive prices and amazing deals
✅ Seamless ordering and delivery experience

Your account is now active, and you're just a click away from exploring everything Pharmadeals has to offer.

👉 Start Shopping Now

If you have any questions or need help getting started, our support team is always here for you. Just hit reply or contact us at admin@pharmadeals.ng.

Thank you for joining the Pharmadeals family – let’s make healthcare more accessible, together.

Warm regards,
The Pharmadeals.ng Team
www.pharmadeals.ng
Your trusted partner in healthcare.



"""

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
           message = send_email(request, messages=create_message, subjects="Welcome to PharmaDeals", emails=email)
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
            new_product = f"""
             Hi {request.user.username},

            Great news — your product has been successfully uploaded and is now live on Pharmadeals.ng! 🎉

            We're excited to have your product listed and available to thousands of potential buyers across Nigeria who trust Pharmadeals for their pharmaceutical needs.

            Here’s what happens next:

            Your product will be reviewed for quality and compliance (if needed).

            Customers can now view, search, and purchase your product.

            You’ll receive notifications on any orders or customer inquiries.

            Want to increase visibility? Here are a few tips: 🔹 Make sure your product description is clear and complete
            🔹 Use high-quality images
            🔹 Set competitive pricing
            🔹 Respond quickly to inquiries

            👉 View Your Product
            👉 Add More Products

            If you need assistance or have any questions, we’re just an email away at admin@pharmadeals.ng.

            Thanks for choosing Pharmadeals.ng — we’re excited to grow with you!

            Warm regards,
            The Pharmadeals.ng Team
            Empowering pharmacies, one deal at a time.
            """
            email = request.user.email
            message = send_email(request, messages=new_product, subjects="product added successfully", emails=email)
            success= "Your product has been uploaded"
            return render(request, 'pharma/register.html', {'success': success, 'none':'none'})
    else:
        form = pharma_form()
    return render(request, 'pharma/register.html', {'form': form, 'text':text})


def send_email(request, messages,subjects, emails ):
    email = emails
    subject = subjects
    message = messages
    from_email = 'admin@pharmadeals.ng'
    html_message = render(request, 'pharma/email.html', {"message": message}).content.decode('utf-8')
    send_mail(subject, message, from_email, [email], html_message=html_message)
    f = open('email.txt', 'a')
    f.write(f'email sent to {email} \n')
    f.close()
    return f'email sent to {email}'

