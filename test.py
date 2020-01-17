from pyecharts import options as opts
from pyecharts.charts import Bar,Page, WordCloud,Line,Tree,Geo,Grid,Scatter,Pie
from pyecharts.render import make_snapshot
from snapshot_phantomjs import snapshot
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType, SymbolType
import json
import os


def bar_base():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c



def bar_border_radius():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), category_gap="60%")
        .set_series_opts(itemstyle_opts={
            "normal": {
                "color": JsCode("""new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(0, 244, 255, 1)'
                }, {
                    offset: 1,
                    color: 'rgba(0, 77, 167, 1)'
                }], false)"""),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": 'rgb(0, 160, 221)',
            }})
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-渐变圆柱"))
    )
    return c

def bar_base_with_animation():
    c = (
        Bar(
            init_opts=opts.InitOpts(
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="elasticOut"
                )
            )
        )
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-动画配置基本示例", subtitle="我是副标题")
        )
    )
    return c


def bar_is_selected():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values(), is_selected=False)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-默认取消显示某 Series"))
    )
    return c


def bar_same_series_gap():
    c = (
        Bar()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), category_gap="80%")
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-单系列柱间距离"))
    )
    return c


def line_base():
    c = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
    )
    return c


def line_smooth():
    c = (
        Line()
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values(), is_smooth=True)
        .add_yaxis("商家B", Faker.values(), is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Line-smooth"))
    )
    
    return c



if __name__ == "__main__":
    # page = Page()
    # charts = [bar_base(),bar_border_radius(),bar_base_with_animation(),bar_is_selected(),bar_is_selected(),bar_same_series_gap(),line_base(),line_smooth()]
    
    # for index,chart in enumerate(charts):
    #     page.add(chart)
    #     make_snapshot(snapshot, page.render(), f'static/tmp{index}.png')
    
    from os import listdir
    from PIL import Image

    imgs = [Image.open(f'static/{fn}') for fn in listdir(path='static/') if fn.endswith('.png')]
    width, height = imgs[0].size
    result = Image.new(imgs[0].mode, (width, height * len(imgs)))
    for index, img in enumerate(imgs):
        result.paste(img, box=(0, index * height))
    result.save('result.png')