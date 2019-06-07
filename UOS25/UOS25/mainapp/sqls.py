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

    sql_CustomerRegister = "insert into MAINAPP_CUSTOMER(customer_id, name, mileage, gender, birthday, contact) \
        values (%s, %s, %s, %s, %s, %s)"

    sql_CustomerManage = "select customer_id, name, mileage, gender, birthday, contact \
        from MAINAPP_CUSTOMER \
        order by customer_id"

    sql_CustomerDelete = "delete from MAINAPP_CUSTOMER where customer_id = %s"
