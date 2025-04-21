from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm
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


           user = form.save()
           return redirect('login')
       else:
            # Form is not valid, errors will be passed to the template
            return render(request, 'pharma/register.html', {'form': form})


    form= NewUserForm()
    life= "Create"
    return render(request=request, template_name="pharma/register.html", context={"form":form, 'life':life})

