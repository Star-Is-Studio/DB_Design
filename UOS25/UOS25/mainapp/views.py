from django.shortcuts import render, redirect
from mainapp.models import *
from mainapp.query import *
from hashlib import sha256
from mainapp.sqls import SQLs
from mainapp.forms import *


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
    def checker(request,*args,**kwargs):
        sess = request.session
        if sess['_auth_user_id'] != '1':
            return redirect('login')
        return func(request,*args,**kwargs)
    return checker
        
def login(request):
    if request.method=='POST':
        try:
            post = request.POST
            if not 'id' in post.keys() or not 'password' in post.keys():
                raise Exception('un proper login post')
            id, password = post['id'], post['password']
            user_object : User = query_pk(User,int(id), 'userId')
            if user_object is None:
                raise Exception('no user')
            if sha256(password.encode()) != user_object.password:
                raise Exception("doesn't match password")
            request.session['id'] = user_object.id
        except Exception as e:
            print(e)
            return redirect('login')
    return render(request, 'login.html')

def indexAdmin(request):
    return render(request, 'indexAdmin.html')

def index(request):
    return render(request, 'index.html')

# 본사 페이지
def franchiseManage(request):
    if request.method == 'POST':
        process = request.POST.get('process', False)
        
        if process == 'register':
            form = StoreRegisterForm(request.POST)
            if form.is_valid():
                store_id = form.cleaned_data['store_id']
                address = form.cleaned_data['address']
                contact = form.cleaned_data['contact']
                store_pay = form.cleaned_data['store_pay']
                store_code = form.cleaned_data['store_code']

                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_storeRegister, [store_id, address, contact, store_pay, store_code])

        elif process == 'delete':
            store_id = int(request.POST.get('store_id', 'Error'))

            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeDelete, [store_id])

        elif process == 'update':
            store_id = int(request.POST.get('store_id', 'Error'))
            address = request.POST.get('address', False)
            contact = request.POST.get('contact', False)
            store_pay = float(request.POST.get('store_pay', 'Error'))
            store_code = int(request.POST.get('store_code', 'Error'))

            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeUpdate, [address, contact, store_pay, store_code, store_id])

        return HttpResponseRedirect('/central/franchiseManage')

    stores = Store.objects.raw(SQLs.sql_franchiseManage)
    store_register_form = StoreRegisterForm()
    return render(request, 'franchiseManage.html', {'stores' : stores, 'storeRegisterForm' : store_register_form})


def franchiseCostManage(request):
    context=dict(
        
    )
    return render(request, 'franchiseCostManage.html', context)

@check_central
def supplierManage(request):
    return render(request, 'deliveryManage.html')

def storeOrderManage(request):
    return render(request, 'franchiseOrderManage.html')

def registerProduct(request):
    return render(request, 'registerHeadProduct.html')

def productManage(request):
    context = dict(
        products=query_all(Product),
    )
    return render(request, 'HeadProductManage.html', context)

def registerCustomer(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            customer_id = form.cleaned_data['customer_id']
            name = form.cleaned_data['name']
            mileage = form.cleaned_data['mileage']
            gender = form.cleaned_data['gender']
            birthday = form.cleaned_data['birthday']
            contact = form.cleaned_data['contact']

            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_CustomerRegister, [customer_id, name, mileage, gender, birthday, contact])

            return HttpResponseRedirect('/central/customerManage')

    else:
        form = CustomerRegisterForm()
    return render(request, 'registerCustomer.html', {'form' : form})

def customerManage(request):
    # 단순한 삭제 메커니즘. 수정 필요.
    delete_id = request.GET.get('delete_id', False)
    if delete_id:
        with connection.cursor() as cursor:
            cursor.execute(SQLs.sql_CustomerDelete, [delete_id])
    
    customer_list = Customer.objects.raw(SQLs.sql_CustomerManage) # IDE에서 objects 없다고 에러뜨면 무시
    return render(request, 'customerManage.html', {'customer_list' : customer_list})


# 가맹점 페이지
def orderManage(request):
    return render(request, 'orderHeadManage.html')

def centralRefundManage(request):
    return render(request, 'refundHeadManage.html')

def saleProduct(request):
    return render(request, 'saleProduct.html')

def customerRefundManage(request):
    return render(request, 'refundCustomerManage.html')
    
def registerStock(request):
    return render(request, 'registerProduct.html')

def deleteStock(request):
    return render(request, 'deleteProduct.html')

def expireDateManage(request):
    return render(request, 'expiryDateManage.html')

def saleManage(request):
    return render(request, 'saleManage.html')

def maintenanceCostManage(request):
    return render(request, 'costManage.html')

def employeeManage(request):
    return render(request, 'employeeManage.html')

def workListManage(request):
    return render(request, 'workRecordManage.html')

def salaryManage(request):
    return render(request, 'salaryManage.html')