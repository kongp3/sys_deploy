# -*- coding: utf-8 -*-
from prettytable import PrettyTable
from fabric.colors import yellow
from fabric.contrib.files import *


@task(name='help')
def deploy_help():
    print yellow("一. 查询可部署产品")
    print yellow("    1. 定义")
    helper = PrettyTable()
    helper.field_names = ["命令", "说明"]
    helper.align = "l"
    helper.add_row(["fab -f product.py -l", "xx产品"])
    print helper

    print yellow("    2. 举例")
    helper = PrettyTable()
    helper.field_names = ["命令", "结果"]
    helper.align = "l"
    helper.add_row(["fab -f product.py -l", "Available commands:"])
    helper.add_row(["", ""])
    helper.add_row(["", ""])
    helper.add_row(["", "php_sys"])
    helper.add_row(["", "py_sys"])
    print helper

    print yellow("二. 部署指令")
    print yellow("    1. 定义")
    helper = PrettyTable()
    helper.field_names = ["命令", "说明"]
    helper.align = "l"
    helper.add_row(["fab -f product.py py_sys", "部署 py_sys 产品, 分支为master"])
    helper.add_row(["fab -f product.py py_sys:2019", "部署 py_sys 产品, 分支为2019"])
    print helper

    print yellow("    2. 举例")
    print yellow("    请查看帮助文档 http://10.180.55.111:8088/x/x-mind/issues/15")


@task(name='detail')
def deploy_detail():
    detailer = PrettyTable()
    detailer.field_names = ["产品线", "命令", "对应产品"]
    detailer.align = "l"
    detailer.add_row(["XX", "py_sys", "后端"])
    detailer.add_row(["XX", "php_sys", "主站"])

    print detailer
