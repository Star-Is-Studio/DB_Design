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

    sql_storeCount = "select count(id) from MAINAPP_STORE"

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