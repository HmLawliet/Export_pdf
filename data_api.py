import numpy as np
import pandas as pd
from pull_ms_lt import query as qt
from pull_dw_df import execute as qd
from collections import OrderedDict
import os
from itertools import zip_longest

def scan():
    df = pd.read_csv('scan.csv')
    return df

def antifake():
    df = pd.read_csv('antifake.csv')
    return df

def distributor():
    df = pd.read_csv('distributor.csv')
    return df

def sales():
    df = pd.read_csv('sale.csv')
    return df 

# def test(org_id):
#     scan_df = scan()
#     scan_df.gmt_create = scan_df.gmt_create.str[:7]
#     scan_df = scan_df[['gmt_create', 'org_id']].groupby(['gmt_create', 'org_id']).size().reset_index(name='counts')
#     antifake_df = antifake()
#     antifake_df.gmt_create = antifake_df.gmt_create.str[:7]
#     antifake_df = antifake_df[['gmt_create', 'org_id']].groupby(['gmt_create', 'org_id']).size().reset_index(name='counts')
#     scan_df.show()

def getSaleCSV(start_time,end_time):
    sql = f'SELECT * FROM  dwd_sale_record WHERE  gmt_create >= "{start_time} 00:00:00" AND gmt_create < "{end_time} 00:00:00" '
    df = qd(sql)
    df.to_csv('csv/sale.csv', index=False)
    return df


def getProvince(prov_list):
    res_list = []
    for item in prov_list:
        if '特别行政区' in item:
            res_list.append(item.strip().replace('特别行政区', ''))
            continue
        if '维吾尔自治区' in item:
            res_list.append(item.strip().replace('维吾尔自治区', ''))
            continue
        if '回族自治区' in item:
            res_list.append(item.strip().replace('回族自治区', ''))
            continue
        if '壮族自治区' in item:
            res_list.append(item.strip().replace('壮族自治区', ''))
            continue
        if '自治区' in item:
            res_list.append(item.strip().replace('自治区', ''))
            continue
        if '省' in item:
            res_list.append(item.strip().replace('省', ''))
            continue
        if '市' in item:
            res_list.append(item.strip().replace('市', ''))
            continue
    return res_list



def api_1_newAddDistributorByMonth(org_id=121,start_time="2019-01-01",end_time="2020-01-01"):
    '''
    公司总的经销商数量
    公司2019年新增的经销商数  每月增数量
    Line图显示每月新增经销商
    '''
    sql = f'select count(1) as count  from ac_distributor where status = 1 and org_id ={org_id};'
    dist_sum = qt(sql)
    if dist_sum:
        dist_sum = dist_sum[0][0]
    else:
        dist_sum = 0
    sql = f'select DATE_FORMAT(gmt_create,"%Y-%m") create_time,count(1) as count from ac_distributor where status=1 and org_id = 121 and gmt_create >= "{start_time}" and gmt_create < "{end_time}" group by create_time;'
    dist_incr = qt(sql)
    incr_sum = 0
    for item in dist_incr:
        incr_sum += item[1]
    # 该公司经销商总数, 该公司今年新增经销商, 该公司每月的新增经销商数
    x_list = []
    y_orderdict = OrderedDict()
    y_orderdict['经销商'] = []
    for item in dist_incr:
        x_list.append(item[0])
        y_orderdict['经销商'].append(item[1]) 
    return dist_sum,incr_sum,x_list,y_orderdict


