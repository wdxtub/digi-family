import tushare as ts
import pandas as pd
import sys
import datetime
import os
import codecs
import csv
import time

import os_utils as ou
import time_utils as tu
import text_utils as utext

# crontab
# 0 18 * * * cd /data1/wdxtub/stock_projects/script; nohup ./daily-data.sh >> /data1/wdxtub/stock_projects/cron.log 2>&1 &


def daily_crawler(interval, path, root):

    now = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + oneday).strftime("%Y-%m-%d")
    folder = root + interval
    print("爬取", today, "所有股票的", interval, "分钟数据")
    if not os.path.exists(folder):
        print("创建保存数据的文件夹", folder)
        os.makedirs(folder, exist_ok=True)

    f = codecs.open(path, "r", "utf-8")
    csv_reader = csv.reader(f)
    count = -1
    fail_count = 0
    for line in csv_reader:
        count = count + 1
        if count == 0:
            # 过滤表头
            continue
        code = line[0]
        name = line[1]
        data = ts.get_hist_data(code, ktype=interval,
                                start=today, end=tomorrow)
        if data is None:
            fail_count = fail_count + 1
            continue
        else:
            dpath = ou.check_path(folder) + code + "-" + today + ".csv"
            data.to_csv(dpath)
    print("共尝试获取", count, "支股票的历史数据,其中", fail_count, "支股票获取失败")
    f.close()
    return 0


def get_stock_list(path):
    print("获取沪深上市公司基本情况")
    stock_basics = ts.get_stock_basics()
    # stock_basics.index, stock_basics.columns, stock_basics.values
    print("数据总数:", stock_basics.index.size)
    print("索引列名:", stock_basics.index.name)
    print("其他列名:", end=' ')
    for item in stock_basics.columns:
        print(item, end=' ')
    print("\n数据前 3 行")
    print(stock_basics.head(3))

    if not os.path.exists(path):
        print("创建保存数据的文件夹", path)
        os.mkdir(path)

    csvpath = ou.check_path(path) + "stock_basics.csv"
    print("全量数据将保存为", csvpath)
    stock_basics.sort_index().to_csv(csvpath)
    print("数据保存成功")
    return 0


def get_period_history_data(code, interval, path, start, end):
    print("获取单个股票一段时间内的历史数据")

    print("要获取的股票代码为:", code)
    data = ts.get_k_data(code, ktype=interval)
    if data is None:
        print("没有该股票的数据（可能是网络问题，也可能是本身就没有这个编号）")
        return -1
    else:
        print("共", data.index.size, "行数据")
        path = ou.check_path(path) + code + "#" + interval + ".csv"
        print("数据获取成功，将被保存在: ", path)
        data.to_csv(path)
        print("数据保存成功")
    return 0


def get_history_data(code, interval, path):
    print("获取单个股票的历史数据")

    if ou.check_interval(interval) == -1:
        print("时间间隔设置错误，请参考 help 文档")
        return -1

    if not os.path.exists(path):
        print("创建保存数据的文件夹", path)
        os.makedirs(path, exist_ok=True)

    print("要获取的股票代码为:", code)
    data = ts.get_k_data(code, ktype=interval)
    if data is None:
        print("没有该股票的数据（可能是网络问题，也可能是本身就没有这个编号）")
        return -1
    else:
        print("共", data.index.size, "行数据")
        path = ou.check_path(path) + code + "#" + interval + ".csv"
        print("数据获取成功，将被保存在: ", path)
        data.to_csv(path)
        print("数据保存成功")
    return 0


def get_all_history_data(interval, path, root):
    print("获取所有股票的历史数据（时间会比较长）")

    if ou.check_interval(interval) == -1:
        print("时间间隔设置错误，请参考 help 文档")
        return -1

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = root + timestamp + "#" + interval
    if not os.path.exists(folder):
        print("创建保存数据的文件夹", folder)
        os.makedirs(folder, exist_ok=True)

    print("开始从", path, "中读取股票列表")
    f = codecs.open(path, "r", "utf-8")
    csv_reader = csv.reader(f)
    count = -1
    fail_count = 0
    for line in csv_reader:
        count = count + 1
        if count == 0:
            # 过滤表头
            continue
        code = line[0]
        name = line[1]
        print("开始获取第", count, "支股票", code, name, "的历史数据")
        if get_history_data(code, interval, folder) != 0:
            fail_count = fail_count + 1

    print("共尝试获取", count, "支股票的历史数据,其中", fail_count, "支股票获取失败")
    f.close()
    return 0


cluster_centers = ["业绩类", "经营类", "股份变动类", "合同类"]
keywords_dict = {
    "业绩类": ["年度报告", "半年度报告", "季度报告", "业绩"],
    "经营类": ["收购", "购买", "重组", "并购", "资产"],
    "股份变动类": ["首次", "非公开", "员工持股", "股权激励", "发行", "增发", "配售", "分配", "要约收购", "举牌", "增持"],
    "合同类": ["中标", "合同", "订单"]
}

