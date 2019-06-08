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

    sql_workListManage = "select wl.id as id, workstart_timestamp, workend_timestamp, storeowner_check, wl.employee_id as employee_id \
        from MAINAPP_WORK_LIST wl, MAINAPP_EMPLOYEE emp \
        where wl.employee_id = emp.id and emp.store_id = %s \
        order by wl.id desc"

    sql_workListRegister = "insert into MAINAPP_WORK_LIST(employee_id, workstart_timestamp, workend_timestamp, storeowner_check) \
        values (%s, %s, %s, 'N')"

    sql_workListDelete = "delete from MAINAPP_WORK_LIST where id = %s"

    sql_userGetPosition = "select position_code from mainapp_employee where id=%s;"