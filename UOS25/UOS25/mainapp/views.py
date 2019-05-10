from django.shortcuts import render
from mainapp.forms import *

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'index.html',{'form':form})
    
def index(request):
    return render(request, 'index.html')
    
def registerProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()
    return render(request, 'registerProduct.html', {'form':form})

def dashBoard(request):
    return render(request, 'dashBoard.html')

def adminPage(request):
    return render(request, 'adminPage.html')
    