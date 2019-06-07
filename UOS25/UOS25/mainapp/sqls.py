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

    sql_CustomerRegister = "insert into MAINAPP_CUSTOMER(id, name, mileage, gender, birthday, contact) \
        values (%s, %s, %s, %s, %s, %s)"

    sql_CustomerManage = "select id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        order by id"

    sql_CustomerDelete = "delete from MAINAPP_CUSTOMER where id = %s"
