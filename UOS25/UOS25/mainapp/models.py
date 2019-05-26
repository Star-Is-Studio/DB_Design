from django.db import models

# Create your models here.

class Store(models.Model):
    address = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    store_pay = models.FloatField() # 가맹요금비율
    store_code = models.IntegerField() # 지점상태코드
    
class Supplier(models.Model):
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    
class Product(models.Model):
    barcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    supply_price = models.IntegerField()
    unit_price = models.IntegerField()
    supplier_id = models.ForeignKey(Supplier.id) # ?
    category_a = models.IntegerField() # 상품 대분류 코드
    category_b = models.IntegerField() # 상품 소분류 코드
    information = models.TextField()
    img_path = models.TextField() # 사진파일경로

class Stock(models.Model):
    store_id = models.ForeignKey(Store.id)
    location_code = models.IntegerField() # TODO 이름이..
    barcode  = models.ForeignKey(Product.barcode)
    quantity = models.IntegerField()

class Order(models.Model):
    store_id = models.ForeignKey(Store.id)
    order_timestamp = models.DateTimeField()
    complete_timestamp = models.DateTimeField()
    process_code = models.IntegerField()
    
class Orderlist(models.Model):
    order_id = models.ForeignKey(Order.id)
    barcode = models.ForeignKey(Product.barcode)
    quantity = models.IntegerField()
    sent_timestamp = models.DateTimeField()
    arrival_timestamp = models.DateTimeField()
    process_code = models.IntegerField()
    

class Storerefund(models.Model):
    store_id = models.ForeignKey(Store.id)
    barcode = models.ForeignKey(Product.id)
    quantity = models.IntegerField()
    refund_timestamp = models.IntegerField()
    refund_reason_code = models.IntegerField()
    process_code = models.IntegerField()

class Storercpt(models.Model): # 가맹요금수납
    store_id = models.ForeignKey(Store.id)
    rcpt_timestamp = models.DateTimeField()
    amount = models.IntegerField()
    
class Employee(models.Model):
    store_id = models.ForeignKey(Store.id)
    name = models.CharField(max_length=25)
    daytime_hourpay = models.IntegerField()
    nighttime_hourpay = models.IntegerField()
    employed_date =  models.DateField()
    fire_date=  models.DateField()
    contact = models.CharField(20)
    position_code = models.IntegerField()

class Worklist(models.Model):
    emp_id = models.ForeignKey(Employee.id)
    name = models.CharField(max_length=25)
    workstart_timestamp = models.DateTimeField()
    workend_timestamp = models.DateTimeField()
    storeowner_check = models.BooleanField()

class Maintenance(models.Model):
    store_id = models.ForeignKey(Store.id)
    maintenance_code = models.IntegerField()
    amount = models.IntegerField()
    process_date = models.DateField()
    emp_id = models.ForeignKey(Employee.id)
    information = models.TextField() # 비고
    storeowner_check = models.BooleanField()

class Customer(models.Model):
    name = models.CharField()
    mileage = models.IntegerField()
    gender = models.IntegerField()
    birthday = models.DateField()
    contact = models.CharField()

class Receipt(models.Model):
    store_id = models.ForeignKey(Store.id)
    trade_timestamp = models.DateTimeField()
    emp_id = models.ForeignKey(Employee.id)
    customer_id = models.ForeignKey(Customer.id)
    payment_method_code = models.IntegerField()
    payment_information = models.CharField(max_length=20) # TODO 초단문?
    
class Tradelist(models.Model):
    receipt_id = models.ForeignKey(Receipt.id)
    barcode = models.ForeignKey(Product.barcode)
    quantity = models.IntegerField()
    is_refund = models.BooleanField()
    
class Customerrefund(models.Model):
    # receipt_id = models.ForeignKey() TODO 장고가 외래키를 기본키로 사용할 수 없는 걸로 보임.
    refund_date = models.DateTimeField()
    refund_reason_code = models.IntegerField()

class Setting(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()

class Code(models.Model):
    information = models.CharField(max_length=20)