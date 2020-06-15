#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 4:19 下午

class StatusCode:
    OK = 200
    TypeError = 501


error_map = {
    StatusCode.OK: "成功",
    StatusCode.TypeError: "类型错误，只能接受图片类型(image)文件。"
}
