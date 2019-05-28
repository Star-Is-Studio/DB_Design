from django.db import models

# Create your models here.

class Store(models.Model):
    address = models.CharField(max_length=80)
    contact = models.CharField(max_length=20)
    store_pay = models.FloatField() # 가맹요금비율
    store_code = models.IntegerField() # 지점상태코드
    
class Supplier(models.Model):
    name = models.CharField(max_length=25)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    
class Product(models.Model):
    barcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    supply_price = models.IntegerField()
    unit_price = models.IntegerField()
    supplier_id = models.ForeignKey(Supplier) # ?
    category_a = models.IntegerField() # 상품 대분류 코드
    category_b = models.IntegerField() # 상품 소분류 코드
    information = models.TextField()
    img_path = models.TextField() # 사진파일경로

class Stock(models.Model):
    store_id = models.ForeignKey(Store)
    location_code = models.IntegerField() # TODO 이름이..
    barcode  = models.ForeignKey(Product)
    quantity = models.IntegerField()

class Order(models.Model):
    store_id = models.ForeignKey(Store)
    order_timestamp = models.DateTimeField()
    complete_timestamp = models.DateTimeField()
    process_code = models.IntegerField()
    
class Orderlist(models.Model):
    order_id = models.ForeignKey(Order)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField()
    sent_timestamp = models.DateTimeField()
    arrival_timestamp = models.DateTimeField()
    process_code = models.IntegerField()
    

class Storerefund(models.Model):
    store_id = models.ForeignKey(Store)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField()
    refund_timestamp = models.IntegerField()
    refund_reason_code = models.IntegerField()
    process_code = models.IntegerField()

class Storercpt(models.Model): # 가맹요금수납
    store_id = models.ForeignKey(Store)
    rcpt_timestamp = models.DateTimeField()
    amount = models.IntegerField()
    
class Employee(models.Model):
    store_id = models.ForeignKey(Store)
    name = models.CharField(max_length=25)
    daytime_hourpay = models.IntegerField()
    nighttime_hourpay = models.IntegerField()
    employed_date =  models.DateField()
    fire_date=  models.DateField()
    contact = models.CharField(max_length=20)
    position_code = models.IntegerField()

class Worklist(models.Model):
    emp_id = models.ForeignKey(Employee)
    workstart_timestamp = models.DateTimeField()
    workend_timestamp = models.DateTimeField()
    storeowner_check = models.CharField(max_length=1)

class Maintenance(models.Model):
    store_id = models.ForeignKey(Store)
    maintenance_code = models.IntegerField()
    amount = models.IntegerField()
    process_date = models.DateField()
    emp_id = models.ForeignKey(Employee)
    information = models.TextField() # 비고
    storeowner_check = models.CharField(max_length=1)

class Customer(models.Model):
    name = models.CharField(max_length=25)
    mileage = models.IntegerField()
    gender = models.IntegerField()
    birthday = models.DateField()
    contact = models.CharField(max_length=20)

class Receipt(models.Model):
    store_id = models.ForeignKey(Store)
    trade_timestamp = models.DateTimeField()
    emp_id = models.ForeignKey(Employee)
    customer_id = models.ForeignKey(Customer)
    payment_method_code = models.IntegerField()
    payment_information = models.CharField(max_length=30)
    
class Tradelist(models.Model):
    receipt_id = models.ForeignKey(Receipt)
    barcode = models.ForeignKey(Product)
    quantity = models.IntegerField()
    is_refund = models.BooleanField()
    
class Customerrefund(models.Model):
    receipt_id = models.ForeignKey(Receipt) # TODO 장고가 외래키를 기본키로 사용할 수 없는 걸로 보임.
    refund_date = models.DateTimeField()
    refund_reason_code = models.IntegerField()

class Setting(models.Model):
    name = models.CharField(max_length=20)
    value = models.IntegerField()

class Code(models.Model):
    information = models.CharField(max_length=20)

# no need.
class User(models.Model):
    userId = models.IntegerField()