# 生成需要被标注的数据


def generate_label_data(apath, opath):
    record_list = get_all_announcement(apath)
    clean_list = []
    clean_count = 0

    print("根据关键词进行过滤")
    for center in cluster_centers:
        print("开始处理类别", center)
        for record in record_list:
            # 遍历关键词，选取
            for word in keywords_dict[center]:
                # 如果该关键词在标题中
                if word in record[2]:
                    # keywords_cluster[center].append("%s %s %s %s %s" % (record[0], record[1], record[2], record[3], record[4]))
                    # 只保留标题
                    clean_list.append(record)
                    clean_count = clean_count + 1
                    break
    print("过滤后共有 %d 条满足要求的标题" % clean_count)

    announcement_dict = {}
    unique_count = 0
    for record in clean_list:
        if not announcement_dict.__contains__(record[2]):
            announcement_dict[record[2]] = 1
            unique_count = unique_count + 1
        else:
            announcement_dict[record[2]] = announcement_dict[record[2]] + 1
    print("去处重复后的公告标题数目为 %d" % unique_count)
    # 结果写入到文件中
    sorted_list = sorted(announcement_dict.items(),
                         key=lambda x: x[1], reverse=True)
    now = int(time.time())
    filepath = "%sunlabelled-data-%d.csv" % (opath, now)

    with codecs.open(filepath, "w+", "utf-8") as f:
        for line in sorted_list:
            f.write("%d,%s\n" % (line[1], line[0]))
    print("写入完成，保存在 %s" % filepath)
    return 0

# 聚类公告


def cluster_announcement(apath, opath):

    keywords_cluster = {
        "业绩类": [],
        "经营类": [],
        "股份变动类": [],
        "合同类": []
    }
    cluster_counts = {
        "业绩类": 0,
        "经营类": 0,
        "股份变动类": 0,
        "合同类": 0
    }

    record_list = get_all_announcement(apath)
    record_count = len(record_list)
    # 考虑到一个公告可能属于两个或多个类别，所以以类别作为外层循环
    for center in cluster_centers:
        print("开始处理类别", center)
        for record in record_list:
            # 遍历关键词，选取
            for word in keywords_dict[center]:
                # 如果该关键词在标题中
                if word in record[2]:
                    # keywords_cluster[center].append("%s %s %s %s %s" % (record[0], record[1], record[2], record[3], record[4]))
                    # 只保留标题
                    keywords_cluster[center].append("%s" % record[2])
                    cluster_counts[center] = cluster_counts[center] + 1
                    break

    for center in cluster_centers:
        print(center, "类别数量", cluster_counts[center], "/", record_count)

    for center in cluster_centers:
        print("========================================")
        print(center, "类别数量", cluster_counts[center], "/", record_count)
        utext.get_lda_result(keywords_cluster[center])

        # for line in keywords_cluster[center]:
        #     print(line)

    return 0


