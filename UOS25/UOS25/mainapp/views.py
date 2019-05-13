from django.shortcuts import render
from mainapp.forms import *

# Create your views here.

'''def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'index.html',{'form':form})'''
def login(request):
    return render(request, 'login.html')

def indexAdmin(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'indexAdmin.html',{'form':form})

def index(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'index.html',{'form':form})

def registerProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProductForm()
    return render(request, 'registerProduct.html', {'form':form})

def deleteProduct(request):
    return render(request, 'deleteProduct.html')

def dashBoard(request):
    return render(request, 'dashBoard.html')

def adminPage(request):
    return render(request, 'adminPage.html')

def employeeManage(request):
    return render(request, 'employeeManage.html')

def orderHead(request):
    return render(request, 'orderHead.html')
    