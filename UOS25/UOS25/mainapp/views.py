from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db import connection
from mainapp.models import *
from mainapp.query import *
from mainapp.sqls import SQLs
from mainapp.forms import *
from hashlib import sha256


def login_check_central(func):
    '''
    본사 로그인 체크 데코레이터, @login_check_central로 사용
    '''
    def checker(request,*args,**kwargs):
        sess = request.session
        if 'id' in sess and 'store_id' in sess:
            if sess['store_id'] != None: # 가맹점 아이디일 경우
                return redirect('index')
        else: # 현재 세션에 로그인 정보가 없을 경우
            return redirect('login')
        request.user_id = sess['id']
        return func(request,*args,**kwargs)
    return checker
        
def login_check_store(func):
    '''
    지점 로그인 체크 데코레이터, @login_check_login로 사용
    '''
    def checker(request,*args,**kwargs):
        sess = request.session
        if 'id' in sess and 'store_id' in sess:
            if sess['store_id'] == None: # 본점 아이디일 경우
                return redirect('indexAdmin')
        else: # 현재 세션에 로그인 정보가 없을 경우
            return redirect('login')
        request.user_id = sess['id']
        return func(request,*args,**kwargs)
    return checker
    
def login(request):
    if request.method=='POST':
        sess = request.session
        post = request.POST
        # 로그아웃 요청 처리
        if 'logout' in post.keys():
            if 'id' in sess.keys():
                del sess['id']
            if 'store_id' in sess.keys():
                del sess['store_id']
            return redirect('login')
        # 로그인 요청 처리
        try:
            if not 'user_id' in post.keys() or not 'password' in post.keys():
                raise Exception('un proper login post')
            id, password = post['user_id'], post['password']
            user_object : User = query_pk(User, id, 'user_id')
            if user_object is None:
                raise Exception('no user')
            if sha256(password.encode()).hexdigest() != user_object.password:
                raise Exception("doesn't match password")
            sess['id'] = user_object.id
            sess['store_id'] = user_object.store_id
        except Exception as e:
            print(e)
            return redirect('login')
        # 로그인 성공 후 적절한 페이지로 연결
        if user_object.store_id == None:
            return redirect('indexAdmin')
        else:
            return redirect('index')
    else:
        #로그인 페이지 처리
        return render(request, 'login.html')

# 패스워드 처리 확인을 위한 코드!!
def _join(id,pwd,store_id):
    from hashlib import sha256
    pwd = sha256(pwd.encode()).hexdigest()
    return id, pwd, store_id
    
    
def indexAdmin(request):
    return render(request, 'indexAdmin.html')

def index(request):
    return render(request, 'index.html')

# 본사 페이지