# 根据公告匹配数据
def match_announcement(apath, hpath, opath, origin, keywords, stopwords, find_origin):
    print("匹配公告与历史股价数据")

    announcement_dict = {}
    if find_origin:
        # 如果 find_origin 为 true，需要找到原始公告数据
        texts = codecs.open(origin, "r", "utf-8")
        count = 0

        for line in texts:
            items = line.split("_")
            code = items[0]
            title = items[1]
            datestr = items[2]
            timestr = ":".join(items[3:5]) + ":" + items[5][:2]
            content = items[5][2:]

            announcement_dict["%s %s" % (code, title)] = (
                datestr, timestr, content)
            count = count + 1
        texts.close()
        print("需要载入原始公告内容，数量为", count)

    print("历史数据所在位置:", hpath)
    hdata = ""
    for parent, dirnames, _ in os.walk(hpath):
        # 获取最新日期的文件夹
        hdata = os.path.join(parent, sorted(dirnames, reverse=True)[0])
        break
    print("将使用", hdata, "中的历史股价数据")

    now = int(time.time())

    if not os.path.exists(opath):
        print("创建保存分析结果的文件夹", opath)
        os.mkdir(opath)

    r = codecs.open("%s%d_match_result.txt" % (opath, now), "w+", "utf-8")
    up_result = codecs.open("%s%d_up_result.txt" % (opath, now), "w+", "utf-8")
    down_result = codecs.open("%s%d_down_result.txt" %
                              (opath, now), "w+", "utf-8")

    record_list = get_all_announcement(apath)
    # 这样排序后方便获取历史数据，不然对内存压力太大，速度也会太慢
    print("根据股票代码进行排序")
    sorted_list = sorted(record_list, key=lambda d: d[0])
    current_stock = ""
    change = 0
    current_history = ""
    current_code = ""
    search_max = 1000
    up_count = 0
    down_count = 0
    for line in sorted_list:
        if current_stock != line[1]:
            change = change + 1
            # 测试一个股票
            # if change == 3:
            #      break

            # 这里获取的是 60 分钟的数据
            try:
                current_history = pd.read_csv(
                    hdata + '/' + line[0] + "#60.csv")
            except:
                print("无对应股价信息，跳过")
                continue
            print("读取", line[0], line[1], "的历史数据，共",
                  current_history.index.size, "条")
            if current_history.index.size == 0:
                print("无历史数据，跳过")
                continue
            current_stock = line[1]
            ou.split_line("-", 1, 20)
            print("开始匹配", line[0], line[1], "的公告与历史股价数据")
            current_code = current_history.head(1).code.values[0]
            ou.split_line("-", 1, 20)
            # print(current_history.head(10))
            # print(current_history.dtypes)
        print("公告标题:", line[2], "，公告日期:", line[3], line[4])
        # 检查公告标题中是否包含指定词语
        is_target = False
        for word in keywords:
            if word in line[2]:
                is_target = True
                break

        if not is_target:
            print("标题中不包含指定关键词，跳过")
            continue

        # 检查公告标题中是否包含需要过滤的词，如果包含，直接跳过
        should_filtered = False
        for word in stopwords:
            if word in line[2]:
                should_filtered = True
                break

        if should_filtered:
            print("标题中包含需要过滤的词，跳过")
            continue

        # 这里需要处理日期和时间（周末和无法交易的时刻）
        period = tu.get_compare_data(line[3], line[4])
        prev_frame = current_history[current_history.date.str.contains(
            "%s %s" % (period[0], period[1]))]
        next_frame = current_history[current_history.date.str.contains(
            "%s %s" % (period[3], period[4]))]

        # 如果停牌没数据，需要继续查找
        prev_slot = (period[0], period[1])
        next_slot = (period[3], period[4])
        lookup_count = 0
        while len(prev_frame) == 0:
            prev_slot = tu.get_prev_trade_slot(prev_slot[0], prev_slot[1])
            prev_frame = current_history[current_history.date.str.contains(
                "%s %s" % (prev_slot[0], prev_slot[1]))]
            lookup_count = lookup_count + 1
            if lookup_count > search_max:
                print("超出股价搜寻范围，跳过本公告")
                break
        if lookup_count > search_max:
            continue

        lookup_count = 0
        while len(next_frame) == 0:
            next_slot = tu.get_next_trade_slot(next_slot[0], next_slot[1])
            next_frame = current_history[current_history.date.str.contains(
                "%s %s" % (next_slot[0], next_slot[1]))]
            lookup_count = lookup_count + 1
            if lookup_count > search_max:
                print("超出股价搜寻范围，跳过本公告")
                break
        if lookup_count > search_max:
            continue

        # print(prev_frame, len(prev_frame), prev_frame.size)
        # print(next_frame, len(next_frame), next_frame.size)
        is_prev_price_exist = False
        is_next_price_exist = False
        if prev_frame.code.values[0] != current_code:
            prev_price = -1.0
        else:
            prev_price = prev_frame[period[2]].values[0]
            is_prev_price_exist = True

        if next_frame.code.values[0] != current_code:
            next_price = -1.0
        else:
            next_price = next_frame[period[5]].values[0]
            if next_price != 0.0:  # 如果等于 0，则不处理
                is_next_price_exist = True

        if is_next_price_exist and is_prev_price_exist:
            # 这里还需要寻找原始的公告数据
            content = ""
            matched = False
            if find_origin:
                ikey = "%s %s" % (current_code, line[2])
                if announcement_dict.__contains__(ikey):
                    content = announcement_dict[ikey]
                    matched = True

            delta = next_price - prev_price

            change_str = "股价变动 %.2f，公告前价格 %.2f，公告后价格 %.2f\n" % (
                delta, prev_price, next_price)
            title_str = "股票: %s %s，公告标题: %s，公告日期: %s %s\n" % (
                line[0], line[1], line[2], line[3], line[4])

            print(change_str, end="")
            r.write(title_str)
            r.write(change_str)

            if matched:
                announce_str = "公告原文: %s" % content[2]
                r.write(announce_str)

            if delta > 0:
                up_count = up_count + 1
                up_result.write(title_str)
                up_result.write(change_str)
                up_result.write("-  -  -  -  -  -  -  -  -  -  -\n")
            elif delta < 0:
                down_count = down_count + 1
                down_result.write(title_str)
                down_result.write(change_str)
                down_result.write("-  -  -  -  -  -  -  -  -  -  -\n")

        else:
            if not is_next_price_exist:
                print("无法找到前一个交易日的股价")
            if not is_next_price_exist:
                print("无法找到后一个交易日的股价")

        r.write("-  -  -  -  -  -  -  -  -  -  -\n")
        ou.split_line("-", 2, 10)

    r.write("发布公告后上涨的数量 %d\n" % up_count)
    r.write("发布公告后下跌的数量 %d\n" % down_count)
    r.close()
    up_result.close()
    down_result.close()

    return 0

