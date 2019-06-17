# SQL Statements.

class SQLs:

    sql_franchiseManage = "select id, address, contact, store_pay \
        from MAINAPP_STORE \
        order by id"

    sql_storeRegister = "insert into MAINAPP_STORE(id, address, contact, store_pay, store_code) \
        values (%s, %s, %s, %s, %s)"

    sql_storeDelete = "delete from MAINAPP_STORE where id = %s"

    sql_storeUpdate = "update MAINAPP_STORE set \
        address = %s, contact = %s, store_pay = %s, store_code = %s \
        where id = %s"

    sql_storeSearch = "select id, address, contact, store_pay \
        from MAINAPP_STORE \
        where address LIKE %s\
        and contact LIKE %s\
        and store_pay between %s and %s\
        order by id"
    sql_storeSearchPage = "select count(id) \
        from MAINAPP_STORE \
        where address LIKE %s\
        and contact LIKE %s\
        and store_pay between %s and %s\
        order by id"
    sql_supplierManage = "select id, name, contact, email \
        from MAINAPP_SUPPLIER \
        order by id"

    sql_supplierRegister = "insert into MAINAPP_SUPPLIER(id, name, contact, email) \
        values (%s, %s, %s, %s)"

    sql_supplierDelete = "delete from MAINAPP_SUPPLIER where id = %s"

    sql_supplierUpdate = "update MAINAPP_SUPPLIER set \
        name = %s, contact = %s, email = %s \
        where id = %s"

    sql_supplierSearch = "select id, name, contact, email \
        from MAINAPP_SUPPLIER \
        where name LIKE %s\
        and contact LIKE %s\
        and email LIKE %s\
        order by id"
    sql_supplierSearchp = "select count(id) \
        from MAINAPP_SUPPLIER \
        where name LIKE %s\
        and contact LIKE %s\
        and email LIKE %s\
        order by id"

    sql_customerManage = "select id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        order by id"

    sql_customerRegister = "insert into MAINAPP_CUSTOMER(id, name, mileage, gender, birthday, contact) \
        values (%s, %s, %s, %s, %s, %s)"

    sql_customerDelete = "delete from MAINAPP_CUSTOMER where id = %s"

    sql_customerUpdate = "update MAINAPP_CUSTOMER set \
        name = %s, mileage = %s, gender = %s, birthday = %s, contact = %s \
        where id = %s"

    sql_customerSearch = "select id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        where name LIKE %s\
        and mileage between %s and %s\
        and gender = %s\
        and birthday between %s and %s\
        and contact LIKE %s\
        order by id"

    sql_customerSearchp = "select count(id) \
        from MAINAPP_CUSTOMER \
        where name LIKE %s\
        and mileage between %s and %s\
        and gender = %s\
        and birthday between %s and %s\
        and contact LIKE %s\
        order by id"

    sql_productManage = "select barcode, name, supply_price, unit_price, supplier_id, \
        category_a, category_b, explain, picture_file_path \
        from MAINAPP_PRODUCT \
        order by barcode"

    sql_productRegister = "insert into MAINAPP_PRODUCT(barcode, name, supply_price, unit_price, supplier_id, \
        category_a, category_b, explain, picture_file_path) \
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    sql_productDelete = "delete from MAINAPP_PRODUCT where barcode = %s"

    sql_productUpdate = "update MAINAPP_product set \
        name = %s, supply_price = %s, unit_price = %s, supplier_id = %s, \
        category_a = %s, category_b = %s, explain = %s, picture_file_path = %s\
        where barcode = %s"

    sql_productSearch = "select barcode, name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path \
        from MAINAPP_PRODUCT \
        where barcode LIKE %s\
        and name LIKE %s\
        and supply_price between %s and %s\
        and unit_price between %s and %s\
        and supplier_id LIKE %s \
        and category_a LIKE %s \
        and category_b LIKE %s \
        order by barcode"
    
    sql_productSearchp = "select count(barcode) \
        from MAINAPP_PRODUCT \
        where barcode LIKE %s\
        and name LIKE %s\
        and supply_price between %s and %s\
        and unit_price between %s and %s\
        and supplier_id LIKE %s \
        and category_a LIKE %s \
        and category_b LIKE %s \
        order by barcode"

    sql_productSearchByBarcode = "select barcode, name, supply_price, unit_price, supplier_id, category_a, category_b, explain, picture_file_path \
        from MAINAPP_PRODUCT \
        where barcode = %s"

    sql_employeeManage = "select id, name, daytime_hourpay, nighttime_hourpay, \
        employed_date, fire_date, contact, position_code \
        from MAINAPP_EMPLOYEE \
        where store_id = %s \
        order by id"

    sql_employeeRegister = "insert into MAINAPP_EMPLOYEE(store_id, name, daytime_hourpay, nighttime_hourpay, \
        employed_date, fire_date, contact, position_code) \
        values (%s, %s, %s, %s, %s, %s, %s, %s)"

    sql_employeeDelete = "delete from MAINAPP_EMPLOYEE where store_id = %s and id = %s"

    sql_employeeUpdate = "update MAINAPP_employee set \
        name = %s, daytime_hourpay = %s, nighttime_hourpay = %s, \
        employed_date = %s, fire_date = %s, contact = %s, position_code = %s \
        where store_id = %s and id = %s"

    sql_expireDateManage = "select id, store_id, display_location_code, st.barcode as barcode, quantity \
        from MAINAPP_STOCK st, MAINAPP_PRODUCT p\
        where store_id = %s and \
        st.barcode = p.barcode and \
        p.category_a in (1, 2) \
        order by st.barcode"

    sql_stockManage = "select id, store_id, display_location_code, barcode, quantity \
        from MAINAPP_STOCK \
        where store_id = %s \
        order by barcode"

    sql_stockRegister = "insert into MAINAPP_STOCK(store_id, display_location_code, barcode, quantity) \
        values (%s, %s, %s, %s)"

    sql_stockDelete = "delete from MAINAPP_STOCK where store_id = %s and id = %s"

    sql_stockUpdate = "update MAINAPP_STOCK set \
        display_location_code = %s, barcode = %s, quantity = %s \
        where store_id = %s and id = %s"
    
    sql_orderManage = "select id, store_id, order_timestamp, complete_timestamp, process_code \
        from MAINAPP_ORDER \
        where store_id = %s \
        order by id desc"

    sql_orderRegister = "insert into MAINAPP_ORDER(store_id, order_timestamp, process_code) \
        values (%s, %s, 0)"

    sql_orderListManage = "select id, barcode, quantity, sent_timestamp, arrival_timestamp, process_code, order_id \
        from MAINAPP_ORDER_LIST \
        where order_id = %s \
        order by id desc"

    sql_orderListRegister = "insert into MAINAPP_ORDER_LIST(barcode, quantity, process_code, order_id) \
        values (%s, %s, 0, %s)"

    sql_orderListDelete = "delete from MAINAPP_ORDER_LIST where id = %s"

    sql_storeRefundManage = "select id, barcode, quantity, refund_timestamp, refund_reason_code, process_code \
        from MAINAPP_STORE_REFUND \
        where store_id = %s \
        order by id desc"

    sql_storeRefundRegister = "insert into MAINAPP_STORE_REFUND(barcode, quantity, refund_timestamp, refund_reason_code, process_code, store_id) \
        values (%s, %s, %s, %s, 0, %s)"

    sql_storeRefundDelete = "delete from MAINAPP_STORE_REFUND where id = %s"

    sql_customerRefundManage = "select id, refund_timestamp, refund_reason_code, trade_list_id \
        from MAINAPP_CUSTOMER_REFUND \
        where id = %s \
        order by id desc"

    sql_customerRefundRegister = "insert into MAINAPP_CUSTOMER_REFUND(refund_timestamp, refund_reason_code, trade_list_id) \
        values (%s, %s, %s)"
    
    sql_tradelistRefundMark = "update MAINAPP_TRADE_LIST set IS_REFUND = 'Y' where id = %s"

    sql_customerRefundDelete = "delete from MAINAPP_CUSTOMER_REFUND where id = %s"

    sql_workListManage = "select wl.id as id, workstart_timestamp, workend_timestamp, storeowner_check, wl.employee_id as employee_id \
        from MAINAPP_WORK_LIST wl, MAINAPP_EMPLOYEE emp \
        where wl.employee_id = emp.id and emp.store_id = %s \
        order by wl.id desc"

    sql_workListRegister = "insert into MAINAPP_WORK_LIST(employee_id, workstart_timestamp, workend_timestamp, storeowner_check) \
        values (%s, %s, %s, 'N')"

    sql_workListDelete = "delete from MAINAPP_WORK_LIST where id = %s"

    sql_workListConfirm = "update MAINAPP_WORK_LIST set STOREOWNER_CHECK = 'Y' where id = %s"

    sql_workListQueryForSalary = "select id, workstart_timestamp, workend_timestamp \
        from MAINAPP_WORK_LIST \
        where employee_id = %s and workstart_timestamp >= %s and workend_timestamp <= %s \
        order by id"

    sql_maintenanceCostManage = "select id, maintenance_cost_code, amount, process_date, employee_id, etc, storeowner_check, store_id \
        from MAINAPP_MAINTENANCE_COST \
        where store_id = %s \
        order by id desc"

    sql_maintenanceCostRegister = "insert into MAINAPP_MAINTENANCE_COST(maintenance_cost_code, amount, process_date, employee_id, etc, storeowner_check, store_id) \
        values (%s, %s, %s, %s, %s, 'N', %s)"

    sql_maintenanceCostDelete = "delete from MAINAPP_MAINTENANCE_COST where id = %s"

    sql_saleProductManage = "select id, trade_timestamp, employee_id, customer_id, payment_method_code, payment_information, store_id \
        from MAINAPP_RECEIPT \
        where store_id = %s \
        order by id desc"

    sql_receiptRegister = "insert into MAINAPP_RECEIPT(TRADE_TIMESTAMP, EMPLOYEE_ID, CUSTOMER_ID, \
        PAYMENT_METHOD_CODE, PAYMENT_INFORMATION, STORE_ID) \
        values (%s, %s, %s, %s, %s, %s)"

    sql_tradeListManage = "select id, barcode, quantity, is_refund, receipt_id \
        from MAINAPP_TRADE_LIST \
        where receipt_id = %s \
        order by id"
    
    #영수증 등록하기전에 충분한 재고의 갯수를 리턴
    sql_tradeListRegisterCheck = "select quantity from MAINAPP_STOCK \
        where BARCODE = %s and store_id = %s \
        order by quantity desc"

    #영수증 등록 후 재고에서 뺌
    sql_tradeListMinusStock = 'update mainapp_stock set \
        quantity = quantity - %s where barcode = %s and store_id = %s'

    sql_tradeListRegister = "insert into MAINAPP_TRADE_LIST(BARCODE, QUANTITY, IS_REFUND, RECEIPT_ID) \
        values (%s, %s, 'N', %s)"

    sql_franchiseStoreRcptManage = "select id, store_id, rcpt_date, rcpt_amount\
        from MAINAPP_FRANCHISE_STORE_RCPT \
        order by rcpt_date desc"

    sql_franchiseStoreRcptRegister = "insert into MAINAPP_FRANCHISE_STORE_RCPT(store_id, rcpt_date, rcpt_amount) \
        values (%s, %s, %s)"

    sql_franchiseStoreRcptDelete = "delete from MAINAPP_FRANCHISE_STORE_RCPT where id = %s"

    sql_franchiseStoreRcptUpdate = "update MAINAPP_FRANCHISE_STORE_RCPT set \
        rcpt_date = %s, rcpt_amount = %s, store_id = %s \
        where id = %s"
    
    sql_storeOrderManage = "select id, store_id, order_timestamp, complete_timestamp, process_code \
        from MAINAPP_ORDER \
        order by order_timestamp"
    
    sql_storeOrderUpdate = "update MAINAPP_ORDER set \
        store_id = %s, order_timestamp = %s, complete_timestamp = %s, process_code = %s \
        where id = %s"
    
    sql_centralStoreRefundManage = 'select id, store_id, barcode, quantity, refund_timestamp, \
        refund_reason_code, process_code\
        from MAINAPP_STORE_REFUND\
        order by store_id'
    sql_centralStoreRefundUpdate = 'update MAINAPP_STORE_REFUND set\
        store_id = %s, barcode = %s, refund_timestamp = %s, refund_reason_code = %s, \
        process_code = %s \
        where id = %s'
    
    sql_storeOrderTotalPrice = 'select sum(b.quantity*p.unit_price) \
        from mainapp_order a, mainapp_order_list b, mainapp_product p \
        where a.id=b.order_id and b.barcode=p.barcode\
        and a.id=%s '
    
    sql_storeOrderListManage = 'select id, barcode, quantity, sent_timestamp, arrival_timestamp, \
        process_code, order_id \
        from mainapp_order_list \
        where order_id=%s '

    sql_storeOrderListUpdate = "update mainapp_order_list set\
        sent_timestamp=%s, arrival_timestamp=%s, process_code=%s \
        where id=%s"
    
    sql_userRegister = 'insert into mainapp_user(user_id, password, store_id, emp_pos_code) \
        values (%s, %s, %s, %s)'

    sql_userIdGetter = 'select id, password, store_id, emp_pos_code \
        from mainapp_user \
        where user_id=%s'

    sql_customerMileageAdd = 'update mainapp_customer set \
        mileage = mileage + %s where id=%s '
        
    sql_salesMonthlyGroup = '''
    select to_char(trade_timestamp,'YYYY-MM') as dat
    from mainapp_receipt
    where store_id=%s
    group by to_char(trade_timestamp,'YYYY-MM')
    '''

    sql_salesMonthlyGet = '''
    select  sum(p.unit_price*a.quantity) 
    from mainapp_trade_list a, mainapp_product p
    where a.receipt_id in 
    (select id from mainapp_receipt where to_char(trade_timestamp, 'YYYY-MM') = %s and store_id=%s )
    and p.barcode=a.barcode
    '''