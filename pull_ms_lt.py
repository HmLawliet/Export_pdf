import pymysql
from collections import namedtuple
import pandas as pd
import numpy as np



Mysql = namedtuple('Mysql', 'host,user,passwd,db')
m_p = Mysql('******************','******************','******************','******************')


class PandasMySql(object):
    
    def __init__(self, host=m_p.host, user=m_p.user, passwd=m_p.passwd, db=m_p.db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def __enter__(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user, password=self.passwd,
                                    db=self.db, charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


SQL_DICT = {
    'ordred':'select DAYOFYEAR(create_time) as date_index,count(distinct label_code) as count from statistics_ordred where org_id = 324 group by date_index order by date_index;',
    # 'delivery':''
    'distributor':'select * from ac_distributor '
}


def query(sql):
    try:
        with PandasMySql() as pm:
            cur = pm.cursor
            cur.execute(sql)
            result = cur.fetchall()
            return result
    except Exception:
        return ()

if __name__ == "__main__":
    df = query(SQL_DICT['distributor'])
    print(df)