# 获取所有的公告


def get_all_announcement(apath):
    print("公告所在位置:", apath)
    record_list = []
    record_count = 0
    for parent, dirnames, _ in os.walk(apath):
        for dirname in dirnames:
            if dirname[0] == ".":
                continue
            print("公告年份:", dirname)
            for _, _, filenames in os.walk(os.path.join(parent, dirname)):
                for filename in filenames:
                    if filename[0] == ".":
                        continue
                    print("正在读取公告文件列表:", filename)
                    f = codecs.open(os.path.join(
                        parent, dirname, filename), "r", "utf-8")
                    csv_reader = csv.reader(f)
                    for line in csv_reader:
                        # 把一个 tuple 添加到 list 中
                        record_list.append(
                            (line[1], line[2], line[3], line[4], line[5]))
                        record_count = record_count + 1
                    f.close()
                    print("目前公告标题数:", record_count)
    print("总公告标题数:", record_count)
    return record_list


# 获取基本面数据
def get_fundamental_data(opath):
    print("获取沪深上市公司的基本面情况（会花费较长时间，请耐心等待）")
    if not os.path.exists(opath):
        print("创建保存数据的文件夹", opath)
        os.makedirs(opath, exist_ok=True)

    print("#1 获取股票列表")
    csvpath = ou.check_path(opath) + "stock_basics.csv"
    if os.path.exists(csvpath): # 如果存在，则直接跳过，不重复获取
        print("已有该股票列表数据，跳过获取")
    else:
        stock_basics = ts.get_stock_basics()
        print("数据总数:", stock_basics.index.size)
        print("全量数据将保存为", csvpath)
        stock_basics.sort_index().to_csv(csvpath)
        print("数据保存成功")

    title = ["业绩报告", "盈利能力", "营运能力", 
    "成长能力", "偿债能力", "现金流量"]
    en_name = ["report_data", "profit_data", "operation_data", 
    "growth_data", "debtpaying_data", "cashflow_data"]

    count = 0
    while count < len(title):
        print("#%d 获取 %s 报表" % (count + 2, title[count]))
        # 从 1989 到现在
        now = datetime.datetime.now()
        year = 1989
        while year <= now.year:
            season = 1
            while season <= 4:
                print("获取 %d 年第 %d 季度的 %s 报表" % (year, season, title[count]))
                try:
                    csvpath = "%s%d-%d-%s.csv" % (ou.check_path(opath), year, season, en_name[count])
                    if os.path.exists(csvpath): # 如果存在，则直接跳过，不重复获取
                        print("已有该季度数据，跳过获取")
                        season = season + 1
                        continue
                    exec("data = ts.get_%s(%d, %d)" %(en_name[count], year, season))
                    exec('data.sort_index().to_csv(csvpath)')
                    print("\n数据保存成功")
                except IOError:
                    print("获取数据错误，跳过该季度")
                season = season + 1
            year = year + 1
        count = count + 1
    return 0

def get_macro_enco_data(opath):
    print("获取沪深上市公司的基本面情况（会花费较长时间，请耐心等待）")
    if not os.path.exists(opath):
        print("创建保存数据的文件夹", opath)
        os.makedirs(opath, exist_ok=True)

    now = datetime.datetime.now()

    title = ["存款利率", "贷款利率", "存款准备金率", 
    "货币供应量", "货币供应量(年底余额)", "国内生产总值(年度)",
    "国内生产总值(季度)", "三大需求对 GPD 贡献", "三大产业对 GDP 拉动",
    "三大产业贡献率", "居民消费价格指数", "工业品出场价格指数"]
    en_name = ["deposit_rate", "loan_rate", "rrr", 
    "money_supply", "money_supply_bal", "gdp_year",
    "gdp_quarter", "gdp_for", "gdp_pull", 
    "gdp_contrib", "cpi", "ppi"]

    count = 0
    while count < len(title):
        print("#%d 获取 %s 报表" % (count + 1, title[count]))
        try:
            csvpath = "%s%d-%2d-%2d-%s.csv" % (ou.check_path(opath), now.year, now.month, now.day, en_name[count])
            if os.path.exists(csvpath): # 如果存在，则直接跳过，不重复获取
                print("已有该数据，跳过获取")
                count = count + 1
                continue
            exec("data = ts.get_%s()" % en_name[count])
            exec('data.sort_index().to_csv(csvpath)')
            print("数据保存成功")
        except IOError:
            print("获取数据错误，跳过指标")
        count = count + 1
    return 0