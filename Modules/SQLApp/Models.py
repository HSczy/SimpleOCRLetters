#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 6:23 下午

from sqlalchemy import Column, Integer, String

from .Database import Base


class DataParse(Base):
    __tablename__ = 'data_parse'
    # 用自增长的id作为主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 原始分析文件名称
    file_path = Column(String)
    # 生成的时间
    created_time = Column(String)
    # 得到的结果
    result = Column(String)

