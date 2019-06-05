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

# 본사 페이지
admin_urlpatterns = [
    path(r'^admin/$',indexAdmin, name='indexAdmin'),#본사인덱스
    path(r'^admin/ranchiseManage/$',franchiseManage, name='franchiseManage'),#가맹점 관리
    path(r'^admin/franchiseCostManage/$',franchiseCostManage, name='franchiseCostManage'),#가맹요금 수납
    path(r'^admin/deliveryManage/$',deliveryManage, name='deliveryManage'),#납품 업체 관리
    path(r'^admin/franchiseOrderManage/$',franchiseOrderManage, name='franchiseOrderManage'),#가맹점 주문 관리
    path(r'^admin/registerHeadProduct/$',registerHeadProduct, name='registerHeadProduct'),#상품 등록
    path(r'^admin/HeadProductManage/$',HeadProductManage, name='HeadProductManage'),#상품 조회/삭제
    path(r'^admin/registerCustomer/$',registerCustomer, name='registerCustomer'),#고객 등록
    path(r'^admin/customerManage/$',customerManage, name='customerManage'),#고객 조회/삭제
]

# 가맹점 페이지
franchise_urlpatterns = [    
    path(r'^franchise/$',index, name='index'),#가맹점인덱스
    path(r'^franchise/orderHeadManage/$',orderHeadManage, name='orderHeadManage'),#본사주문관리
    path(r'^franchise/refundHeadManage/$',refundHeadManage, name='refundHeadManage'),#본사반품관리
    path(r'^franchise/saleProduct/$',saleProduct, name='saleProduct'),#물품판매
    path(r'^franchise/refundCustomerManage/$',refundCustomerManage, name='refundCustomerManage'),#고객반품관리
    path(r'^franchise/registerProduct/$',registerProduct, name='registerProduct'),#재고추가
    path(r'^franchise/deleteProduct/$',deleteProduct, name='deleteProduct'),#재고삭제
    path(r'^franchise/expiryDateManage/$',expiryDateManage, name='expiryDateManage'),#유통기한관리
    path(r'^franchise/saleManage/$',saleManage, name='saleManage'),#매출관리
    path(r'^franchise/costManage/$',costManage, name='costManage'),#유지비관리
    path(r'^franchise/employeeManage/$',employeeManage, name='employeeManage'),#점원관리
    path(r'^franchise/workRecordManage/$',workRecordManage, name='workRecordManage'),#근무기록관리
    path(r'^franchise/salaryManage/$',salaryManage, name='salaryManage'),#월급관리
]

# 통합페이지
urlpatterns = [
    path(r'^$',login, name='login'),#로그인페이지
] + admin_urlpatterns + franchise_urlpatterns

