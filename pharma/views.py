from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm
# Create your views here.
def index(request):
    return render(request, 'pharma/index.html')


def login(request):
    form = NewUserForm()
    return render(request, 'pharma/login.html',  context={"form":form})
