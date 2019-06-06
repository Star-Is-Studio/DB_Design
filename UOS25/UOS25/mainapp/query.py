from mainapp.models import *
from django.db import connection


def _sql_convert(obj):
    sql_type_convert = {
        str: lambda x : "'{}'".format(x),
        int: lambda x : str(x),
        float: lambda x : str(x),
    }
    return sql_type_convert[ type(obj) ](obj)

def query_all(model):
    sql = 'select * from {}'
    table_name = model._meta.db_table
    return list(model.objects.raw(sql.format(table_name)) )

def query_pk(model, pk, pk_name='id'):
    sql = 'select * from {} where {}={}'
    table_name = model._meta.db_table
    dat = model.objects.raw(
        list(sql.format(table_name, pk_name, _sql_convert(pk)))
    )
    return None if len(dat)!=0 else dat[0]

def query_insert(model, data : dict):
    '''
    data : 딕셔너리
        key:필드이름, value:필드값
    '''
    sql_base = 'insert into {}({}) values ({})'
    table_name = model._meta.db_table
    keys = list(data.keys())
    fields_str = ",".join(keys)
    fields_value_str = ",".join([ _sql_convert(data[k]) for k in keys])
    sql = sql_base.format(table_name, fields_str, fields_value_str)
    with connection.cursor() as cur:
        cur.execute(sql)
