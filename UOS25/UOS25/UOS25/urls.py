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
from django.urls import path
from django.contrib.auth import views as auth_views
from mainapp.views import *
#123 : 미구현
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login),#로그인페이지
    path('index/',index),#가맹점인덱스
    path('indexAdmin/',indexAdmin),#본사인덱스
    ###가맹점페이지
    path('orderHeadManage/',orderHeadManage),#본사주문관리
    path('refundHeadManage/',refundHeadManage),#본사반품관리
    path('saleProduct/',saleProduct),#물품판매
    path('refundCustomerManage/',refundCustomerManage),#고객반품관리
    path('registerProduct/',registerProduct),#재고추가
    path('deleteProduct/',deleteProduct),#재고삭제
    path('expiryDateManage/',expiryDateManage),#유통기한관리123
    path('saleManage/',saleManage),#매출관리123
    path('costManage/',costManage),#유지비관리123
    path('employeeManage/',employeeManage),#점원관리
    path('workRecordManage/',workRecordManage),#근무기록관리123
    path('salaryManage/',salaryManage),#월급관리123
    ###본사페이지
    
]