def api_2_newAddDistributorSaleTop5(org_id=121,start_time='2019-01-01',end_time='2020-01-01'):
    '''
    公司销售top5经销商, 以及新增经销商top5
    饼图显示 全部前五,新增前五
    '''
    sql = f'select id from ac_distributor where status=1 and org_id = {org_id} and gmt_create >= "{start_time}" and gmt_create < "{end_time}";'
    dist_ids = qt(sql)
    dist_list = []
    if dist_ids:
        dist_list = [item[0] for item in dist_ids]
    if not os.path.isfile('csv/sale.csv'): 
        df_org = getSaleCSV(start_time, end_time)
    else:
        df_org = pd.read_csv('csv/sale.csv', low_memory=False)

    df_org = df_org[df_org['org_id'] == org_id]
    df = df_org[['sell_distributor_name']].groupby(['sell_distributor_name']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    df = df.drop(df[df['sell_distributor_name'] == ''].index).iloc[:5,:]
    left_x_list = df['sell_distributor_name'].tolist()
    left_y_list = df['counts'].tolist()

    df = df_org[df_org['sell_distributor_id'].isin(dist_list)]
    df = df[['sell_distributor_name']].groupby(['sell_distributor_name']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    df = df.drop(df[df['sell_distributor_name'] == ''].index).iloc[:5,:]
    right_x_list = df['sell_distributor_name'].tolist()
    right_y_list = df['counts'].tolist()
    return left_x_list,left_y_list,right_x_list,right_y_list


def api_3_saleNumByDay(org_id=121,start_time='2019-01-01',end_time='2020-01-01'):
    '''
    公司销售数量  日历统计
    日历图显示
    '''
    if not os.path.isfile('csv/sale.csv'): 
        df_org = getSaleCSV(start_time, end_time)
    else:
        df_org = pd.read_csv('csv/sale.csv', low_memory=False)
    df_org = df_org[df_org['org_id'] == org_id]
    df_org['gmt_create'] = df_org.gmt_create.str[:10]
    df = df_org[['gmt_create']].groupby(['gmt_create']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)
    item0 = df['gmt_create'].tolist()
    item1 = df['counts'].tolist()
    result_list = []
    sum_num = sum(item1) 
    for item in zip_longest(item0, item1):
        result_list.append(item)
    if result_list:
        result_list = sorted(result_list, key=lambda x: x[1], reverse=True)
    # 返回的列表   生成年份    题目    一年销量
    return result_list, '2019', '2019年度销量情况',sum_num

def api_4_productTopTen(org_id=121,start_time='2019-01-01',end_time='2020-01-01'):
    '''
    销售火爆的产品  top10
    词云图来表示
    '''
    if not os.path.isfile('csv/sale.csv'): 
        df_org = getSaleCSV(start_time, end_time)
    else:
        df_org = pd.read_csv('csv/sale.csv', low_memory=False)
    df_org = df_org[df_org['org_id'] == org_id]
    df = df_org[["product_name"]].groupby(["product_name"]).size().reset_index(name="counts").sort_values(by="counts", ascending=False)
    item0 = df['product_name'].tolist()[:10]
    item1 = df['counts'].tolist()[:10]
    result_list = []
    for item in zip_longest(item0,item1):
        result_list.append(item)    
    return result_list, '2019年度畅销产品'
    
def api_5_areaHeatMap(org_id=121, start_time='2019-01-01', end_time='2020-01-01'):
    '''
    销售省份热度图  以及 销售城市top10 
    热度图  以及  横行柱状图表示
    '''
    if not os.path.isfile('csv/sale.csv'): 
        df_org = getSaleCSV(start_time, end_time)
    else:
        df_org = pd.read_csv('csv/sale.csv', low_memory=False)
    df_org = df_org[df_org['org_id'] == org_id]
    df = df_org[["province_name"]].groupby(["province_name"]).size().reset_index(name="counts").sort_values(by="counts", ascending=False)
    df = df.drop(df[df['province_name'] == ''].index)
    p_item0 = df['province_name'].tolist()
    p_item0 = getProvince(p_item0)
    p_item1 = df['counts'].tolist()

    df = df_org[["city_name"]].groupby(["city_name"]).size().reset_index(name="counts").sort_values(by="counts", ascending=False)
    df = df.drop(df[df['city_name'] == ''].index).iloc[:10,:]
    c_item0 = df['city_name'].tolist()
    c_item0.reverse()
    c_item1 = df['counts'].tolist()
    c_item1.reverse()
    city_dict = OrderedDict({'城市':c_item1})
    # 省份  销量   前五省
    return p_item0,p_item1,p_item0[:5],c_item0,city_dict



def api_6_scan(org_id=121, start_time='2019-01-01', end_time='2020-01-01'):
    '''
    扫描用户
    '''
    pass 





if __name__ == "__main__":
    # 基于事实 扫描  验伪  营销活动  质保卡 
    from myCharts import MyCharts,genLongImage
    
    # c = MyCharts()

    # data = api_1_newAddDistributorByMonth()
    # c.genLine(data[2],data[3],title='经销商统计',subtitle=f'经销商总数:{data[0]},其中2019年新增经销商{data[1]}')

    # data = api_2_newAddDistributorSaleTop5()
    # c.genMultiPie(data[0],data[1],data[2],data[3],title='2019年Top5销量王')

    # data = api_3_saleNumByDay()
    # c.genCalendar(data[0],year=data[1],title =data[2],subtitle =f'销量总数:{data[3]}' )

    # data = api_4_productTopTen()
    # c.genWordCloud(data[0],title =data[1])
    
    # data = api_5_areaHeatMap()
    # c.geoHeatMap(data[0], data[1], title='销售省份热力图', subtitle=f'销量排行前五的省份:{data[2]}')
    # c.genBarReversalAxis(data[3],data[4],title='销售城市Top10')

    genLongImage()
    pass 