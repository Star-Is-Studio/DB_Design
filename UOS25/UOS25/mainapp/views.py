from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from mainapp.models import *
from mainapp.query import *
from mainapp.sqls import SQLs
from mainapp.forms import *
from hashlib import sha256
import datetime, imghdr

# 파일 업로드 핸들러 : 상품 사진 업로드용
def handle_uploaded_file(f, fpath):
    with open('product_pic/' + str(fpath), 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

def productPicture(request, *args, **kwargs):
    with open('product_pic/' + str(kwargs['pic_number']), 'rb') as f:
        img_type = str(imghdr.what(f))
        return HttpResponse(f.read(), content_type="image/"+img_type)

def alertBack(msg):
    return "<script>alert('데이터베이스 에러  :  " + msg + " '); window.history.back();</script>"

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
        request.store_id = sess['store_id']
        request.emp_pos = sess['emp_pos']
        return func(request,*args,**kwargs)
    return checker
    
def login(request):
    sess = request.session
    if request.method=='POST':
        post = request.POST
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
            sess['id'] = id
            sess['store_id'] = user_object.store_id.id if not user_object.store_id is None else None
            sess['emp_pos'] = user_object.emp_pos_code

        except Exception as e:
            print(e)
            return redirect('login')
        # 로그인 성공 후 적절한 페이지로 연결
        if user_object.store_id == None:
            return redirect('indexAdmin')
        else:
            return redirect('index')
    else:
        get = request.GET
        # 로그아웃 요청 처리
        if 'logout' in get.keys():
            if 'id' in sess.keys():
                del sess['id']
            if 'store_id' in sess.keys():
                del sess['store_id']
            return redirect('login')
        #로그인 페이지 처리
        return render(request, 'login.html')

# 패스워드 처리 확인을 위한 코드!!
def hash_pwd(pwd):
    from hashlib import sha256
    pwd = sha256(pwd.encode()).hexdigest()
    return pwd
    
@login_check_central
def indexAdmin(request):
    return render(request, 'indexAdmin.html')
@login_check_store
def index(request):
    return render(request, 'index.html')


# 본사 페이지

# 지점 관리
@login_check_central
def franchiseManage(request):
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]

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
                        # 지점장 생성 로직
                        user_id, password = '{}m'.format(id), hash_pwd('hoho')
                        cursor.execute(SQLs.sql_userRegister, [user_id, password, id, 0])

                        # 점원 생성 로직
                        user_id, password = '{}e'.format(id), hash_pwd('hoho')
                        cursor.execute(SQLs.sql_userRegister, [user_id, password, id, 1])
                        
                    elif process == 'update':
                        cursor.execute(SQLs.sql_storeUpdate, [address, contact, store_pay, store_code, id])
                
                return HttpResponseRedirect(reverse('franchiseManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeDelete, [id])
            return HttpResponseRedirect(reverse('franchiseManage')+'?page=%s' % page)

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

# 가맹요급 수납
@login_check_central
def franchiseCostManage(request):

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_FRANCHISE_STORE_RCPT').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = FranchiseStoreRcptRegisterForm(request.POST)
            elif process == 'update' :
                instance = Franchise_store_rcpt.objects.get(id=request.POST.get('id', 'Error')) # 해당 id가 있는지 확인
                form = FranchiseStoreRcptUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id']

                store_id = form.cleaned_data['store_id'].id
                rcpt_date = form.cleaned_data['rcpt_date']
                rcpt_amount = form.cleaned_data['rcpt_amount']
                
                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_franchiseStoreRcptRegister, [store_id, rcpt_date, rcpt_amount])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_franchiseStoreRcptUpdate, [rcpt_date, rcpt_amount, store_id, id])
                
                return HttpResponseRedirect('/central/franchiseCostManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_franchiseStoreRcptDelete, [id])
            return HttpResponseRedirect('/central/franchiseCostManage?page=%s' % page)

    else:
        franchiseStoreRcpts = Franchise_store_rcpt.objects.raw(SQLs.sql_franchiseStoreRcptManage)
        franchiseStoreRcpts = franchiseStoreRcpts[(10*(page-1)):10*page]

    franchise_store_rcpt_register_form = FranchiseStoreRcptRegisterForm()
    franchise_store_rcpt_update_form = FranchiseStoreRcptUpdateForm()

    return render(request, 'franchiseCostManage.html', \
        {'franchise_store_rcpts' : franchiseStoreRcpts, 'franchiseStoreRcptRegisterForm' : franchise_store_rcpt_register_form, 'franchiseStoreRcptUpdateForm' : franchise_store_rcpt_update_form, \
            'this_page' : page, 'pages' : pages})

# 납품 업체 관리
@login_check_central
def supplierManage(request):
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
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
                
                return HttpResponseRedirect(reverse('supplierManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_supplierDelete, [id])
            return HttpResponseRedirect(reverse('supplierManage')+'?page=%s' % page)

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

# 지점 주문 관리
@login_check_central
def storeOrderManage(request):
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_ORDER').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]

    if request.method=='POST':
        process = str(request.GET.get('process', False))
        if process=='update':
            instance = Order.objects.get(id=request.POST.get('id','Error'))
            form = StoreOrderUpdateForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                store_id = form.cleaned_data['store_id'].id
                order_timestamp = form.cleaned_data['order_timestamp']
                complete_timestamp = form.cleaned_data['complete_timestamp']
                process_code = form.cleaned_data['process_code']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_storeOrderUpdate, [store_id, order_timestamp, complete_timestamp, process_code, id])
                
    orders = Order.objects.raw(SQLs.sql_storeOrderManage)
    orders = orders[(10*(page-1)):10*page]
    
    store_order_update_form = StoreOrderUpdateForm()
    return render(request, 'storeOrderManage.html', {'orders':orders, 'this_page':page, 'pages':pages,
        'storeOrderUpdateForm':store_order_update_form})

# 지점 주문내역 조회
@login_check_central
def storeOrderManageList(request):
    order_id = int(request.GET.get('order_id','Error'))
    
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_ORDER').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]


    if request.method=='POST':
        process = str(request.GET.get('process', False))
        if process=='update':
            print(request.POST)
            form = StoreOrderManageListUpdateForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                sent_timestamp =  form.cleaned_data['sent_timestamp']
                arrival_timestamp = form.cleaned_data['arrival_timestamp']
                process_code = form.cleaned_data['process_code']

                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_storeOrderListUpdate, [sent_timestamp, arrival_timestamp, process_code, id])
            else:
                print("non valid")
                print(form.errors)

    orders = Order_list.objects.raw(SQLs.sql_storeOrderListManage, [order_id])
    orders = orders[(10*(page-1)):10*page]
    for order in orders:
        order.subtotal = order.quantity * order.barcode.unit_price
    
    store_order_manage_list_update_form = StoreOrderManageListUpdateForm()
    return render(request, 'storeOrderManageList.html', {'order_id':order_id,'orders':orders, 'this_page':page, 'pages':pages,
        'storeOrderManageListUpdateForm':StoreOrderManageListUpdateForm,})

# 지점 반품 관리
@login_check_central
def storeRefundManage(request):
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE_REFUND').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]

    if request.method=='POST':
        process = str(request.GET.get('process', False))
        if process=='update':
            instance = Order.objects.get(id=request.POST.get('id','Error'))
            form = StoreRefundUpdateForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                store_id = form.cleaned_data['store_id'].id
                barcode = form.cleaned_data['barcode'].barcode
                refund_timestamp = form.cleaned_data['refund_timestamp']
                refund_reason_code = form.cleaned_data['refund_reason_code']
                process_code = form.cleaned_data['process_code']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_centralStoreRefundUpdate, 
                        [store_id, barcode, refund_timestamp, refund_reason_code, process_code, id])
    
    refunds = Store_refund.objects.raw(SQLs.sql_centralStoreRefundManage)
    refunds = refunds[(10*(page-1)):10*page]
    store_refund_update_form = StoreRefundUpdateForm()
    
    return render(request, 'centralStoreRefundManage.html', {'refunds':refunds, 'this_page':page, 'pages':pages,
        'storeRefundUpdateForm':store_refund_update_form})



