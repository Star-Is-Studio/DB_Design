from django.db import models

# Create your models here.

class Store(models.Model):
    address = models.CharField(max_length=80)
    contact = models.CharField(max_length=20)
    store_pay = models.FloatField(default=None) # 가맹요금비율
    store_code = models.IntegerField(default=None) # 지점상태코드

class Supplier(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    
class Product(models.Model):
    barcode = models.IntegerField(default=0, primary_key=True)
    name = models.CharField(max_length=50)
    supply_price = models.IntegerField(default=None)
    unit_price = models.IntegerField(default=None)
    supplier = models.ForeignKey(Supplier, default=None) # ?
    category_a = models.IntegerField(default=None) # 상품 대분류 코드
    category_b = models.IntegerField(default=None) # 상품 소분류 코드
    information = models.TextField(default=None)
    img_path = models.TextField(default=None) # 사진파일경로

class Stock(models.Model):
    store = models.ForeignKey(Store)
    location_code = models.IntegerField(default=None) # TODO 이름이..
    barcode  = models.ForeignKey(Product)
    quantity = models.IntegerField(default=None)

class Order(models.Model):
    store = models.ForeignKey(Store)
    order_timestamp = models.DateTimeField(default=None)
    complete_timestamp = models.DateTimeField(default=None)
    process_code = models.IntegerField(default=None)
    
class Orderlist(models.Model):
    order = models.ForeignKey(Order)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField(default=None)
    sent_timestamp = models.DateTimeField()
    arrival_timestamp = models.DateTimeField()
    process_code = models.IntegerField(default=None)
    

class Storerefund(models.Model):
    store = models.ForeignKey(Store)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField(default=None)
    refund_timestamp = models.IntegerField(default=None)
    refund_reason_code = models.IntegerField(default=None)
    process_code = models.IntegerField(default=None)

class Storercpt(models.Model): # 가맹요금수납
    store = models.ForeignKey(Store)
    rcpt_timestamp = models.DateTimeField()
    amount = models.IntegerField(default=None)
    
class Employee(models.Model):
    store = models.ForeignKey(Store)
    name = models.CharField(max_length=25)
    daytime_hourpay = models.IntegerField(default=None)
    nighttime_hourpay = models.IntegerField(default=None)
    employed_date =  models.DateField()
    fire_date=  models.DateField()
    contact = models.CharField(max_length=20)
    position_code = models.IntegerField(default=None)

class Worklist(models.Model):
    emp = models.ForeignKey(Employee)
    workstart_timestamp = models.DateTimeField()
    workend_timestamp = models.DateTimeField()
    storeowner_check = models.CharField(max_length=1)

class Maintenance(models.Model):
    store = models.ForeignKey(Store)
    maintenance_code = models.IntegerField(default=None)
    amount = models.IntegerField(default=None)
    process_date = models.DateField()
    emp = models.ForeignKey(Employee)
    information = models.TextField(default=None) # 비고
    storeowner_check = models.CharField(max_length=1)

class Customer(models.Model):
    name = models.CharField(max_length=25)
    mileage = models.IntegerField(default=None)
    gender = models.IntegerField(default=None)
    birthday = models.DateField()
    contact = models.CharField(max_length=20)

class Receipt(models.Model):
    store = models.ForeignKey(Store)
    trade_timestamp = models.DateTimeField()
    emp = models.ForeignKey(Employee)
    customer = models.ForeignKey(Customer)
    payment_method_code = models.IntegerField(default=None)
    payment_information = models.CharField(max_length=30)
    
class Tradelist(models.Model):
    receipt = models.ForeignKey(Receipt)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField(default=None)
    is_refund = models.CharField(max_length=1)
    
class Customerrefund(models.Model):
    receipt = models.ForeignKey(Receipt) # TODO 장고가 외래키를 기본키로 사용할 수 없는 걸로 보임.
    refund_date = models.DateTimeField()
    refund_reason_code = models.IntegerField(default=None)

class Setting(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField(default=None)

class Code(models.Model):
    information = models.CharField(max_length=20)

# no need.
class User(models.Model):
    userId = models.IntegerField()
    password = models.CharField(max_length=200)