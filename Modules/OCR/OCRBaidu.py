#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Zhenyu Chan
# E-mail:hsczyic@gmail.com
# Time: : 2020/6/15 5:13 下午
import datetime
import json

from sqlalchemy.orm import Session

import Settings
import os

from aip import AipOcr
from dotenv import load_dotenv
from Modules.SQLApp import CRUD, Models, Schemas
from Modules.SQLApp.Database import SessionLocal, engine
from Modules.SQLApp.Schemas import DataParseCreate

Models.Base.metadata.create_all(bind=engine)

load_dotenv()


# Dependency


class OCRBaidu:
    """
    使用百度接口进行OCR识别
    """

    def __init__(self, file_name):
        AppId = os.getenv('AppId')
        APIKey = os.getenv('APIKey')
        SecretKey = os.getenv('SecretKey')
        self.client = AipOcr(AppId, APIKey, SecretKey)
        FileDir = Settings.FileDir
        self.file_name = os.path.join(FileDir, file_name)
        self.db: Session = SessionLocal()

    def get_content_from_pic(self):
        # 用二进制读取图片文件
        with open(self.file_name, 'rb') as f:
            image_data = f.read()
        # 获取图片结果
        results = self.client.general(image_data)['words_result']
        # 对文字进行整理，返回完整文字内容
        content = ''
        for result in results:
            content += result['words']
        return content

    def get_litter(self):
        # 对文本进行处理，返回字母列表
        content = self.get_content_from_pic()
        if ' ' in content:
            content = content.replace(' ', '')
        if '\n' in content:
            content = content.replace('\n', '')
        # 将内容存入至数据库
        schema_data = DataParseCreate(
            file_path=self.file_name,
            create_time=datetime.datetime.now().timestamp(),
            result=json.dumps(list(content))
        )
        CRUD.create_data_parse(db=self.db, data=schema_data)
        return list(content)


if __name__ == '__main__':
    print(OCRBaidu('97652-150a53012f8e5279.png').get_litter())
