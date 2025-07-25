#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author  :   Arthals
# @File    :   main.py
# @Time    :   2024/08/10 03:06:58
# @Contact :   zhuozhiyongde@126.com
# @Software:   Visual Studio Code


import time
from datetime import datetime, timedelta

import yaml

from session import BarkNotifier, Session

# load env
with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)


def start(notifier=None):
    print(f"{'[Start]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    s = Session(config=data, notifier=notifier)
    s.login()

    try:
        s.submit_all()
        print(f"{'[Succeed]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if notifier:
            notifier.send("All Succeed")
    except AssertionError as e:
        print(f"{'[Failed]':<15}: {e} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if notifier:
            notifier.send(f"Failed: {e}")


if __name__ == "__main__":
    print(f"{'[Schedule]':<15}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 计算到第二天 00:00:00 的时间差
    now = datetime.now()
    tomorrow = (now + timedelta(days=1)).replace(
        hour=8, minute=0, second=1, microsecond=0
    )
    wait_time = (tomorrow - now).total_seconds()

    print(f"{'[Waiting]':<15}: {wait_time} s")
    if data.get("auto", True):
        # 自动获取 2FA 验证码不需要提前提醒
        # 等待到第二天的 00:00:00 时刻
        if data.get("bark", None):
            notifier = BarkNotifier(data["bark"])
            notifier.send("已启动自动预约脚本")
        else:
            notifier = None
        time.sleep(wait_time)
    else:
        # 手动获取 2FA 验证码需要提前提醒
        # 等待到第二天的 00:00:00 时刻
        if data.get("bark", None):
            notifier = BarkNotifier(data["bark"])
            notifier.send("已启动自动预约脚本")
            if wait_time > 30:
                time.sleep(wait_time - 30)
                notifier.send("请准备在 30 秒后输入验证码")
                time.sleep(30)
            else:
                notifier.send("请立刻准备输入验证码，剩余时间已不足 30 秒")
                time.sleep(wait_time)
        else:
            notifier = None
            time.sleep(wait_time)

    # 开始执行任务
    start(notifier)
