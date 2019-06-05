from mainapp.models import *

def query_all(model):
    sql = 'select * from {}'
    table_name = model._meta.db_table
    return model.objects.raw(sql.format(table_name))

def query_pk(model, pk, pk_name='id'):
    sql = 'select * from {} where {}={}'
    table_name = model._meta.db_table
    return model.objects.raw(
        sql.format(table_name, pk_name, pk)
    )