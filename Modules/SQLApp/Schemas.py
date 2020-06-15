#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 6:35 下午
from pydantic import BaseModel


class DataParseBase(BaseModel):
    create_time: str
    result: str
    file_path: str


class DataParseCreate(DataParseBase):
    pass


class DataParse(DataParseBase):
    id: int
    file_path: str

    class Config:
        orm_mode = True
