# !/usr/bin/env python3
import time


def get_time_string():
    """
    获得形如20161010120000这样的年月日时分秒字符串
    """
    current = time.localtime()
    return time.strftime("%Y%m%d%H%M%S", current)


def get_date_string():
    """
    获得形如20161010这样的年月日字符串
    """
    current = time.localtime()
    return time.strftime("%Y%m%d", current)


def get_year_month_string():
    """
    获得形如201610这样的年月字符串
    """
    current = time.localtime()
    return time.strftime("%Y%m", current)


if __name__ == "__main__":
    print(get_time_string())
    print(get_date_string())
    print(get_year_month_string())