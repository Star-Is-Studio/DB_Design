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
from django.conf.urls import url

# 본사 페이지
central_urlpatterns = [
    url(r'^central/$',indexAdmin, name='indexAdmin'),#본사인덱스
    url(r'^central/franchiseManage/$',franchiseManage, name='franchiseManage'),#가맹점 관리
    url(r'^central/franchiseCostManage/$',franchiseCostManage, name='franchiseCostManage'),#가맹요금 수납
    url(r'^central/supplierManage/$', supplierManage, name='supplierManage'),#납품 업체 관리
    url(r'^central/storeOrderManage/$', storeOrderManage, name='storeOrderManage'),#지점 주문 관리
    url(r'^central/registerProduct/$', registerProduct, name='registerProduct'),#상품 등록
    url(r'^central/productManage/$', productManage, name='productManage'),#상품 조회/삭제
    url(r'^central/customerManage/$',customerManage, name='customerManage'),#고객 조회/삭제
]

# 가맹점 페이지
franchise_urlpatterns = [    
    url(r'^franchise/$',index, name='index'),#가맹점인덱스
    url(r'^franchise/orderManage/$',orderManage, name='orderManage'),#주문관리
    url(r'^franchise/centralRefundManage/$', centralRefundManage, name='centralRefundManage'),#본사반품관리
    url(r'^franchise/saleProduct/$', saleProduct, name='saleProduct'),#물품판매
    url(r'^franchise/customerRefundManage/$', customerRefundManage, name='customerRefundManage'),#고객반품관리
    url(r'^franchise/registerStock/$',registerStock, name='registerStock'),#재고추가
    url(r'^franchise/deleteStock/$',deleteStock, name='deleteStock'),#재고삭제
    url(r'^franchise/expireDateManage/$',expireDateManage, name='expireDateManage'),#유통기한관리
    url(r'^franchise/saleManage/$',saleManage, name='saleManage'),#매출관리
    url(r'^franchise/maintenanceCostManage/$',maintenanceCostManage, name='maintenanceCostManage'),#유지비관리
    url(r'^franchise/employeeManage/$',employeeManage, name='employeeManage'),#점원관리
    url(r'^franchise/workListManage/$',workListManage, name='workListManage'),#근무기록관리
    url(r'^franchise/salaryManage/$',salaryManage, name='salaryManage'),#월급관리
]

# 통합페이지
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',login, name='login'),#로그인페이지
] + central_urlpatterns + franchise_urlpatterns
