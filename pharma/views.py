from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
def index(request):
    return render(request, 'pharma/index.html')
