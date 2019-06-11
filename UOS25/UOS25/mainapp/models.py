from django.db import models, connection
from decimal import Decimal
from mainapp.sqls import SQLs

# Create your models here.

# 지점 테이블
class Store(models.Model):
    address = models.CharField(max_length=80, null=False)
    contact = models.CharField(max_length=20, null=False)
    # 용어사전 반영 필요
    store_pay = models.DecimalField(decimal_places=2, max_digits=3,null=False) # 가맹요금비율

    __STORE_CODE__ = [
        (1, '개점'),
        (2, '폐점'),
    ]
    store_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__STORE_CODE__, null=False) # 지점상태코드

    def __str__(self):
        return '_'.join((str(self.id), self.address[:10]))

# 납품업체 테이블
class Supplier(models.Model):
    name = models.CharField(max_length=25, null=False)
    contact = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=40, null=False)

    def __str__(self):
        return self.name
    
# 상품 테이블
class Product(models.Model):
    barcode = models.DecimalField(decimal_places=0, max_digits=13, primary_key=True)
    name = models.CharField(max_length=50, null=False)
    supply_price = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    unit_price = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    supplier_id = models.ForeignKey(Supplier, null=False, db_column='supplier_id')

    __CATEGORY_A__ = [
        (0, '기타'),
        (1, '신선식품'),
        (2, '식품'),
        (3, '주류'),
        (4, '생활용품'),
        (5, '담배')
    ]
    category_a = models.DecimalField(decimal_places=0, max_digits=4, choices=__CATEGORY_A__, null=False) # 상품 분류 코드

    __CATEGORY_B__ = [
        (0, '일반판매'),
        (1, '기간한정판매'),
        (2, '할인행사판매')
    ]
    category_b = models.DecimalField(decimal_places=0, max_digits=4, choices=__CATEGORY_B__, null=False) # 판매 분류 코드
    explain = models.CharField(max_length=80, null=True)
    picture_file_path = models.CharField(max_length=80, null=True) # 사진파일경로

    def __str__(self):
        return self.name

# 재고 테이블
class Stock(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    __DISP_LOC_CODE__ = [
        (0, '진열'),
        (1, '창고'),
        (2, '매장외부'),
    ]
    display_location_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__DISP_LOC_CODE__, null=False)
    barcode  = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, default=0, null=False)

# 주문 테이블
class Order(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    order_timestamp = models.DateTimeField(null=False)
    complete_timestamp = models.DateTimeField(null=True)

    __PROCESS_CODE__ = [
        (0, '처리대기'),
        (1, '배송시작'),
        (2, '배송완료'),
        (3, '처리완료'),
        (-1, '주문취소'),
    ]
    process_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__PROCESS_CODE__, null=False)
    
    def sum_price(self):
        with connection.cursor() as cursor:
            gett = cursor.execute(SQLs.sql_storeOrderTotalPrice,[self.id]).fetchone() 
            val = gett[0]
        return val
        
    
# 주문내역 테이블
class Order_list(models.Model):
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    sent_timestamp = models.DateTimeField(null=True)
    arrival_timestamp = models.DateTimeField(null=True)

    __PROCESS_CODE__ = [
        (0, '처리대기'),
        (1, '배송시작'),
        (2, '배송완료'),
        (3, '처리완료'),
        (-1, '주문취소'),
        (-2, '처리불가'),
    ]
    process_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__PROCESS_CODE__, null=False)
    order_id = models.ForeignKey(Order, null=False, db_column='order_id') #기존 것은 db_column 빼먹었으므로 고친다면 주의

# 지점반품 테이블
class Store_refund(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    refund_timestamp = models.DateTimeField(null=False)

    __REFUND_REASON_CODE__ = [
        (0, '일반반품'),
        (1, '본사리콜'),
        (2, '불량품'),
        (-1, '유통기한폐기')
    ]
    refund_reason_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__REFUND_REASON_CODE__, null=False)

    __PROCESS_CODE__ = [
        (0, '반품대기'),
        (1, '회수완료'),
        (2, '반품불가'),
        (-1, '자체폐기'),
    ]
    process_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__PROCESS_CODE__, null=False)

# 고객반품 테이블
class Customer_refund(models.Model):
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    refund_timestamp = models.DateTimeField(null=False)

    __REFUND_REASON_CODE__ = [
        (0, '일반반품'),
        (1, '불량품'),
    ]
    refund_reason_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__REFUND_REASON_CODE__, null=False)

    __PROCESS_CODE__ = [
        (0, '반품대기'),
        (1, '회수완료'),
        (2, '반품불가'),
        (-1, '자체폐기'),
    ]
    process_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__PROCESS_CODE__, null=False)

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

    __POSITION_CODE__ = [
        (0, '점주'),
        (1, '매니저'),
        (2, '직원'),
    ]
    position_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__POSITION_CODE__, null=False)

    def __str__(self):
        return self.name

