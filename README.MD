
# 所依赖的库

pip install pyecharts
pip install numpy
pip install pandas 
pip install snapshot_phantomjs
pip install pymysql
pip install pillow


# 文件说明

csv文件夹 存放csv的数据

static   存放图片

data_api.py  是需要根据实际数据调整的，定制化文件

myCharts.py  图表型的文件 里面有详细传入参数的说明

pull_dw_df.py  拉取阿里云dataworks上的数据  返回的是dataframe的数据类型

pull_ms_df.py  拉取mysql的数据，返回的是dataframe的数据类型

pull_ms_lt.py  拉取mysql的数据，返回的是元组或者列表

render.html 文件是生成图片的临时文件是用来转换图片的  可以删除 

result.png 是结果图片

tempCodeRunnerFile.py  运行pyecharts生成图片的临时文件，可以不用管

test.py   临时验证测试的文件
