from django.shortcuts import render
from mainapp.forms import *
from mainapp.models import *

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
##가맹점페이지
def orderHeadManage(request):
    return render(request, 'orderHeadManage.html')

def refundHeadManage(request):
    return render(request, 'refundHeadManage.html')

def saleProduct(request):
    return render(request, 'saleProduct.html')

def refundCustomerManage(request):
    return render(request, 'refundCustomerManage.html')
    
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

def expiryDateManage(request):
    return render(request, 'expiryDateManage.html')

def saleManage(request):
    return render(request, 'saleManage.html')

def costManage(request):
    return render(request, 'costManage.html')

def employeeManage(request):
    return render(request, 'employeeManage.html')

def workRecordManage(request):
    return render(request, 'workRecordManage.html')

def salaryManage(request):
    return render(request, 'salaryManage.html')
##본사페이지
def franchiseManage(request):
    context=dict(
        stores = [ elem for elem in Store.objects.raw('select * from mainapp_store')]
    )
    return render(request, 'franchiseManage.html', context)

def franchiseCostManage(request):
    return render(request, 'franchiseCostManage.html')

def deliveryManage(request):
    return render(request, 'deliveryManage.html')

def franchiseOrderManage(request):
    return render(request, 'franchiseOrderManage.html')

def registerHeadProduct(request):
    return render(request, 'registerHeadProduct.html')

def HeadProductManage(request):
    return render(request, 'HeadProductManage.html')

def registerCustomer(request):
    return render(request, 'registerCustomer.html')

def customerManage(request):
    return render(request, 'customerManage.html')