# 상품 관리
@login_check_central
def productManage(request):

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(barcode) from MAINAPP_PRODUCT').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = ProductRegisterForm(request.POST, request.FILES)
            elif process == 'update' :
                instance = Product.objects.get(barcode=request.POST.get('barcode', 'Error')) # 해당 id가 있는지 확인
                form = ProductUpdateForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                barcode = form.cleaned_data['barcode']
                name = form.cleaned_data['name']
                supply_price = form.cleaned_data['supply_price']
                unit_price = form.cleaned_data['unit_price']
                supplier_id = form.cleaned_data['supplier_id'].id
                category_a = form.cleaned_data['category_a']
                category_b = form.cleaned_data['category_b']
                explain = form.cleaned_data['explain']

                print(request.FILES)
                # 사진 파일 처리
                if request.FILES.get('picture_file', False):
                    if imghdr.what(request.FILES['picture_file']): # 이미지 파일이 맞다면
                        print('이미지 파일 감지')
                        handle_uploaded_file(request.FILES['picture_file'], barcode)
                        picture_file_path = barcode
                else:
                    if process == 'register':
                        picture_file_path = None
                    elif process == 'update':
                        try:
                            picture_file_path = Product.objects.get(pk=barcode).picture_file_path
                        except Product.DoesNotExist:
                            raise Http404("Picture File Check Error")

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_productRegister, [barcode, name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_productUpdate, [name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path, barcode])
                
                return HttpResponseRedirect(reverse('productManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')
                return HttpResponse(alertBack('상품정보가 올바른지, 중복 바코드가 존재하는지 확인해주세요.'))

        elif process == 'delete':
            barcode = int(request.POST.get('barcode', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_productDelete, [barcode])
            return HttpResponseRedirect(reverse('productManage')+'?page=%s' % page)

        elif process == 'search':
            form = ProductSearchForm(request.POST)
            if form.is_valid():
                #print(form.cleaned_data)
                barcode = "%%" if form.cleaned_data['barcode'] is None else str(form.cleaned_data['barcode'])
                name = "%" + form.cleaned_data['name'] + "%"
                supply_price_min = 0 if form.cleaned_data['supply_price_min'] is None else form.cleaned_data['supply_price_min']
                supply_price_max = 99999999 if form.cleaned_data['supply_price_max'] is None else form.cleaned_data['supply_price_max']
                unit_price_min = 0 if form.cleaned_data['unit_price_min'] is None else form.cleaned_data['unit_price_min']
                unit_price_max = 99999999 if form.cleaned_data['unit_price_max'] is None else form.cleaned_data['unit_price_max']
                supplier_id = ("%" + str(form.cleaned_data['supplier_id'].id) + "%") if form.cleaned_data['supplier_id'] != None else "%%"
                category_a = "%%" if form.cleaned_data['category_a'] is None else str(form.cleaned_data['category_a'])
                category_b = "%%" if form.cleaned_data['category_b'] is None else str(form.cleaned_data['category_b'])

                ##print([barcode, name, supply_price_min, supply_price_max, unit_price_min, \
                #    unit_price_max, supplier_id, category_a, category_b])

                products = Product.objects.raw(SQLs.sql_productSearch, \
                    [barcode, name, supply_price_min, supply_price_max, unit_price_min, \
                    unit_price_max, supplier_id, category_a, category_b])

    else:
        products = Product.objects.raw(SQLs.sql_productManage)
        products = products[(10*(page-1)):10*page]

    product_register_form = ProductRegisterForm()
    product_update_form = ProductUpdateForm()
    product_search_form = ProductSearchForm()
    return render(request, 'productManage.html', \
        {'products' : products, 'productRegisterForm' : product_register_form, 'productUpdateForm' : product_update_form, \
            'productSearchForm' : product_search_form, 'this_page' : page, 'pages' : pages})

# 고객 관리
@login_check_central
def customerManage(request):
    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
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
                
                return HttpResponseRedirect(reverse('customerManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_customerDelete, [id])
            return HttpResponseRedirect(reverse('customerManage')+'?page=%s' % page)

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

# 상품 조회
@login_check_store
def productManageStore(request):

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(barcode) from MAINAPP_PRODUCT').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = ProductRegisterForm(request.POST, request.FILES)
            elif process == 'update' :
                instance = Product.objects.get(barcode=request.POST.get('barcode', 'Error')) # 해당 id가 있는지 확인
                form = ProductUpdateForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                barcode = form.cleaned_data['barcode']
                name = form.cleaned_data['name']
                supply_price = form.cleaned_data['supply_price']
                unit_price = form.cleaned_data['unit_price']
                supplier_id = form.cleaned_data['supplier_id'].id
                category_a = form.cleaned_data['category_a']
                category_b = form.cleaned_data['category_b']
                explain = form.cleaned_data['explain']

                print(request.FILES)
                # 사진 파일 처리
                if request.FILES.get('picture_file', False):
                    if imghdr.what(request.FILES['picture_file']): # 이미지 파일이 맞다면
                        print('이미지 파일 감지')
                        handle_uploaded_file(request.FILES['picture_file'], barcode)
                        picture_file_path = barcode
                else:
                    if process == 'register':
                        picture_file_path = None
                    elif process == 'update':
                        try:
                            picture_file_path = Product.objects.get(pk=barcode).picture_file_path
                        except Product.DoesNotExist:
                            raise Http404("Picture File Check Error")

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_productRegister, [barcode, name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_productUpdate, [name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path, barcode])
                
                return HttpResponseRedirect(reverse('productManageStore')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            barcode = int(request.POST.get('barcode', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_productDelete, [barcode])
            return HttpResponseRedirect(reverse('productManageStore')+'?page=%s' % page)

        elif process == 'search':
            form = ProductSearchForm(request.POST)
            if form.is_valid():
                #print(form.cleaned_data)
                barcode = "%%" if form.cleaned_data['barcode'] is None else str(form.cleaned_data['barcode'])
                name = "%" + form.cleaned_data['name'] + "%"
                supply_price_min = 0 if form.cleaned_data['supply_price_min'] is None else form.cleaned_data['supply_price_min']
                supply_price_max = 99999999 if form.cleaned_data['supply_price_max'] is None else form.cleaned_data['supply_price_max']
                unit_price_min = 0 if form.cleaned_data['unit_price_min'] is None else form.cleaned_data['unit_price_min']
                unit_price_max = 99999999 if form.cleaned_data['unit_price_max'] is None else form.cleaned_data['unit_price_max']
                supplier_id = ("%" + str(form.cleaned_data['supplier_id'].id) + "%") if form.cleaned_data['supplier_id'] != None else "%%"
                category_a = "%%" if form.cleaned_data['category_a'] is None else str(form.cleaned_data['category_a'])
                category_b = "%%" if form.cleaned_data['category_b'] is None else str(form.cleaned_data['category_b'])

                ##print([barcode, name, supply_price_min, supply_price_max, unit_price_min, \
                #    unit_price_max, supplier_id, category_a, category_b])

                products = Product.objects.raw(SQLs.sql_productSearch, \
                    [barcode, name, supply_price_min, supply_price_max, unit_price_min, \
                    unit_price_max, supplier_id, category_a, category_b])

    else:
        products = Product.objects.raw(SQLs.sql_productManage)
        products = products[(10*(page-1)):10*page]

    product_register_form = ProductRegisterForm()
    product_update_form = ProductUpdateForm()
    product_search_form = ProductSearchForm()
    return render(request, 'productManageStore.html', \
        {'products' : products, 'productRegisterForm' : product_register_form, 'productUpdateForm' : product_update_form, \
            'productSearchForm' : product_search_form, 'this_page' : page, 'pages' : pages})

# 주문 관리
@login_check_store
def orderManage(request):
    store_id = request.session['store_id']
    # orders = []

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_ORDER').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        # f = request.POST.dict()
        # f['order_timestamp'] = f['order_timestamp'].replace("T"," ")
        if process == 'register':
            form = OrderRegisterForm(request.POST)
        
        if form.is_valid():
            order_timestamp = form.cleaned_data['order_timestamp']
            with connection.cursor() as cursor:
                if process == 'register':
                    cursor.execute(SQLs.sql_orderRegister, [store_id, order_timestamp])
            
            return HttpResponseRedirect(reverse('orderManage')+'?page=%s' % page)
        else:
            print(form.errors)
            print('가 발생')

    else:
        orders = Order.objects.raw(SQLs.sql_orderManage, [store_id])
        orders = orders[(10*(page-1)):10*page]

    order_register_form = OrderRegisterForm()

    return render(request, 'orderManage.html', \
        {'orders' : orders, 'orderRegisterForm' : order_register_form, 'this_page' : page, 'pages' : pages})

# 주문 목록 내역
@login_check_store
def orderManageList(request, *args, **kwargs):
    order_id = int(request.GET.get('order_id', 'Error'))
    order = Order.objects.get(id=order_id)

    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
    
        if process == 'register':
            form = OrderListRegisterForm(request.POST)
            if form.is_valid():
                barcode = form.cleaned_data['barcode'].barcode
                quantity = form.cleaned_data['quantity']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_orderListRegister, [barcode, quantity, order_id])
                    
                return HttpResponseRedirect(reverse('orderManageList')+'?order_id=%s&page=%s' % (order_id, page))
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_orderListDelete, [id])
            return HttpResponseRedirect(reverse('orderManageList')+'?order_id=%s&page=%s' % (order_id, page))

    else:
        orderRecords = Order_list.objects.raw(SQLs.sql_orderListManage, [order_id])
        orderRecords = orderRecords[(10*(page-1)):10*page]

    orderList_register_form = OrderListRegisterForm()

    return render(request, 'orderManageList.html', \
        {'orderRecords' : orderRecords, 'orderListRegisterForm' : orderList_register_form, 'order': order, \
        'this_page' : page, 'pages' : pages})

# 본사 반품 관리
@login_check_store
def centralRefundManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(barcode) from MAINAPP_STORE_REFUND').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        # f = request.POST.dict()

        if process == 'register':
            form = StoreRefundRegisterForm(request.POST)
            if form.is_valid():
                barcode = form.cleaned_data['barcode'].barcode
                quantity = form.cleaned_data['quantity']
                refund_timestamp = form.cleaned_data['refund_timestamp']
                refund_reason_code = form.cleaned_data['refund_reason_code']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_storeRefundRegister, [barcode, quantity, refund_timestamp, refund_reason_code, store_id])
                
                return HttpResponseRedirect(reverse('centralRefundManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeRefundDelete, [id])
            return HttpResponseRedirect(reverse('centralRefundManage')+'?page=%s' % page)

    else:
        refunds = Store_refund.objects.raw(SQLs.sql_storeRefundManage, [store_id])
        refunds = refunds[(10*(page-1)):10*page]

    storeRefund_register_form = StoreRefundRegisterForm()

    return render(request, 'centralRefundManage.html', \
        {'refunds' : refunds, 'storeRefundRegisterForm' : storeRefund_register_form, 'this_page' : page, 'pages' : pages})

@login_check_store
def saleProduct(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_RECEIPT').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process == 'register':
            form = ReceiptRegisterForm(request.POST)
        if form.is_valid():
            trade_timestamp = datetime.datetime.now()
            employee_id = form.cleaned_data['employee_id'].id
            customer_id = None if form.cleaned_data['customer_id'] is None else form.cleaned_data['customer_id'].id
            pay_method = form.cleaned_data['payment_method_code']
            pay_info = form.cleaned_data['payment_information']
            
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_receiptRegister, [trade_timestamp, employee_id, customer_id, pay_method, pay_info, store_id])
            
            return HttpResponseRedirect(reverse('saleProduct')+'?page=%s' % page)
        else:
            print(form.errors)
            print('가 발생')

    else:
        receipts = Receipt.objects.raw(SQLs.sql_saleProductManage, [store_id])
        receipts = receipts[(10*(page-1)):10*page]

    receipt_register_form = ReceiptRegisterForm()

    return render(request, 'saleProduct.html', \
        {'receipts' : receipts, 'receiptRegisterForm' : receipt_register_form, 'this_page' : page, 'pages' : pages})

@login_check_store
def saleProductList(request):
    receipt_id = int(request.GET.get('receipt_id', 'Error'))
    receipt = Receipt.objects.get(id=receipt_id)

    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_TRADE_LIST').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10 == 0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
    
        if process == 'register':
            form = TradeListRegisterForm(request.POST)
            if form.is_valid():
                barcode = form.cleaned_data['barcode'].barcode
                quantity = form.cleaned_data['quantity']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_tradeListRegister, [barcode, quantity, receipt_id])
                    
                return HttpResponseRedirect(reverse('saleProductList')+'?receipt_id=%s&page=%s' % (receipt_id, page))
            else:
                print(form.errors)
                print('가 발생')

    else:
        tradeList = Trade_list.objects.raw(SQLs.sql_tradeListManage, [receipt_id])
        tradeList = tradeList[(10*(page-1)):10*page]

        total_price = 0
        for trade in tradeList:
            product_info = Product.objects.raw(SQLs.sql_productSearchByBarcode, [trade.barcode.barcode])
            trade.subtotal_price = product_info[0].unit_price * trade.quantity
            total_price += trade.subtotal_price

    tradeList_register_form = TradeListRegisterForm()

    return render(request, 'saleProductList.html', \
        {'tradeList' : tradeList, 'tradeListRegisterForm' : tradeList_register_form, 'receipt': receipt, 'total_price' : total_price,\
        'this_page' : page, 'pages' : pages})

def customerRefundManage(request):
    return render(request, 'customerRefundManage.html')

#재고 관리
@login_check_store
def stockManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STOCK where store_id=%s', [store_id]).fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = StockRegisterForm(request.POST)
            elif process == 'update' :
                instance = Stock.objects.get(id=request.POST.get('id', 'Error')) # 해당 id가 있는지 확인
                form = StockUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id']
                            
                display_location_code = form.cleaned_data['display_location_code']
                barcode  = form.cleaned_data['barcode'].barcode
                quantity = form.cleaned_data['quantity']

                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_stockRegister, [store_id, display_location_code, barcode, quantity])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_stockUpdate, [display_location_code, barcode, quantity, store_id, id])
                
                return HttpResponseRedirect('/franchise/stockManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_stockDelete, [store_id, id])
            return HttpResponseRedirect('/franchise/stockManage?page=%s' % page)

    else:
        stocks = Stock.objects.raw(SQLs.sql_stockManage, [store_id])
        stocks = stocks[(10*(page-1)):10*page]

    stock_register_form = StockRegisterForm()
    stock_update_form = StockUpdateForm()

    return render(request, 'stockManage.html', \
        {'stocks' : stocks, 'stockRegisterForm' : stock_register_form, 'stockUpdateForm' : stock_update_form, \
            'this_page' : page, 'pages' : pages})
            


def expireDateManage(request):
    return render(request, 'expiryDateManage.html')

def saleManage(request):
    return render(request, 'saleManage.html')

@login_check_store
def maintenanceCostManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        if process == 'register':
            form = MaintenanceCostRegisterForm(request.POST)
            if form.is_valid():
                mccode = form.cleaned_data['maintenance_cost_code']
                amount = form.cleaned_data['amount']
                process_date = form.cleaned_data['process_date']
                employee_id = form.cleaned_data['employee_id'].id if form.cleaned_data['employee_id'] else None
                etc = form.cleaned_data['etc']

                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_maintenanceCostRegister, [mccode, amount, process_date, employee_id, etc, store_id])
                
                return HttpResponseRedirect('/franchise/maintenanceCostManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_maintenanceCostDelete, [id])
            return HttpResponseRedirect('/franchise/maintenanceCostManage?page=%s' % page)

    else:
        costs = Maintenance_cost.objects.raw(SQLs.sql_maintenanceCostManage, [store_id])
        costs = costs[(10*(page-1)):10*page]

    cost_register_form = MaintenanceCostRegisterForm()

    return render(request, 'maintenanceCostManage.html', \
        {'costs' : costs, 'maintenanceCostRegisterForm' : cost_register_form, 'this_page' : page, 'pages' : pages})

# 점원 관리
@login_check_store
def employeeManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))
        
        if process in ('register', 'update'):
            if process == 'register':
                form = EmployeeRegisterForm(request.POST)
            elif process == 'update' :
                instance = Employee.objects.get(id=request.POST.get('id', 'Error')) # 해당 id가 있는지 확인
                form = EmployeeUpdateForm(request.POST, instance=instance)
            if form.is_valid():
                if process == 'update':
                    id = form.cleaned_data['id']
                name = form.cleaned_data['name']
                daytime_hourpay = form.cleaned_data['daytime_hourpay']
                nighttime_hourpay = form.cleaned_data['nighttime_hourpay']
                employed_date = form.cleaned_data['employed_date']
                fire_date = form.cleaned_data['fire_date']
                contact = form.cleaned_data['contact']
                position_code = form.cleaned_data['position_code']
                
                with connection.cursor() as cursor:
                    if process == 'register':
                        cursor.execute(SQLs.sql_employeeRegister, [store_id, name, daytime_hourpay, nighttime_hourpay, employed_date, fire_date, contact, position_code])
                    elif process == 'update':
                        cursor.execute(SQLs.sql_employeeUpdate, [name, daytime_hourpay, nighttime_hourpay, employed_date, fire_date, contact, position_code, store_id, id])
                
                return HttpResponseRedirect('/franchise/employeeManage?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_employeeDelete, [store_id, id])
            return HttpResponseRedirect('/franchise/employeeManage?page=%s' % page)

    else:
        employees = Employee.objects.raw(SQLs.sql_employeeManage, [store_id])
        employees = employees[(10*(page-1)):10*page]

    employee_register_form = EmployeeRegisterForm()
    employee_update_form = EmployeeUpdateForm()

    return render(request, 'employeeManage.html', \
        {'employees' : employees, 'employeeRegisterForm' : employee_register_form, 'employeeUpdateForm' : employee_update_form, \
            'this_page' : page, 'pages' : pages})

# 고객 반품 관리
@login_check_store
def customerRefundManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(barcode) from MAINAPP_STORE_REFUND').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        f = request.POST.dict()

        if process == 'register':
            form = StoreRefundRegisterForm(f)
            if form.is_valid():
                barcode = form.cleaned_data['barcode'].barcode
                quantity = form.cleaned_data['quantity']
                refund_timestamp = form.cleaned_data['refund_timestamp']
                refund_reason_code = form.cleaned_data['refund_reason_code']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_storeRefundRegister, [barcode, quantity, refund_timestamp, refund_reason_code, store_id])
                
                return HttpResponseRedirect(reverse('customerRefundManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_storeRefundDelete, [id])
            return HttpResponseRedirect(reverse('customerRefundManage')+'?page=%s' % page)

    else:
        refunds = Store_refund.objects.raw(SQLs.sql_storeRefundManage, [store_id])
        refunds = refunds[(10*(page-1)):10*page]

    storeRefund_register_form = StoreRefundRegisterForm()

    return render(request, 'customerRefundManage.html', \
        {'refunds' : refunds, 'storeRefundRegisterForm' : storeRefund_register_form, 'this_page' : page, 'pages' : pages})

# 근무 기록 관리
@login_check_store
def workListManage(request):
    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        if process == 'register':
            form = WorkListRegisterForm(request.POST)
            if form.is_valid():
                employee_id = form.cleaned_data['employee_id'].id
                workstart_timestamp = form.cleaned_data['workstart_timestamp']
                workend_timestamp = form.cleaned_data['workend_timestamp']
                
                with connection.cursor() as cursor:
                    cursor.execute(SQLs.sql_workListRegister, [employee_id, workstart_timestamp, workend_timestamp])
                
                return HttpResponseRedirect(reverse('workListManage')+'?page=%s' % page)
            else:
                print(form.errors)
                print('가 발생')

        elif process == 'delete':
            id = int(request.POST.get('id', 'Error'))
            with connection.cursor() as cursor:
                cursor.execute(SQLs.sql_workListDelete, [id])
            return HttpResponseRedirect(reverse('workListManage')+'?page=%s' % page)

    else:
        worklists = Work_list.objects.raw(SQLs.sql_workListManage, [store_id])
        worklists = worklists[(10*(page-1)):10*page]

    worklist_register_form = WorkListRegisterForm()

    return render(request, 'workListManage.html', \
        {'worklists' : worklists, 'workListRegisterForm' : worklist_register_form, 'this_page' : page, 'pages' : pages})

# 월급 조회
@login_check_store
def salaryManage(request):
    # 커스텀 SQL 용 함수
    def dictfetchall(cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    store_id = request.session['store_id']

    #페이지네이션
    with connection.cursor() as c:
        cnt = c.execute('select count(id) from MAINAPP_STORE').fetchone()
    cnt = int(cnt[0])
    page = int(request.GET.get('page', 1))#현재페이지
    j = int(cnt/10)#5보다작으면 처리필요
    if j>=5:
        pages = [a for a in range(max(1, page-2), max(5, page+2)+1)]
    else:
        if cnt%10==0:
            pages = [a for a in range(max(1, page-2), j+1)]
        else:
            pages = [a for a in range(max(1, page-2), j+2)]

            
    if request.method == 'POST':
        process = str(request.GET.get('process', False))

        if process == 'search':
            form = SalaryManageForm(request.POST)
            if form.is_valid():
                date_min = form.cleaned_data['date_min']
                date_max = form.cleaned_data['date_max']
    else:
        # 기본 조회 기간 : 현재 월
        date_min = datetime.datetime.now().replace(day=1)
        date_max = date_min + datetime.timedelta(days=30)

    # 현재 지점의 모든 점원 정보 가져오기
    with connection.cursor() as cursor:
        cursor.execute(SQLs.sql_employeeManage, [store_id])
        emp_list = dictfetchall(cursor)

    day_works = {}
    salries = []
    for row in emp_list:
        emp = row['NAME']
        emp_id = row['ID']
        day_pay = row['DAYTIME_HOURPAY']
        with connection.cursor() as cursor:
            cursor.execute(SQLs.sql_workListQueryForSalary, [emp_id, date_min, date_max])
            work_list = dictfetchall(cursor)

            for work in work_list:
                try:
                    day_works[emp] += (work['WORKEND_TIMESTAMP'] - work['WORKSTART_TIMESTAMP'])
                except KeyError:
                    day_works[emp] = (work['WORKEND_TIMESTAMP'] - work['WORKSTART_TIMESTAMP'])

            try:
                salries.append({'id' : emp, 'total_day' : day_works[emp], 'total_night' : None, \
                    'amount' : day_works[emp].total_seconds()//3600 * day_pay})
            except KeyError:
                pass # 아직 근무기록 없는 경우
    
    # 점원별 근무시간 합 계산
    salary_manage_form = SalaryManageForm()
    return render(request, 'salaryManage.html', \
        {'salaries' : salries, 'salaryManageForm' : salary_manage_form, 'this_page' : page, 'pages' : pages})