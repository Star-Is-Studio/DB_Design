"""UOS25 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from mainapp.views import *
from django.conf.urls import url as path
#123 : 미구현
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),
    path(r'^$',login, name='login'),#로그인페이지
    path('index/',index, name='index'),#가맹점인덱스
    path('indexAdmin/',indexAdmin, name='indexAdmin'),#본사인덱스
    ###가맹점페이지
    path('orderHeadManage/',orderHeadManage, name='orderHeadManage'),#본사주문관리
    path('refundHeadManage/',refundHeadManage, name='refundHeadManage'),#본사반품관리
    path('saleProduct/',saleProduct, name='saleProduct'),#물품판매
    path('refundCustomerManage/',refundCustomerManage, name='refundCustomerManage'),#고객반품관리
    path('registerProduct/',registerProduct, name='registerProduct'),#재고추가
    path('deleteProduct/',deleteProduct, name='deleteProduct'),#재고삭제
    path('expiryDateManage/',expiryDateManage, name='expiryDateManage'),#유통기한관리123
    path('saleManage/',saleManage, name='saleManage'),#매출관리123
    path('costManage/',costManage, name='costManage'),#유지비관리123
    path('employeeManage/',employeeManage, name='employeeManage'),#점원관리
    path('workRecordManage/',workRecordManage, name='workRecordManage'),#근무기록관리123
    path('salaryManage/',salaryManage, name='salaryManage'),#월급관리123
    ###본사페이지
    path('franchiseManage/',franchiseManage, name='franchiseManage'),#가맹점 관리
    path('franchiseCostManage/',franchiseCostManage, name='franchiseCostManage'),#가맹요금 수납
    path('deliveryManage/',deliveryManage, name='deliveryManage'),#납품 업체 관리
    path('franchiseOrderManage/',franchiseOrderManage, name='franchiseOrderManage'),#가맹점 주문 관리
    path('registerHeadProduct/',registerHeadProduct, name='registerHeadProduct'),#상품 등록
    path('HeadProductManage/',HeadProductManage, name='HeadProductManage'),#상품 조회/삭제
    path('registerCustomer/',registerCustomer, name='registerCustomer'),#고객 등록
    path('customerManage/',customerManage, name='customerManage'),#고객 조회/삭제
]
