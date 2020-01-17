'''
执行从dataworks拉取数据保存至配置的本地文件中
'''
from odps import ODPS
import numpy as np
import pandas as pd
from functools import wraps
import logging
from collections import namedtuple


logging.basicConfig(level=logging.INFO)


class Config:
    ORG_TUPLE = (324,407,352,257,39,51,364,328,169,342,130,177,380,267,348,386,293,374,376,121,119)
    START_TIME = '2019-01-01 00:00:00'
    END_TIME = '2020-01-01 00:00:00'
    # 连接 DataStudio 的id,key与项目
    DATA_STUDIO = namedtuple('DATA_STUDIO', 'access_id,secret_access_key,project')
    # 正式dataworks的连接值
    ODPS_COMMON = DATA_STUDIO(
        '******************', '******************', '******************')
    CONNECT_DICT = {}
    QUERY_CONFIG = {
        'scan': f'select * from dwd_scan_log where org_id in {ORG_TUPLE} and gmt_create >= "{START_TIME}" and gmt_create < "{END_TIME}"',
        'antifake': f'select * from dwd_antifake_log where org_id in {ORG_TUPLE} and gmt_create >= "{START_TIME}" and gmt_create < "{END_TIME}"'
        
    }


# 异常捕获的装饰器
def get_Exception(func):
    '''捕获异常'''
    @wraps(func)
    def inner(*args, **kwargs):
        res = pd.DataFrame()
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            logging.warning(e)
        return res
    return inner


# 实例化odps对象
@get_Exception
def connect(access_id=Config.ODPS_COMMON.access_id,
                      secret_access_key=Config.ODPS_COMMON.secret_access_key, project=Config.ODPS_COMMON.project):
    '''
    实例化odps并返回该对象
    param access_id : 连接 datastudio的id   type : str
    param secret_access_key : 连接 datastudio的key  type : str
    param project : 选择的项目名称    type : str
    '''
    if not 'odps' in Config.CONNECT_DICT.keys():
        Config.CONNECT_DICT['odps'] = ODPS(access_id, secret_access_key, project)
    return Config.CONNECT_DICT['odps']


@get_Exception
def get_result(odps, sql):
    '''从dataworks 上读取数据并写入文件
    param odps : dataworks instance 对象
    param sql : 执行的sql
    '''
    instance = odps.execute_sql(sql)
    with instance.open_reader() as reader:
        df = reader.to_pandas()
        return df

# 执行sql
@get_Exception
def execute(sql):
    '''
    单表查询
    param sql : 执行的sql  type : str
    '''
    odps = connect()
    return get_result(odps,sql)



if __name__ == '__main__':
    # df = execute('scan')
    # df.to_csv('scan.csv',index=False)
    # df = execute('antifake')
    # df.to_csv('antifake.csv',index=False)

    df = execute('scan')
    df.to_csv('scan.csv', index=False)
    




