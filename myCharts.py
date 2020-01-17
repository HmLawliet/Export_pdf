from pyecharts import options as opts
from pyecharts.charts import Bar,Page, WordCloud,Line,Tree,Geo,Grid,Scatter,Pie,Calendar
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType, SymbolType
import json
import os
from os import listdir
from PIL import Image
import datetime


class MyCharts:

    def __init__(self):
        self.index = 1

    def genWordCloud(self,words=None,title='示例'):
        '''
        词云
        应用场景 关键词显示
        '''
        words = words or [
            ("Sam S Club", 10000),
            ("Macys", 6181),
            ("Amy Schumer", 4386),
            ("Jurassic World", 4055),
            ("Charter Communications", 2467),
            ("Chick Fil A", 2244),
            ("Planet Fitness", 1868),
            ("Pitch Perfect", 1484),
            ("Express", 1112),
            ("Home", 865),
            ("Johnny Depp", 847),
            ("Lena Dunham", 582),
            ("Lewis Hamilton", 555),
            ("KXAN", 550),
            ("Mary Ellen Mark", 462),
            ("Farrah Abraham", 366),
            ("Rita Ora", 360),
            ("Serena Williams", 282),
            ("NCAA baseball tournament", 273),
            ("Point Break", 265),
        ]
        c = (
            WordCloud()
            .add("", words, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        chart_name = f'static/chart{self.index}_wordcloud'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1

    def genBarReversalAxis(self,x_list=None,y_orderdicts=None,title='柱形示例'):
        '''
        横向柱状图
        应用场景 ： 省份排行
        '''
        x_list = x_list or Faker.choose()
        y_orderdicts = y_orderdicts or { i:Faker.values() for i in range(1,3)} 
        c = (
            Bar()
            .add_xaxis(x_list)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        for key,value in y_orderdicts.items():
            c.add_yaxis(key, value)
        chart_name = f'static/chart{self.index}_bar'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1

    def genLine(self,x_list=None,y_orderdicts=None,title='线形示例',subtitle='副标题示例',is_smooth=True,average = None):
        '''
        折线图  平滑曲线
        应用场景 趋势图
        param x_list x轴的值   type  list
        param y_dicts key是类别，value是y轴的值  type orderdict
        param title 图表的题目    type  str
        param is_smooth 是否平滑   默认是  type bool 
        param average 平均数的基准标记线  type number 
        '''
        x_list = x_list or Faker.choose()
        y_orderdicts = y_orderdicts or {i: Faker.values() for i in range(1, 3)}
        c = (
            Line()
            .add_xaxis(x_list)
            .set_global_opts(title_opts=opts.TitleOpts(title=title,subtitle =subtitle))
        )
        for key, value in y_orderdicts.items():
            if average:
                # c.add_yaxis(key, value,is_smooth=True,markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]))
                c.add_yaxis(key, value,is_smooth=True,markline_opts=opts.MarkLineOpts(data=average))
            else:
                c.add_yaxis(key, value,is_smooth=True)
        chart_name = f'static/chart{self.index}_line'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1


    def genTreeLayout(self,json,title='树形示例'):
        '''
        结点之间的关系图title
        '''
        c = (
            Tree()
            .add("", [json], collapse_interval=2, layout="radial")
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        chart_name = f'static/chart{self.index}_tree'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1


    def geoHeatMap(self,area=None,data=None,maptype='china',title='热力图示例',subtitle='副标题'):
        '''
        热力图
        param area: 省份的列表   type list  例如 ['吉林', '辽宁', '河北', '河南']
        param data: 对应的值     type list  例如 [63,10,2,30]
        应用场景  省份或者城市排行榜
        # ['黑龙江', '吉林', '辽宁', '河北', '河南', '山东', '山西', '安徽', '江西', '江苏', '浙江', '福建', '台湾', '广东',
        # '湖南', '湖北', '海南', '云南', '贵州', '四川', '青海', '甘肃', '陕西', '内蒙古', '新疆', '广西', '宁夏', '西藏',
        # '北京','天津','上海','重庆','香港','澳门']
        '''
        area = area or Faker.provinces
        data = data or Faker.values()
        c = (
            Geo()
            .add_schema(maptype=maptype)
            .add(
                "geo",
                [list(z) for z in zip(area, data)],
                type_=ChartType.HEATMAP,
            )
            # .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(),
                title_opts=opts.TitleOpts(title=title,subtitle=subtitle),
            )
        )
        chart_name = f'static/chart{self.index}_heatmap'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1

    def genMultiPie(self, left_x_list=None,left_y_list=None, right_x_list=None, right_y_list=None, title='多玫瑰示例'):
        '''
        多个玫瑰图
        param left_x_list 标注 type list
        param right_x_list 标注 type list
        datas 
        '''  
        
        left_x_list = left_x_list or Faker.choose()
        left_y_list = left_y_list or Faker.values()
        right_x_list = right_x_list or Faker.choose()
        right_y_list = right_y_list or Faker.values()
        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(left_x_list, left_y_list)],
                radius=["30%", "75%"],
                center=["25%", "50%"],
                rosetype="radius",
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add(
                "",
                [list(z) for z in zip(right_x_list, right_y_list)],
                radius=["30%", "75%"],
                center=["75%", "50%"],
                rosetype="area",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-玫瑰图示例"))
        )
        chart_name = f'static/chart{self.index}_multipie'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1

    def genPie(self,headlines=None,datas=None,title='玫瑰示例'):
        '''
        玫瑰图
        param headline 标注  type list 
        param data 详细数据 type list
        '''
        headlines = headlines or Faker.choose()
        datas = datas or Faker.values()
        c = (
            Pie()
            .add(
                "",
                [list(z) for z in zip(headlines, datas)],
                radius=["30%", "75%"],
                center=["75%", "50%"],
                rosetype="area",
            )
            .set_global_opts(title_opts=opts.TitleOpts(title=title))
        )
        chart_name = f'static/chart{self.index}_pie'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1

    def genCalendar(self,data = None, year='2017',title='Calendar示例',subtitle =''):
        '''
        日历表
        param year 指定的年的日历
        param data 日期和统计的数量 [('2020-01-01',300),('2020-01-02',200)]
        '''
        if not data:
            import random
            begin = datetime.date(2017, 1, 1)
            end = datetime.date(2017, 12, 31)
            data = [
                [str(begin + datetime.timedelta(days=i)), random.randint(1000, 25000)]
                for i in range((end - begin).days + 1)
            ] 
        c = (
            Calendar()
            .add("", data, calendar_opts=opts.CalendarOpts(range_=year))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=title,subtitle=subtitle),
                visualmap_opts=opts.VisualMapOpts(
                    max_=10000,
                    min_=0,
                    orient="horizontal",
                    is_piecewise=True,
                    pos_top="230px",
                    pos_left="100px",
                ),
            )
        )
        c.render()
        chart_name = f'static/chart{self.index}_calendar'
        make_snapshot(snapshot,c.render(f'{chart_name}.html'),f'{chart_name}.png',is_remove_html=True)
        self.index += 1




def genLongImage():
    imgs = [Image.open(f'static/{fn}') for fn in listdir(path='static/') if fn.endswith('.png')]
    width, height = imgs[0].size
    result = Image.new(imgs[0].mode, (width, height * len(imgs)))
    for index, img in enumerate(imgs):
        result.paste(img, box=(0, index * height))
    result.save('result.png')



if __name__ == '__main__':
    pass
    c = MyCharts()
    c.genCalendar()
    # c.genBarReversalAxis()
    # c.genLine()
    # c.genWordCloud()
    # c.genPie()
    # c.geoHeatMap()
    # genLongImage()

