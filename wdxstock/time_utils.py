import datetime


holiday = ["2017-10-01", "2017-10-02", "2017-10-03", "2017-10-04",
           "2017-10-05", "2017-10-06", "2017-10-07", "2017-10-08"]

'''
00:00:00 - 09:20:00 -> 0
09:20:01 - 10:20:00 -> 1
10:20:01 - 11:20:00 -> 2
11:20:01 - 12:50:00 -> 3
12:50:01 - 13:50:00 -> 4
13:50:01 - 14:50:00 -> 5
14:50:01 - 23:59:59 -> 6
'''

trade_time_intervel = [("00:00:00-09:20:00", "15:00", "close", "10:30", "open"),
                       ("09:20:01-10:20:00", "10:30", "open", "10:30", "close"),
                       ("10:20:01-11:20:00", "11:30", "open", "11:30", "close"),
                       ("11:20:01-12:50:00", "11:30", "close", "14:00", "open"),
                       ("12:50:01-13:50:00", "14:00", "open", "14:00", "close"),
                       ("13:50:01-14:50:00", "15:00", "open", "15:00", "close"),
                       ("14:50:01-23:59:59", "15:00", "close", "10:30", "open")]

m_start = datetime.datetime.strptime("09:20:01", "%H:%M:%S")
m_middle = datetime.datetime.strptime("10:20:01", "%H:%M:%S")
m_end = datetime.datetime.strptime("11:20:00", "%H:%M:%S")
a_start = datetime.datetime.strptime("12:50:01", "%H:%M:%S")
a_middle = datetime.datetime.strptime("13:50:01", "%H:%M:%S")
a_end = datetime.datetime.strptime("14:50:00", "%H:%M:%S")


'''
获取公告对应的有效交易时间

# 传入的时间字符串格式为 2017-10-11 00:00:00
# 股票交易时间 9:30-11:30 13:00-15:00
1. 能够获取到的时间为 [D] 10:30 11:30 14:00 15:00
# 时间节点的表示
1. 10:30 的开盘价表示 9:30 的价格，收盘价表示 10:30 的价格
2. 11:30 的开盘价表示 10:30 的价格，收盘价表示 11:30 的价格
3. 14:00 的开盘价表示 13:00 的价格，收盘价表示 14:00 的价格
4. 15:00 的开盘价表示 14:00 的价格，收盘价表示 15:00 的价格
# 主要是要处理周末、节假日以及非交易时间的情况，具体的情况为
1. 如果公告在周五结束交易到周一开始交易之间发布，那么比较周五 14:00 收盘与周一 10:30 开盘
2. 具体时间比较，以十分钟为阈值区间
   公告发布于 09:21-10:20，比较 10:30 的开盘和 10:30 的收盘
   公告发布于 10:21-11:20，比较 11:30 的开盘和 11:30 的收盘
   公告发布于 11:21-12:50，比较 11:30 的收盘和 14:00 的开盘
   公告发布于 12:51-13:50，比较 14:00 的开盘和 14:00 的收盘
   公告发布于 13:51-14:50，比较 15:00 的开盘和 15:00 的收盘
   公告发布于 14:51-09:20(下一交易日)，比较 15:00 的收盘和 10:30(下一交易日)的开盘
3. 如果遇到节假日，则在规则 1 的基础上顺延

'''

# 这里的 datestr 与 timestr 一定是在交易期间的
def get_next_trade_slot(datestr, timestr):
    cdate = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    if timestr == "10:30":
        return (datestr, "11:30")
    elif timestr == "11:30":
        return (datestr, "14:00")
    elif timestr == "14:00":
        return (datestr, "15:00")
    elif timestr == "15:00":
        return (format_date(get_next_trade_day(cdate)), "10:30")


# 这里的 datestr 与 timestr 一定是在交易期间的
def get_prev_trade_slot(datestr, timestr):
    cdate = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    if timestr == "15:00":
        return (datestr, "14:00")
    elif timestr == "14:00":
        return (datestr, "11:30")
    elif timestr == "11:30":
        return (datestr, "10:30")
    elif timestr == "10:30":
        return (format_date(get_prev_trade_day(cdate)), "15:00")


def is_trade_day(cdate):
    week = cdate.weekday()
    if week == 5 or week == 6:  # 如果是周末，一定不是交易日
        return False
    # 如果是在周中，需要判断是否是休息日
    if cdate.strftime("%Y-%m-%d") in holiday:
        return False
    # 如果都不是，就是交易日
    return True


def get_next_trade_day(cdate):
    oneday = datetime.timedelta(days=1)
    next_trade_day = cdate + oneday
    while not is_trade_day(next_trade_day):
        next_trade_day = next_trade_day + oneday
    return next_trade_day


def get_prev_trade_day(cdate):
    oneday = datetime.timedelta(days=1)
    prev_trade_day = cdate - oneday
    while not is_trade_day(prev_trade_day):
        prev_trade_day = prev_trade_day - oneday
    return prev_trade_day


def format_date(cdate):
    return cdate.strftime("%Y-%m-%d")


def get_trade_interval(ctime):
    # 判断是否在交易时间内
    if ctime < m_start:  # 早于交易时间
        return 0
    elif m_start <= ctime and ctime < m_middle:
        return 1
    elif m_middle <= ctime and ctime < m_end:
        return 2
    elif m_end <= ctime and ctime < a_start:
        return 3
    elif a_start <= ctime and ctime < a_middle:
        return 4
    elif a_middle <= ctime and ctime < a_end:
        return 5

    return 6

# 返回一个六个元素的 tuple


def get_compare_data(datestr, timestr):
    cdate = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    ctime = datetime.datetime.strptime(timestr, "%H:%M:%S")

    if is_trade_day(cdate):  # 是交易日
        trade_time_flag = get_trade_interval(ctime)
        interval = trade_time_intervel[trade_time_flag]
        if 0 < trade_time_flag and trade_time_flag < 6:
            return (format_date(cdate), interval[1], interval[2],
                    format_date(cdate), interval[3], interval[4])
        elif trade_time_flag == 0:
            return (format_date(get_prev_trade_day(cdate)), interval[1], interval[2],
                    format_date(cdate), interval[3], interval[4])
        elif trade_time_flag == 6:
            return (format_date(cdate), interval[1], interval[2],
                    format_date(get_next_trade_day(cdate)), interval[3], interval[4])
        else:
            return None
    else:  # 不是交易日
        return (format_date(get_prev_trade_day(cdate)), "15:00", "close",
                format_date(get_next_trade_day(cdate)), "10:30", "open")