# 근무기록 테이블
class Work_list(models.Model):
    employee_id = models.ForeignKey(Employee, null=False, db_column='employee_id')
    workstart_timestamp = models.DateTimeField(null=False)
    workend_timestamp = models.DateTimeField(null=False)

    __STOREOWNER_CHECK__ = [
        ('N', '미확인'),
        ('Y', '확인'),
    ]
    storeowner_check = models.CharField(max_length=1, default='N', choices=__STOREOWNER_CHECK__, null=False)

# 유지비 테이블
class Maintenance_cost(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    __MAINTENANCE_COST_CODE__ = [
        (0, '기타'),
        (1, '세금/유지비'),
        (2, '월세'),
        (3, '직원과실'),
        (4, '절도')
    ]
    maintenance_cost_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__MAINTENANCE_COST_CODE__, null=False)
    amount = models.DecimalField(decimal_places=0, max_digits=10, null=False)
    process_date = models.DateField(null=False)
    employee_id = models.ForeignKey(Employee, null=True, db_column='employee_id')
    etc = models.CharField(max_length=80, null=True) # 비고
    __STOREOWNER_CHECK__ = [
        ('N', '미확인'),
        ('Y', '확인'),
    ]
    storeowner_check = models.CharField(max_length=1, default='N', choices=__STOREOWNER_CHECK__, null=False)
 
# 고객 테이블
class Customer(models.Model):
    name = models.CharField(max_length=25, null=False)
    mileage = models.DecimalField(decimal_places=0, max_digits=10, default=0, null=False)
    __GENDER__ = [
        (None, '미선택'),
        (1, '남'),
        (2, '여')
    ]
    gender = models.DecimalField(decimal_places=0, max_digits=4, choices=__GENDER__, null=True)
    birthday = models.DateField(null=True)
    contact = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name

# 영수증 테이블
class Receipt(models.Model):
    store_id = models.ForeignKey(Store, null=False, db_column='store_id')
    trade_timestamp = models.DateTimeField(null=False)
    employee_id = models.ForeignKey(Employee, null=False, db_column='employee_id')
    customer_id = models.ForeignKey(Customer, null=True, db_column='customer_id')
    __PAYMENT_METHOD_CODE__ = [
        (0, '현금'),
        (1, '체크/신용카드'),
        (2, '편의점상품권'),
        (3, '마일리지'),
        (4, '간편결제앱'),
    ]
    payment_method_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__PAYMENT_METHOD_CODE__, null=False)
    payment_information = models.CharField(max_length=30, null=True)
    
# 거래내역 테이블
class Trade_list(models.Model):
    receipt_id = models.ForeignKey(Receipt, null=False, db_column='receipt_id')
    barcode = models.ForeignKey(Product, null=False, db_column='barcode')
    quantity = models.DecimalField(decimal_places=0, max_digits=6, null=False)
    __IS_REFUND__ = [
        ('N', '미반품'),
        ('Y', '반품됨'),
    ]
    is_refund = models.CharField(max_length=1, default='N', null=False)
    
# 고객반품 테이블
class Customer_refund(models.Model):
    trade_list_id = models.ForeignKey(Trade_list, null=False, db_column='trade_list_id')
    refund_timestamp = models.DateTimeField(null=False)
    __REFUND_REASON_CODE__ = [
        (0, '일반반품'),
        (1, '본사리콜'),
        (2, '불량품'),
        (-1, '유통기한')
    ]
    refund_reason_code = models.DecimalField(decimal_places=0, max_digits=4, choices=__REFUND_REASON_CODE__, null=False)

class Setting(models.Model):
    name = models.CharField(max_length=20)
    value = models.DecimalField(max_digits=10, decimal_places=0)

class Code(models.Model):
    information = models.CharField(max_length=20)

class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    store_id = models.ForeignKey(Store, db_column='store_id', null=True)
    # employee_id = models.ForeignKey(Employee, db_column='employee_id', null=True)
    __EMP_POS_CODE__ = [
        (0, '지점장/본점장'),
        (1, '직원'),
    ]
    emp_pos_code = models.DecimalField(max_digits=1, decimal_places=0, choices=__EMP_POS_CODE__, null=False, default=0)