# 지점 관리
@login_check_central
def franchiseManage(request):
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAIN_APP_STORE').fetchone()
    cnt = int(cnt[0])
    
    page = int(request.GET.get('page', 1))
    pages = [i for i in range(max(1, page-2), max(5, page+2)+1)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = StoreRegisterForm(request.POST)
            elif process == 'update' :
                instance = Store.objects.get(id=request.POST.get('id', 'Error')) # 해당 store_id가 있는지 확인
                form = StoreUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id'] #register의 경우 DB 트리거로 자동 지정
                address = form.cleaned_data['address']
                contact = form.cleaned_data['contact']
                store_pay = form.cleaned_data['store_pay']
                store_code = form.cleaned_data['store_code']

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_storeRegister, ['', address, contact, store_pay, store_code])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_storeUpdate, [address, contact, store_pay, store_code, id])
                
                return HttpResponseRedirect('/central/franchiseManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeDelete, [id])
            return HttpResponseRedirect('/central/franchiseManage?page=%s' % page)

        elif process == 'search':
            form = StoreSearchForm(request.POST)
            if form.is_valid():
                address = "%" + form.cleaned_data['address'] + "%"
                contact = "%" + form.cleaned_data['contact'] + "%"
                store_pay_min = 0 if form.cleaned_data['store_pay_min'] is None else float(form.cleaned_data['store_pay_min'])
                store_pay_max = 1 if form.cleaned_data['store_pay_max'] is None else float(form.cleaned_data['store_pay_max'])
                stores = Store.objects.raw(SQLs.sql_storeSearch, [address, contact, store_pay_min, store_pay_max])

    else:
        stores = Store.objects.raw(SQLs.sql_franchiseManage)
        stores = stores[(10*(page-1)):10*page]

    store_register_form = StoreRegisterForm()
    store_update_form = StoreUpdateForm()
    store_search_form = StoreSearchForm()
    return render(request, 'franchiseManage.html', \
        {'stores' : stores, 'storeRegisterForm' : store_register_form, 'storeUpdateForm' : store_update_form, \
            'storeSearchForm' : store_search_form, 'this_page' : page, 'pages' : pages})

def franchiseCostManage(request):
    context=dict(
        
    )
    return render(request, 'franchiseCostManage.html', context)

# 납품 업체 관리
def supplierManage(request):
    page = int(request.GET.get('page', 1))
    pages = [i for i in range(max(1, page-2), max(5, page+2)+1)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = SupplierRegisterForm(request.POST)
            elif process == 'update' :
                instance = Supplier.objects.get(id=request.POST.get('id', 'Error')) # 해당 id가 있는지 확인
                form = SupplierUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id']
                name = form.cleaned_data['name']
                contact = form.cleaned_data['contact']
                email = form.cleaned_data['email']

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_supplierRegister, ['', name, contact, email])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_supplierUpdate, [name, contact, email, id])
                
                return HttpResponseRedirect('/central/supplierManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_supplierDelete, [id])
            return HttpResponseRedirect('/central/supplierManage?page=%s' % page)

        elif process == 'search':
            form = SupplierSearchForm(request.POST)
            if form.is_valid():
                name = "%" + form.cleaned_data['name'] + "%"
                contact = "%" + form.cleaned_data['contact'] + "%"
                email = "%" + form.cleaned_data['email'] + "%"
                suppliers = Supplier.objects.raw(SQLs.sql_supplierSearch, [name, contact, email])

    else:
        suppliers = Supplier.objects.raw(SQLs.sql_supplierManage)
        suppliers = suppliers[(10*(page-1)):10*page]

    supplier_register_form = SupplierRegisterForm()
    supplier_update_form = SupplierUpdateForm()
    supplier_search_form = SupplierSearchForm()
    return render(request, 'supplierManage.html', \
        {'suppliers' : suppliers, 'supplierRegisterForm' : supplier_register_form, 'supplierUpdateForm' : supplier_update_form, \
            'supplierSearchForm' : supplier_search_form, 'this_page' : page, 'pages' : pages})

def storeOrderManage(request):
    return render(request, 'storeOrderManage.html')

# 상품 등록
def registerProduct(request):

    return render(request, 'registerProduct.html',{'form':ProductRegisterForm()})

def productManage(request):
    context = dict(
        products=query_all(Product),
    )
    return render(request, 'HeadProductManage.html', context)

# 고객 관리
def customerManage(request):
    page = int(request.GET.get('page', 1))
    pages = [i for i in range(max(1, page-2), max(5, page+2)+1)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = CustomerRegisterForm(request.POST)
            elif process == 'update' :
                instance = Customer.objects.get(id=request.POST.get('id', 'Error')) # 해당 id가 있는지 확인
                form = CustomerUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id']
                name = form.cleaned_data['name']
                mileage = form.cleaned_data['mileage']
                gender = form.cleaned_data['gender']
                birthday = form.cleaned_data['birthday']
                contact = form.cleaned_data['contact']

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_customerRegister, ['', name, mileage, gender, birthday, contact])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_customerUpdate, [name, mileage, gender, birthday, contact, id])
                
                return HttpResponseRedirect('/central/customerManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_customerDelete, [id])
            return HttpResponseRedirect('/central/customerManage?page=%s' % page)

        elif process == 'search':
            form = CustomerSearchForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                name = "%" + form.cleaned_data['name'] + "%"
                mileage_min = 0 if form.cleaned_data['mileage_min'] is None else int(form.cleaned_data['mileage_min'])
                mileage_max = 99999999 if form.cleaned_data['mileage_max'] is None else int(form.cleaned_data['mileage_max'])
                gender = 1 if form.cleaned_data['gender'] is None else form.cleaned_data['gender']
                birthday_min = '1970-01-01' if form.cleaned_data['birthday_min'] is None else str(form.cleaned_data['birthday_min'])
                birthday_max = '2100-12-12' if form.cleaned_data['birthday_max'] is None else str(form.cleaned_data['birthday_max'])
                contact = "%" + form.cleaned_data['contact'] + "%"
                print([name, mileage_min, mileage_max, gender, birthday_min, birthday_max, contact])
                customers = Customer.objects.raw(SQLs.sql_customerSearch,\
                    [name, mileage_min, mileage_max, gender, birthday_min, birthday_max, contact])

    else:
        customers = Customer.objects.raw(SQLs.sql_customerManage)
        customers = customers[(10*(page-1)):10*page]

    customer_register_form = CustomerRegisterForm()
    customer_update_form = CustomerUpdateForm()
    customer_search_form = CustomerSearchForm()
    return render(request, 'customerManage.html', \
        {'customers' : customers, 'customerRegisterForm' : customer_register_form, 'customerUpdateForm' : customer_update_form, \
            'customerSearchForm' : customer_search_form, 'this_page' : page, 'pages' : pages})

# 가맹점 페이지
def orderManage(request):
    return render(request, 'orderManage.html')

@login_check_store
def centralRefundManage(request):
    return render(request, 'centralRefundManage.html')

def saleProduct(request):
    return render(request, 'saleProduct.html')

def customerRefundManage(request):
    return render(request, 'customerRefundManage.html')

# 재고 등록
def registerStock(request):
    return render(request, 'registerStock.html')

def deleteStock(request):
    return render(request, 'deleteStock.html')

def expireDateManage(request):
    return render(request, 'expiryDateManage.html')

def saleManage(request):
    return render(request, 'saleManage.html')

def maintenanceCostManage(request):
    return render(request, 'maintenanceCostManage.html')

def employeeManage(request):
    return render(request, 'employeeManage.html')

def workListManage(request):
    return render(request, 'workListManage.html')

def salaryManage(request):
    return render(request, 'salaryManage.html')