#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 6:40 下午
from sqlalchemy.orm import Session
from . import Models, Schemas


def create_data_parse(db: Session, data: Schemas.DataParseCreate):
    # 创建新表格
    db_data = Models.DataParse(file_path=data.file_path, result=data.result, created_time=data.create_time)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
