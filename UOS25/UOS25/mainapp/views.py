from django.shortcuts import render
from mainapp.models import *
from mainapp.query import *
from django.core.handlers.wsgi import WSGIHandler

# request type : django.core.handlers.wsgi.WSGIRequest
# Create your views here.

'''def login(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UserForm()
    return render(request, 'index.html',{'form':form})'''

def check_central(func):
    '''
    본사 로그인 체크 데코레이터, @check_central로 사용
    '''
    def checker(request : WSGIHandler ,*args,**kwargs):
        pass
    
def login(request):
    return render(request, 'login.html')

def indexAdmin(request):
    return render(request, 'indexAdmin.html')

def index(request):
    return render(request, 'index.html')

# 본사 페이지
def franchiseManage(request):
    context=dict(
        stores = query_all(Store)
    )
    return render(request, 'franchiseManage.html', context)

def franchiseCostManage(request):
    context=dict(
        
    )
    return render(request, 'franchiseCostManage.html', context)

def deliveryManage(request):
    return render(request, 'deliveryManage.html')

def franchiseOrderManage(request):
    return render(request, 'franchiseOrderManage.html')

def registerHeadProduct(request):
    return render(request, 'registerHeadProduct.html')

def HeadProductManage(request):
    context = dict(
        products=query_all(Product),
    )
    return render(request, 'HeadProductManage.html', context)

def registerCustomer(request):
    return render(request, 'registerCustomer.html')

def customerManage(request):
    return render(request, 'customerManage.html')


# 가맹점 페이지
def orderHeadManage(request):
    return render(request, 'orderHeadManage.html')

def refundHeadManage(request):
    return render(request, 'refundHeadManage.html')

def saleProduct(request):
    return render(request, 'saleProduct.html')

def refundCustomerManage(request):
    return render(request, 'refundCustomerManage.html')
    
def registerProduct(request):
    return render(request, 'registerProduct.html')

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