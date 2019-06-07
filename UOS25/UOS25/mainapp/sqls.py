# SQL Statements.

class SQLs:

    sql_franchiseManage = "select store_id, address, contact, store_pay \
        from MAINAPP_STORE \
        order by store_id"

    sql_storeRegister = "insert into MAINAPP_STORE(store_id, address, contact, store_pay, store_code) \
        values (%s, %s, %s, %s, %s)"

    sql_storeDelete = "delete from MAINAPP_STORE where store_id = %s"

    sql_storeUpdate = "update MAINAPP_STORE set \
        address = %s, contact = %s, store_pay = %s, store_code = %s \
        where store_id = %s"

    sql_storeSearch = "select store_id, address, contact, store_pay \
        from MAINAPP_STORE \
        where address LIKE %s\
        and contact LIKE %s\
        and store_pay >= %s\
        and store_pay <= %s\
        order by store_id"

    sql_supplierManage = "select supplier_id, name, contact, email \
        from MAINAPP_SUPPLIER \
        order by supplier_id"

    sql_supplierRegister = "insert into MAINAPP_SUPPLIER(supplier_id, name, contact, email) \
        values (%s, %s, %s, %s)"

    sql_supplierDelete = "delete from MAINAPP_SUPPLIER where supplier_id = %s"

    sql_supplierUpdate = "update MAINAPP_SUPPLIER set \
        name = %s, contact = %s, email = %s \
        where supplier_id = %s"

    sql_supplierSearch = "select supplier_id, name, contact, email \
        from MAINAPP_SUPPLIER \
        where name LIKE %s\
        and contact LIKE %s\
        and email LIKE %s\
        order by supplier_id"

    sql_customerManage = "select customer_id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        order by customer_id"

    sql_customerRegister = "insert into MAINAPP_CUSTOMER(customer_id, name, mileage, gender, birthday, contact) \
        values (%s, %s, %s, %s, %s, %s)"

    sql_customerDelete = "delete from MAINAPP_CUSTOMER where customer_id = %s"

    sql_customerUpdate = "update MAINAPP_CUSTOMER set \
        name = %s, mileage = %s, gender = %s, birthday = %s, contact = %s \
        where customer_id = %s"

    sql_customerSearch = "select customer_id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        where name LIKE %s\
        and mileage between %s and %s\
        and gender = %s\
        and birthday between %s and %s\
        and contact LIKE %s\
        order by customer_id"