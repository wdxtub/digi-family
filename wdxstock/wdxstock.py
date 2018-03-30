import click
import stock_utils as su
import os_utils as ou


@click.group()
@click.version_option()
def cli():
    """wdxstock
    来自 wdx 的股票分析工具包，感谢无师对我的大力支持
    """

# ============== spider Group =================
@cli.group()
def spider():
    """管理数据抓取的相关内容"""

@spider.command("stock-list")
@click.option('--output', '-o', default='./data',
              help='输出路径，默认为 data/')
def get_stock_list(output):
    """获取 A 股的股票列表及对应详情"""
    ou.check_ret(su.get_stock_list(ou.check_path(output)))

@spider.command("price-daily")
@click.option('--list_file', '-l', default='./data/stock_basics.csv',
              help='A股股票基本信息列表，默认为 ./data/stock_basics.csv')
@click.option('--output', '-o', default='./data/history',
              help='输出路径，默认为 data/history')
def daily(list_file, output):
    """获取 A 股的股票列表及对应详情"""
    intervals = ["5", "15", "30", "60"]
    for i in intervals:
        ou.check_ret(su.daily_crawler(i, list_file, ou.check_path(output)))

@spider.command("price-history")
@click.argument('code')
@click.option('--output', '-o', default='./data',
              help='输出路径，默认为 data/')
@click.option('--interval', default='D',
              help='数据的时间间隔，默认为天(D)，其他选项有 W(周) M(月) 5/15/30/60(分钟)')
def get_history_data(code, interval, output):
    """获取指定股票指定时间间隔的股价数据"""
    ou.check_ret(su.get_history_data(code, interval, ou.check_path(output)))

@spider.command("all-price-history")
@click.option('--list_file', '-l', default='./data/stock_basics.csv',
              help='A股股票基本信息列表，默认为 ./data/stock_basics.csv')
@click.option('--output', '-o', default='./data/history',
              help='输出路径，默认为 data/history')
@click.option('--interval', default='D',
              help='数据的时间间隔，默认为天(D)，其他选项有 W(周) M(月) 5/15/30/60(分钟)')
def get_all_history(list_file, interval, output):
    """获取指定时间间隔的全部股价数据"""
    ou.check_file(list_file, "请先使用 stock-list 命令来获取")
    # 读取默认输出文件夹中的 stock_basics.csv 来获取股票列表
    ou.check_ret(su.get_all_history_data(interval, list_file, ou.check_path(output)))


@spider.command("fundamental-data")
@click.option('--output_dir', '-o', default='./data/fundamental',
              help='输出路径，默认为 data/fundamental')
def fundamental_data(output_dir):
    """获取基本面数据"""
    ou.check_ret(su.get_fundamental_data(
        ou.check_path(output_dir)))

@spider.command("macro-enco-data")
@click.option('--output_dir', '-o', default='./data/macro',
              help='输出路径，默认为 data/macro')
def macro_enco_data(output_dir):
    """获取宏观经济数据"""
    ou.check_ret(su.get_macro_enco_data(
        ou.check_path(output_dir)))

# ============== analysis Group =================

@cli.group()
def analysis():
    """股票数据分析的相关操作"""

@analysis.command("keyword-cluster")
@click.option('--input_dir', '-i', default='./data/announcement',
              help='A 股公告数据的保存位置，按年划分，默认为 data/announcement')
@click.option('--output_dir', '-o', default='./data/analysis',
              help='输出路径，默认为 data/analysis')
def keyword_cluster(input_dir, output_dir):
    """根据指定关键词聚类公告"""
    ou.check_ret(su.cluster_announcement(
        ou.check_path(input_dir),
        ou.check_path(output_dir)
        ))

@analysis.command("generate-label-data")
@click.option('--input_dir', '-i', default='./data/announcement',
              help='A 股公告数据的保存位置，按年划分，默认为 data/announcement')
@click.option('--output_dir', '-o', default='./data/analysis',
              help='输出路径，默认为 data/analysis')
def generate_label_data(input_dir, output_dir):
    """生成用于标注的公告数据"""
    ou.check_ret(su.generate_label_data(
        ou.check_path(input_dir),
        ou.check_path(output_dir)
        ))

@analysis.command("match-announcement")
@click.option('--announcement_dir', '-adir', default='./data/announcement',
              help='A 股公告数据的保存位置，按年划分，默认为 data/announcement')
@click.option('--history_dir', '-hdir', default='./data/history',
              help='各股票历史数据的保存位置，按获取日期划分，默认为 ./data/history')
@click.option('--output_dir', '-o', default='./data/analysis',
              help='输出路径，默认为 data/analysis')
@click.option('--origin_file', default='./data/announcement/tingpai.txt',
              help='原始公告文件，默认为 ./data/announcement/tingpai.txt')
def match_announcement(announcement_dir, history_dir, output_dir, origin_file):
    """匹配公告数据与历史股价数据"""
    keywords = ["分配"]
    stopwords = []
    ou.check_ret(su.match_announcement(
        ou.check_path(announcement_dir), 
        ou.check_path(history_dir), 
        ou.check_path(output_dir),
        origin_file,
        keywords,
        stopwords,
        True))

