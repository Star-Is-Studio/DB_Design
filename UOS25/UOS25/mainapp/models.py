from django.db import models

# Create your models here.

# 지점 테이블
class Store(models.Model):
    address = models.CharField(max_length=80, null=False)
    contact = models.CharField(max_length=20, null=False)
    # 용어사전 반영 필요
    store_pay = models.FloatField(null=False) # 가맹요금비율
    store_code = models.DecimalField(decimal_places=0, max_digits=4, null=False) # 지점상태코드

# 납품업체 테이블
class Supplier(models.Model):
    name = models.CharField(max_length=25, null=False)
    contact = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=40, null=False)
    
# 상품 테이블
class Product(models.Model):
    barcode = models.DecimalField(decimal_places=0, max_digits=13, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    supply_price = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    unit_price = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    supplier_id = models.ForeignKey(Supplier, null=False, db_column='supplier_id') 
    category_a = models.DecimalField(decimal_places=0, max_digits=4, null=False) # 상품 대분류 코드
    category_b = models.DecimalField(decimal_places=0, max_digits=4, null=False) # 상품 소분류 코드
    explain = models.CharField(max_length=80, null=True)
    picture_file_path = models.CharField(max_length=80, null=True) # 사진파일경로

# 재고 테이블
class Stock(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    display_location_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    barcode  = models.ForeignKey(Product, null=False)
    quantity = models.DecimalField(decimal_places=0, max_digits=6, default=0, null=False)

# 주문 테이블
class Order(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    order_timestamp = models.DateTimeField(null=False)
    complete_timestamp = models.DateTimeField(null=True)
    process_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    
# 주문내역 테이블
class Order_list(models.Model):
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    sent_timestamp = models.DateTimeField(null=True)
    arrival_timestamp = models.DateTimeField(null=True)
    process_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    order_id = models.ForeignKey(Order, null=False)

# 지점반품 테이블
class Store_refund(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    refund_timestamp = models.DateTimeField(null=False)
    refund_reason_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    process_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)

# 가맹요금수납 테이블
class Franchise_store_rcpt(models.Model): # 가맹요금수납
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    rcpt_date = models.DateField(null=False)
    rcpt_amount = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    
# 점원 테이블
class Employee(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    name = models.CharField(max_length=25, null=False)
    daytime_hourpay = models.DecimalField(decimal_places=0, max_digits=10, null=True, default=6800)
    nighttime_hourpay = models.DecimalField(decimal_places=0, max_digits=10, null=True)
    employed_date =  models.DateField(null=False)
    fire_date=  models.DateField(null=True)
    contact = models.CharField(max_length=20, null=False)
    position_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)

# 근무기록 테이블
class Work_list(models.Model):
    employee_id = models.ForeignKey(Employee, null=False, db_column='employee_id')
    workstart_timestamp = models.DateTimeField(null=False)
    workend_timestamp = models.DateTimeField(null=False)
    storeowner_check = models.CharField(max_length=1, default='N', null=False)

# 유지비 테이블
class Maintenance_cost(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    maintenance_cost_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    amount = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    process_date = models.DateField(null=False)
    employee_id = models.ForeignKey(Employee, null=True, db_column='employee_id')
    etc = models.CharField(max_length=80, null=True) # 비고
    storeowner_check = models.CharField(max_length=1, default='N', null=False)
 
# 고객 테이블
class Customer(models.Model):
    name = models.CharField(max_length=25, null=False)
    mileage = models.DecimalField(decimal_places=0, max_digits=10, default=0, null=False)
    gender = models.DecimalField(decimal_places=0, max_digits=4, null=True)
    birthday = models.DateField(null=True)
    contact = models.CharField(max_length=20, null=True)

# 영수증 테이블
class Receipt(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    trade_timestamp = models.DateTimeField(null=False)
    employee_id = models.ForeignKey(Employee, null=False, db_column='employee_id')
    customer_id = models.ForeignKey(Customer, null=True, db_column='customer_id')
    payment_method_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)
    payment_information = models.CharField(max_length=30, null=True)
    
# 거래내역 테이블
class Trade_list(models.Model):
    receipt_id = models.ForeignKey(Receipt, null=False, db_column='receipt_id')
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    is_refund = models.CharField(max_length=1, default='N', null=False)
    
# 고객반품 테이블
class Customer_refund(models.Model):
    trade_list_id = models.ForeignKey(Trade_list, null=False, db_column='trade_list_id')
    refund_timestamp = models.DateTimeField(null=False)
    refund_reason_code = models.DecimalField(decimal_places=0, max_digits=4, null=False)

class Setting(models.Model):
    name = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=0)

class Code(models.Model):
    information = models.CharField(max_length=20)

class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    store_id = models.ForeignKey(Store, db_column='store_id', null=True)